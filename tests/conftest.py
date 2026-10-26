import pytest
from app import create_app
from app.extensions import db
from app.models import AdminUser, WaterReport, SurveyResponse
from config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a testing Flask application instance."""
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def admin_user(app):
    """Create a test administrator."""
    with app.app_context():
        admin = AdminUser(username='testadmin')
        admin.set_password('AdminSecret123!')
        db.session.add(admin)
        db.session.commit()
        return admin


@pytest.fixture
def auth_client(client, admin_user):
    """Client authenticated as the test administrator."""
    client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'AdminSecret123!'
    }, follow_redirects=True)
    return client
