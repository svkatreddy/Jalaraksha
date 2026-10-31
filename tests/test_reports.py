import io
from datetime import date, timedelta
from app.models import WaterReport, ReportStatusHistory
from app.extensions import db

def test_valid_report_submission(client, app):
    """Test 3: Valid report submission stores a record and returns reference code."""
    data = {
        'category': 'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
        'location_text': 'Science Block A Ground Floor Washroom',
        'observed_on': date.today().strftime('%Y-%m-%d'),
        'description': 'Continuous high drip from the central washbasin tap.'
    }
    response = client.post('/report', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thank You for Reporting!" in response.data
    assert b"JR-" in response.data

    with app.app_context():
        report = WaterReport.query.filter_by(location_text=data['location_text']).first()
        assert report is not None
        assert report.status == 'Submitted'
        assert report.reference_code.startswith('JR-')
        assert len(report.reference_code) == 13

        # Verify initial audit history entry was logged
        hist = ReportStatusHistory.query.filter_by(report_id=report.id).first()
        assert hist is not None
        assert hist.new_status == 'Submitted'


def test_missing_required_field_rejected(client):
    """Test 4: Missing required fields are rejected with validation error."""
    # Omit location_text and description
    data = {
        'category': 'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
        'location_text': '',
        'observed_on': date.today().strftime('%Y-%m-%d'),
        'description': ''
    }
    response = client.post('/report', data=data)
    assert response.status_code == 200
    assert b"Please enter a broad location description" in response.data
    assert b"Please provide a concise description" in response.data


def test_future_observed_date_rejected(client):
    """Test 5: Future observed date is rejected."""
    future_date = date.today() + timedelta(days=5)
    data = {
        'category': 'Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)',
        'location_text': 'Hostel 1 Roof Tank',
        'observed_on': future_date.strftime('%Y-%m-%d'),
        'description': 'Future leak observation test.'
    }
    response = client.post('/report', data=data)
    assert response.status_code == 200
    assert b"The observed date cannot be in the future" in response.data


def test_public_tracking_valid_code(client, app):
    """Test 6: Tracking by valid reference code displays public status."""
    with app.app_context():
        report = WaterReport(
            reference_code='JR-VALIDCODE1',
            category='Damaged public water outlet',
            location_text='Town Hall Square Public Tap',
            description='Private description that must not show in public tracking.',
            observed_on=date.today(),
            status='In Progress',
            public_update='Municipal team notified; valve replacement pending.',
            internal_note='Secret admin note: Contractor quote $50 received.'
        )
        db.session.add(report)
        db.session.commit()

    # Track via GET query or URL
    response = client.get('/track?code=JR-VALIDCODE1')
    assert response.status_code == 200
    assert b"JR-VALIDCODE1" in response.data
    assert b"In Progress" in response.data
    assert b"Town Hall Square Public Tap" in response.data
    assert b"Municipal team notified" in response.data

    # Direct URL route
    resp2 = client.get('/track/JR-VALIDCODE1')
    assert resp2.status_code == 200
    assert b"JR-VALIDCODE1" in resp2.data


def test_public_tracking_invalid_code(client):
    """Test 7: Invalid reference code displays a neutral not-found message."""
    response = client.post('/track', data={'reference_code': 'JR-NOTEXIST99'})
    assert response.status_code == 200
    assert b"No report found for that reference code" in response.data


def test_public_tracking_never_exposes_internal_note(client, app):
    """Test 8: Public tracking strictly hides internal notes and descriptions."""
    with app.app_context():
        report = WaterReport(
            reference_code='JR-CONFIDNTL1',
            category='Other',
            location_text='Community Park Fountain',
            description='Detailed confidential witness statement here.',
            observed_on=date.today(),
            status='Under Review',
            public_update='Under safety inspection.',
            internal_note='TOP_SECRET_INTERNAL_NOTE_12345'
        )
        db.session.add(report)
        db.session.commit()

    response = client.get('/track?code=JR-CONFIDNTL1')
    assert response.status_code == 200
    assert b"TOP_SECRET_INTERNAL_NOTE_12345" not in response.data
    assert b"Detailed confidential witness statement here." not in response.data


def test_unsupported_image_upload_rejected(client):
    """Test 17: Uploading unsupported file types (like .txt or .exe) is rejected."""
    data = {
        'category': 'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
        'location_text': 'Library Restroom',
        'observed_on': date.today().strftime('%Y-%m-%d'),
        'description': 'Tap leaking steadily.',
        'photo': (io.BytesIO(b"executable payload"), "malicious.exe")
    }
    response = client.post('/report', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"Only JPG, JPEG, PNG, or WebP images are allowed" in response.data
