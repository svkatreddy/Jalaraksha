import os
from pathlib import Path
from datetime import datetime, date, timezone, timedelta
import click
from flask import Flask, render_template
from config import Config
from app.extensions import db, login_manager, csrf

def create_app(config_class=Config):
    """Application factory for JalaRaksha."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Ensure instance and upload directories exist
    instance_path = Path(app.config['INSTANCE_PATH'])
    upload_path = Path(app.config['UPLOAD_FOLDER'])
    instance_path.mkdir(parents=True, exist_ok=True)
    upload_path.mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes import public_bp, reports_bp, survey_bp, admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(admin_bp)

    # Context processors
    @app.context_processor
    def inject_global_vars():
        return {
            'current_year': datetime.now(timezone.utc).year
        }

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template(
            'errors/400.html',
            message="Uploaded file is too large. Maximum allowed size is 3 MB."
        ), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # CLI Commands
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    """Register custom Click CLI commands for management."""

    @app.cli.command('init-db')
    def init_db_command():
        """Create all database tables."""
        with app.app_context():
            db.create_all()
            click.echo("Initialized the database tables in: " + str(app.config['SQLALCHEMY_DATABASE_URI']))

    @app.cli.command('create-admin')
    @click.option('--username', prompt=True, help='Administrator username')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Administrator password')
    def create_admin_command(username, password):
        """Create or reset an administrator account securely."""
        from app.models import AdminUser
        username = username.strip()
        if not username or not password:
            click.echo("Error: Username and password must not be empty.")
            return

        with app.app_context():
            db.create_all()
            user = AdminUser.query.filter_by(username=username).first()
            if user:
                user.set_password(password)
                user.is_active = True
                db.session.commit()
                click.echo(f"Administrator '{username}' password successfully updated.")
            else:
                user = AdminUser(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                click.echo(f"Administrator '{username}' created successfully.")

    @app.cli.command('seed-demo-data')
    def seed_demo_data_command():
        """
        Populate sample demonstration records clearly labelled as test data.
        NOTE: These records are exclusively for testing the user interface and local flows.
        """
        from app.models import WaterReport, ReportStatusHistory, SurveyResponse

        with app.app_context():
            db.create_all()
            
            # Create sample reports
            demo_reports = [
                {
                    'reference_code': 'JR-DEMO0001A',
                    'category': 'Leaking tap/pipe',
                    'location_text': 'Engineering Block A, 1st floor water cooler',
                    'description': '[DEMO TEST RECORD] Minor drip observed from cooler inlet valve.',
                    'observed_on': date.today() - timedelta(days=2),
                    'status': 'Under Review',
                    'public_update': 'Report inspected by maintenance supervisor.',
                    'internal_note': 'Scheduled plumber for Thursday routine service.'
                },
                {
                    'reference_code': 'JR-DEMO0002B',
                    'category': 'Overflowing tank',
                    'location_text': 'Hostel 3 Overhead Storage Tank',
                    'description': '[DEMO TEST RECORD] Tank overflow pipe running during morning pump cycle.',
                    'observed_on': date.today() - timedelta(days=5),
                    'status': 'Resolved',
                    'public_update': 'Float valve repaired and water level sensor recalibrated on Oct 24.',
                    'internal_note': 'Verified outcome on-site with hostel warden.'
                },
                {
                    'reference_code': 'JR-DEMO0003C',
                    'category': 'Damaged public water outlet',
                    'location_text': 'Main Campus Sports Ground Tap',
                    'description': '[DEMO TEST RECORD] Push-tap missing handle, continuous trickle.',
                    'observed_on': date.today() - timedelta(days=1),
                    'status': 'Submitted',
                    'public_update': 'Report received and queued for review.',
                    'internal_note': None
                }
            ]

            for d in demo_reports:
                existing = WaterReport.query.filter_by(reference_code=d['reference_code']).first()
                if not existing:
                    rep = WaterReport(
                        reference_code=d['reference_code'],
                        category=d['category'],
                        location_text=d['location_text'],
                        description=d['description'],
                        observed_on=d['observed_on'],
                        status=d['status'],
                        public_update=d['public_update'],
                        internal_note=d['internal_note']
                    )
                    if d['status'] == 'Resolved':
                        rep.resolved_at = datetime.now(timezone.utc)
                    db.session.add(rep)
                    db.session.flush()

                    history = ReportStatusHistory(
                        report_id=rep.id,
                        admin_id=None,
                        old_status=None,
                        new_status=rep.status,
                        public_update=rep.public_update,
                        internal_note=rep.internal_note
                    )
                    db.session.add(history)

            # Sample survey responses
            demo_surveys = [
                {
                    'area_label': 'Campus Academic Zone',
                    'observed_wastage': 'Yes',
                    'categories': ['Leaking tap/pipe', 'Overflowing tank'],
                    'awareness_level': 'Moderate',
                    'rainwater_harvesting': 'Yes',
                    'suggestion': 'Place visual reminders near washbasins.'
                },
                {
                    'area_label': 'Hostel Complex',
                    'observed_wastage': 'Yes',
                    'categories': ['Overflowing tank'],
                    'awareness_level': 'High',
                    'rainwater_harvesting': 'Not sure',
                    'suggestion': 'Automated timer for overhead pump switches.'
                },
                {
                    'area_label': 'Staff Quarters',
                    'observed_wastage': 'No',
                    'categories': [],
                    'awareness_level': 'Moderate',
                    'rainwater_harvesting': 'No',
                    'suggestion': 'Periodic community plumbing inspection.'
                }
            ]

            for s in demo_surveys:
                resp = SurveyResponse(
                    area_label=s['area_label'],
                    observed_wastage=s['observed_wastage'],
                    awareness_level=s['awareness_level'],
                    rainwater_harvesting=s['rainwater_harvesting'],
                    suggestion=s['suggestion']
                )
                resp.set_categories(s['categories'])
                db.session.add(resp)

            db.session.commit()
            click.echo("Successfully seeded clearly-labelled demonstration records (3 reports, 3 survey responses).")
