from flask import Blueprint, render_template
from app.models import WaterReport, db

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Public home page with real database summary counts and clear CTAs."""
    total_reports = WaterReport.query.count()
    resolved_reports = WaterReport.query.filter_by(status='Resolved').count()
    in_progress_reports = WaterReport.query.filter(
        WaterReport.status.in_(['Under Review', 'In Progress'])
    ).count()

    stats = {
        'total': total_reports,
        'resolved': resolved_reports,
        'in_progress': in_progress_reports
    }
    return render_template('index.html', stats=stats)


@public_bp.route('/awareness')
def awareness():
    """Water conservation awareness and practical community guidance."""
    return render_template('awareness.html')
