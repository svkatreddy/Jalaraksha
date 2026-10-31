from datetime import datetime, timezone
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

# Allowed Categories & Statuses
REPORT_CATEGORIES = [
    'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
    'Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)',
    'Contaminated Public Water Source (Post-storm runoff)',
    'Unnecessary Water Use / Negligence',
    'Other'
]

REPORT_STATUSES = [
    'Submitted',
    'Under Review',
    'In Progress',
    'Resolved',
    'Rejected'
]

SURVEY_OBSERVED_CHOICES = ['Yes', 'No', 'Not sure']
SURVEY_AWARENESS_CHOICES = ['Low', 'Moderate', 'High']
SURVEY_RAINWATER_CHOICES = ['Yes', 'No', 'Not sure']
SURVEY_RWH_PIT_CHOICES = ['Yes', 'No', "Don't Know"]
SURVEY_CYCLONE_IMPACT_CHOICES = [
    'No damage',
    'Minor leaks',
    'Major pipe bursts',
    'Water contamination'
]


class AdminUser(UserMixin, db.Model):
    """Administrator user model with hashed credentials."""
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)

    status_histories = db.relationship('ReportStatusHistory', backref='admin', lazy='dynamic')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<AdminUser {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))


class WaterReport(db.Model):
    """Water wastage incident report submitted by community members."""
    __tablename__ = 'water_reports'

    id = db.Column(db.Integer, primary_key=True)
    # Cryptographically random reference code for public status tracking
    reference_code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    category = db.Column(db.String(128), nullable=False, index=True)
    location_text = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    observed_on = db.Column(db.Date, nullable=False)
    
    # Optional private image stored outside static/
    image_filename = db.Column(db.String(128), nullable=True)
    
    status = db.Column(db.String(32), default='Submitted', nullable=False, index=True)
    public_update = db.Column(db.Text, nullable=True)
    internal_note = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)

    status_history = db.relationship(
        'ReportStatusHistory',
        backref='report',
        cascade='all, delete-orphan',
        order_by='ReportStatusHistory.created_at.desc()',
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<WaterReport {self.reference_code} [{self.status}]>"


class ReportStatusHistory(db.Model):
    """Audit history of report status transitions and notes."""
    __tablename__ = 'report_status_history'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('water_reports.id'), nullable=False, index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)
    old_status = db.Column(db.String(32), nullable=True)
    new_status = db.Column(db.String(32), nullable=False)
    public_update = db.Column(db.Text, nullable=True)
    internal_note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<ReportStatusHistory report={self.report_id} {self.old_status}->{self.new_status}>"


class SurveyResponse(db.Model):
    """Anonymous community water conservation survey response."""
    __tablename__ = 'survey_responses'

    id = db.Column(db.Integer, primary_key=True)
    area_label = db.Column(db.String(150), nullable=True)
    observed_wastage = db.Column(db.String(16), nullable=False)
    # Stored as serialized JSON list of category strings
    observed_categories = db.Column(db.Text, default='[]', nullable=False)
    awareness_level = db.Column(db.String(16), nullable=False)
    rainwater_harvesting = db.Column(db.String(16), nullable=False)
    rwh_pit = db.Column(db.String(32), nullable=True)
    cyclone_impact = db.Column(db.String(64), nullable=True)
    suggestion = db.Column(db.String(500), nullable=True)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def get_categories(self):
        try:
            return json.loads(self.observed_categories or '[]')
        except (ValueError, TypeError):
            return []

    def set_categories(self, categories_list):
        self.observed_categories = json.dumps(categories_list)

    def __repr__(self):
        return f"<SurveyResponse #{self.id} on {self.submitted_at.strftime('%Y-%m-%d')}>"
