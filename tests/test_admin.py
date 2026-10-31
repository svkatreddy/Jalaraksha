from datetime import date
from app.models import WaterReport, ReportStatusHistory
from app.extensions import db

def test_admin_login_success_and_failure(client, admin_user):
    """Test 9: Admin login succeeds with valid password and fails with invalid password."""
    # Failure attempt
    fail_resp = client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    assert fail_resp.status_code == 200
    assert b"Invalid username or password" in fail_resp.data

    # Success attempt
    success_resp = client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'AdminSecret123!'
    }, follow_redirects=True)
    assert success_resp.status_code == 200
    assert b"Welcome back, Administrator" in success_resp.data
    assert b"Administrator Operations Dashboard" in success_resp.data


def test_protected_admin_routes_reject_unauthenticated(client):
    """Test 10: Unauthenticated visitors are redirected away from /admin."""
    endpoints = [
        '/admin',
        '/admin/reports',
        '/admin/survey-results',
        '/admin/reports/export.csv'
    ]
    for url in endpoints:
        resp = client.get(url)
        assert resp.status_code in (302, 401)
        # Should redirect to login
        assert '/admin/login' in resp.headers.get('Location', '')


def test_admin_update_report_status_and_audit_history(auth_client, app):
    """Test 11 & 18: Admin updates report status; persists change and records audit history."""
    with app.app_context():
        report = WaterReport(
            reference_code='JR-UPDATETEST',
            category='Everyday Leak / Wastage (Taps, Pipes, Tanks)',
            location_text='Auditorium Basement',
            description='Slow drip under basin.',
            observed_on=date.today(),
            status='Submitted'
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    # Admin updates status to 'In Progress'
    update_data = {
        'status': 'In Progress',
        'public_update': 'Plumber assigned to inspect basement piping.',
        'internal_note': 'Contacted maintenance head.'
    }
    resp = auth_client.post(f'/admin/reports/{report_id}', data=update_data, follow_redirects=True)
    assert resp.status_code == 200
    assert b"status updated to" in resp.data
    assert b"In Progress" in resp.data

    with app.app_context():
        updated = db.session.get(WaterReport, report_id)
        assert updated.status == 'In Progress'
        assert updated.public_update == update_data['public_update']
        assert updated.internal_note == update_data['internal_note']

        # Verify audit history
        hist = ReportStatusHistory.query.filter_by(report_id=report_id, new_status='In Progress').first()
        assert hist is not None
        assert hist.old_status == 'Submitted'
        assert hist.public_update == update_data['public_update']


def test_resolved_status_requires_resolution_note(auth_client, app):
    """Test 12: Marking status as 'Resolved' requires a resolution note."""
    with app.app_context():
        report = WaterReport(
            reference_code='JR-RESOLVETEST',
            category='Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)',
            location_text='Cafeteria Water Tank',
            description='Overflow during noon.',
            observed_on=date.today(),
            status='In Progress'
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    # Try resolving without public_update verification note
    invalid_data = {
        'status': 'Resolved',
        'public_update': '',
        'internal_note': 'Tried fixing.'
    }
    resp = auth_client.post(f'/admin/reports/{report_id}', data=invalid_data)
    assert resp.status_code == 200
    assert b"you must provide a public update confirming how the resolution was verified" in resp.data

    with app.app_context():
        assert db.session.get(WaterReport, report_id).status == 'In Progress'

    # Now provide valid verification note
    valid_data = {
        'status': 'Resolved',
        'public_update': 'Float switch sensor replaced and verified leak-free on inspection.',
        'internal_note': 'Approved by campus engineer.'
    }
    resp2 = auth_client.post(f'/admin/reports/{report_id}', data=valid_data, follow_redirects=True)
    assert resp2.status_code == 200
    assert b"status updated to" in resp2.data
    assert b"Resolved" in resp2.data

    with app.app_context():
        r = db.session.get(WaterReport, report_id)
        assert r.status == 'Resolved'
        assert r.resolved_at is not None


def test_dashboard_counts_match_database(auth_client, app):
    """Test 15: Dashboard counts accurately reflect database records."""
    with app.app_context():
        r1 = WaterReport(
            reference_code='JR-DASH001',
            category='Everyday Leak / Wastage (Taps, Pipes, Tanks)',
            location_text='Hostel 1',
            description='Test leak',
            observed_on=date.today(),
            status='Submitted'
        )
        r2 = WaterReport(
            reference_code='JR-DASH002',
            category='Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)',
            location_text='Hostel 2',
            description='Test overflow',
            observed_on=date.today(),
            status='Resolved'
        )
        db.session.add_all([r1, r2])
        db.session.commit()

    resp = auth_client.get('/admin')
    assert resp.status_code == 200
    # Total reports should be 2
    assert b"Total Reports" in resp.data
    assert b"JR-DASH001" in resp.data
    assert b"JR-DASH002" in resp.data


def test_csv_export_protection_and_sanitization(auth_client, app):
    """Test 16: CSV export is protected and neutralizes formula injection."""
    with app.app_context():
        # Insert a report with a potentially malicious formula prefix
        malicious_report = WaterReport(
            reference_code='JR-FORMULACAP',
            category='Other',
            location_text='=1+1;PAYLOAD_TEST',
            description='Formula test.',
            observed_on=date.today(),
            status='Submitted',
            public_update='+CMD_INJECTION_TEST',
            internal_note='SECRET_ADMIN_NOTE_DO_NOT_EXPORT'
        )
        db.session.add(malicious_report)
        db.session.commit()

    resp = auth_client.get('/admin/reports/export.csv')
    assert resp.status_code == 200
    assert resp.mimetype == 'text/csv'
    csv_text = resp.data.decode('utf-8')

    # Formula injection characters must be prefixed with single quote
    assert "'=1+1;PAYLOAD_TEST" in csv_text
    assert "'+CMD_INJECTION_TEST" in csv_text

    # Private internal note must NOT be in the CSV
    assert "SECRET_ADMIN_NOTE_DO_NOT_EXPORT" not in csv_text
