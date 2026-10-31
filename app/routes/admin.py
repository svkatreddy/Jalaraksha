import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, Response, send_from_directory, current_app, abort
)
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import (
    AdminUser, WaterReport, ReportStatusHistory, SurveyResponse,
    REPORT_CATEGORIES, REPORT_STATUSES,
    SURVEY_OBSERVED_CHOICES, SURVEY_AWARENESS_CHOICES, SURVEY_RAINWATER_CHOICES,
    SURVEY_RWH_PIT_CHOICES, SURVEY_CYCLONE_IMPACT_CHOICES
)
from app.forms import AdminLoginForm, AdminReportUpdateForm
from app.utils import sanitize_csv_field

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Administrator login page with generic credential verification."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        if user and user.is_active and user.check_password(form.password.data):
            user.last_login_at = datetime.now(timezone.utc)
            db.session.commit()
            login_user(user)
            flash("Welcome back, Administrator.", "success")
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        
        # Generic error message to prevent user enumeration
        flash("Invalid username or password.", "danger")

    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Administrator logout."""
    logout_user()
    flash("You have been safely signed out.", "info")
    return redirect(url_for('admin.login'))


@admin_bp.route('')
@admin_bp.route('/')
@login_required
def dashboard():
    """Administrator dashboard with live database metrics."""
    total_reports = WaterReport.query.count()

    # Status counts
    status_counts = {}
    for st in REPORT_STATUSES:
        status_counts[st] = WaterReport.query.filter_by(status=st).count()

    # Category counts
    category_counts = {}
    for cat in REPORT_CATEGORIES:
        category_counts[cat] = WaterReport.query.filter_by(category=cat).count()

    # Top reported locations
    top_areas_query = (
        db.session.query(WaterReport.location_text, func.count(WaterReport.id).label('cnt'))
        .group_by(WaterReport.location_text)
        .order_by(func.count(WaterReport.id).desc())
        .limit(6)
        .all()
    )
    top_areas = [{'location': row[0], 'count': row[1]} for row in top_areas_query]

    # Recent reports
    recent_reports = (
        WaterReport.query
        .order_by(WaterReport.created_at.desc())
        .limit(6)
        .all()
    )

    total_surveys = SurveyResponse.query.count()

    # Climate Resilience Triage Grouping
    emergency_categories = [
        'Post-Cyclone Infrastructure Damage (Cracked mains, broken standposts)',
        'Contaminated Public Water Source (Post-storm runoff)'
    ]
    routine_categories = [
        'Everyday Leak / Wastage (Taps, Pipes, Tanks)',
        'Unnecessary Water Use / Negligence'
    ]

    emergency_count = sum(category_counts.get(c, 0) for c in emergency_categories)
    routine_count = sum(category_counts.get(c, 0) for c in routine_categories)
    other_count = category_counts.get('Other', 0)

    triage_summary = {
        'emergency_count': emergency_count,
        'routine_count': routine_count,
        'other_count': other_count,
        'emergency_pct': round((emergency_count / total_reports * 100)) if total_reports > 0 else 0,
        'routine_pct': round((routine_count / total_reports * 100)) if total_reports > 0 else 0,
        'other_pct': round((other_count / total_reports * 100)) if total_reports > 0 else 0
    }

    return render_template(
        'admin/dashboard.html',
        total_reports=total_reports,
        status_counts=status_counts,
        category_counts=category_counts,
        top_areas=top_areas,
        recent_reports=recent_reports,
        total_surveys=total_surveys,
        statuses=REPORT_STATUSES,
        categories=REPORT_CATEGORIES,
        triage_summary=triage_summary,
        emergency_categories=emergency_categories,
        routine_categories=routine_categories
    )


@admin_bp.route('/reports')
@login_required
def reports_list():
    """Searchable, filterable list of all submitted water reports."""
    query = WaterReport.query

    # Filters
    selected_status = request.args.get('status', '').strip()
    selected_category = request.args.get('category', '').strip()
    search_area = request.args.get('area', '').strip()
    date_from_str = request.args.get('date_from', '').strip()
    date_to_str = request.args.get('date_to', '').strip()

    if selected_status and selected_status in REPORT_STATUSES:
        query = query.filter(WaterReport.status == selected_status)

    if selected_category and selected_category in REPORT_CATEGORIES:
        query = query.filter(WaterReport.category == selected_category)

    if search_area:
        query = query.filter(WaterReport.location_text.ilike(f"%{search_area}%"))

    if date_from_str:
        try:
            d_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            query = query.filter(WaterReport.observed_on >= d_from)
        except ValueError:
            pass

    if date_to_str:
        try:
            d_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            query = query.filter(WaterReport.observed_on <= d_to)
        except ValueError:
            pass

    reports = query.order_by(WaterReport.created_at.desc()).all()

    return render_template(
        'admin/reports.html',
        reports=reports,
        statuses=REPORT_STATUSES,
        categories=REPORT_CATEGORIES,
        selected_status=selected_status,
        selected_category=selected_category,
        search_area=search_area,
        date_from=date_from_str,
        date_to=date_to_str
    )


@admin_bp.route('/reports/<int:report_id>', methods=['GET', 'POST'])
@login_required
def report_detail(report_id):
    report = db.session.get(WaterReport, report_id)
    if not report:
        abort(404)
    form = AdminReportUpdateForm(obj=report)

    if form.validate_on_submit():
        old_status = report.status
        new_status = form.status.data
        new_public_update = (form.public_update.data or '').strip()
        new_internal_note = (form.internal_note.data or '').strip()

        # Update report model
        report.status = new_status
        report.public_update = new_public_update or None
        report.internal_note = new_internal_note or None
        report.updated_at = datetime.now(timezone.utc)

        if new_status == 'Resolved':
            if not report.resolved_at:
                report.resolved_at = datetime.now(timezone.utc)
        else:
            report.resolved_at = None

        # Always record in status history audit trail
        history_entry = ReportStatusHistory(
            report_id=report.id,
            admin_id=current_user.id,
            old_status=old_status,
            new_status=new_status,
            public_update=new_public_update or None,
            internal_note=new_internal_note or None
        )
        db.session.add(history_entry)
        db.session.commit()

        flash(f"Report {report.reference_code} status updated to '{new_status}'.", "success")
        return redirect(url_for('admin.report_detail', report_id=report.id))

    # Pre-populate form on GET
    if request.method == 'GET':
        form.status.data = report.status
        form.public_update.data = report.public_update
        form.internal_note.data = report.internal_note

    history = report.status_history.order_by(ReportStatusHistory.created_at.desc()).all()

    return render_template('admin/report_detail.html', report=report, form=form, history=history)


@admin_bp.route('/reports/export.csv')
@login_required
def export_reports_csv():
    """
    Export reports to CSV with formula injection defense.
    Excludes sensitive internal admin notes and binary image contents.
    """
    reports = WaterReport.query.order_by(WaterReport.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Approved headers
    headers = [
        "Reference Code",
        "Category",
        "Location",
        "Observed Date",
        "Submitted Date (UTC)",
        "Status",
        "Public Update",
        "Last Updated (UTC)",
        "Resolved Date (UTC)"
    ]
    writer.writerow(headers)

    for r in reports:
        row = [
            sanitize_csv_field(r.reference_code),
            sanitize_csv_field(r.category),
            sanitize_csv_field(r.location_text),
            sanitize_csv_field(r.observed_on.strftime('%Y-%m-%d') if r.observed_on else ''),
            sanitize_csv_field(r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''),
            sanitize_csv_field(r.status),
            sanitize_csv_field(r.public_update or ''),
            sanitize_csv_field(r.updated_at.strftime('%Y-%m-%d %H:%M:%S') if r.updated_at else ''),
            sanitize_csv_field(r.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if r.resolved_at else '')
        ]
        writer.writerow(row)

    csv_data = output.getvalue()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=jalaraksha_reports_export.csv"}
    )


@admin_bp.route('/survey-results')
@login_required
def survey_results():
    """Aggregate community survey analytics."""
    responses = SurveyResponse.query.order_by(SurveyResponse.submitted_at.desc()).all()
    total_count = len(responses)

    # Distribution of observed wastage
    observed_dist = {k: 0 for k in SURVEY_OBSERVED_CHOICES}
    # Distribution of awareness level
    awareness_dist = {k: 0 for k in SURVEY_AWARENESS_CHOICES}
    # Distribution of rainwater harvesting
    rainwater_dist = {k: 0 for k in SURVEY_RAINWATER_CHOICES}
    # Distribution of functional RWH pits
    rwh_pit_dist = {k: 0 for k in SURVEY_RWH_PIT_CHOICES}
    # Distribution of Cyclone Arnab infrastructure impact
    cyclone_impact_dist = {k: 0 for k in SURVEY_CYCLONE_IMPACT_CHOICES}
    # Category occurrences
    category_counts = {k: 0 for k in REPORT_CATEGORIES}
    suggestions = []

    for r in responses:
        if r.observed_wastage in observed_dist:
            observed_dist[r.observed_wastage] += 1
        if r.awareness_level in awareness_dist:
            awareness_dist[r.awareness_level] += 1
        if r.rainwater_harvesting in rainwater_dist:
            rainwater_dist[r.rainwater_harvesting] += 1
        if r.rwh_pit in rwh_pit_dist:
            rwh_pit_dist[r.rwh_pit] += 1
        if r.cyclone_impact in cyclone_impact_dist:
            cyclone_impact_dist[r.cyclone_impact] += 1
        
        cats = r.get_categories()
        for cat in cats:
            if cat in category_counts:
                category_counts[cat] += 1

        if r.suggestion and r.suggestion.strip():
            suggestions.append({
                'date': r.submitted_at.strftime('%Y-%m-%d'),
                'area': r.area_label or 'Not specified',
                'text': r.suggestion.strip()
            })

    return render_template(
        'admin/survey_results.html',
        total_count=total_count,
        observed_dist=observed_dist,
        awareness_dist=awareness_dist,
        rainwater_dist=rainwater_dist,
        rwh_pit_dist=rwh_pit_dist,
        cyclone_impact_dist=cyclone_impact_dist,
        category_counts=category_counts,
        suggestions=suggestions
    )


@admin_bp.route('/uploads/<path:filename>')
@login_required
def view_upload(filename):
    """
    Serve uploaded photograph only to authenticated administrators.
    Rejects directory traversal and invalid paths.
    """
    upload_folder = Path(current_app.config['UPLOAD_FOLDER']).resolve()
    file_path = (upload_folder / filename).resolve()

    # Prevent path traversal outside upload directory
    if not str(file_path).startswith(str(upload_folder)):
        abort(403)
    if not file_path.exists() or not file_path.is_file():
        abort(404)

    return send_from_directory(upload_folder, filename)
