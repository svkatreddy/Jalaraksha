from app.models import SurveyResponse
from app.extensions import db

def test_valid_survey_submission(client, app):
    """Test 13: Valid survey response persists properly in the database."""
    survey_data = {
        'area_label': 'North Campus Academic Zone',
        'observed_wastage': 'Yes',
        'observed_categories': [
            'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
            'Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)'
        ],
        'awareness_level': 'Moderate',
        'rainwater_harvesting': 'Yes',
        'rwh_pit': 'Yes',
        'cyclone_impact': 'Minor leaks',
        'suggestion': 'Place visual conservation signs in all restrooms.'
    }
    response = client.post('/survey', data=survey_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thank You for Your Feedback!" in response.data

    with app.app_context():
        saved = SurveyResponse.query.filter_by(area_label='North Campus Academic Zone').first()
        assert saved is not None
        assert saved.observed_wastage == 'Yes'
        assert saved.awareness_level == 'Moderate'
        assert saved.rainwater_harvesting == 'Yes'
        assert saved.rwh_pit == 'Yes'
        assert saved.cyclone_impact == 'Minor leaks'
        categories = saved.get_categories()
        assert 'Everyday Leak / Wastage (Taps, Pipes, Tanks)' in categories
        assert 'Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)' in categories


def test_invalid_survey_choice_rejected(client, app):
    """Test 14: Invalid choices are rejected server-side."""
    invalid_data = {
        'area_label': 'Market Area',
        'observed_wastage': 'InvalidWastageString',
        'awareness_level': 'SuperHigh',
        'rainwater_harvesting': 'Maybe',
        'rwh_pit': 'InvalidRWH',
        'cyclone_impact': 'Tornado'
    }
    response = client.post('/survey', data=invalid_data)
    # The form validator should prevent submission or route reject
    assert response.status_code == 200
    with app.app_context():
        # Nothing should be saved
        assert SurveyResponse.query.filter_by(area_label='Market Area').first() is None


def test_admin_survey_analytics_view(auth_client, app):
    """Verify admin survey analytics displays accurate aggregate metrics."""
    with app.app_context():
        s1 = SurveyResponse(
            area_label='Hostel A',
            observed_wastage='Yes',
            awareness_level='High',
            rainwater_harvesting='Yes',
            rwh_pit='Yes',
            cyclone_impact='Minor leaks',
            suggestion='Fix garden sprinklers.'
        )
        s1.set_categories(['Everyday Leak / Wastage (Taps, Pipes, Tanks)'])

        s2 = SurveyResponse(
            area_label='Block B',
            observed_wastage='No',
            awareness_level='Moderate',
            rainwater_harvesting='No',
            rwh_pit='No',
            cyclone_impact='No damage',
            suggestion=''
        )
        s2.set_categories([])

        db.session.add_all([s1, s2])
        db.session.commit()

    resp = auth_client.get('/admin/survey-results')
    assert resp.status_code == 200
    assert b"Community Survey Analytics" in resp.data
    assert b"Total: <strong>2</strong>" in resp.data
    assert b"Fix garden sprinklers." in resp.data
