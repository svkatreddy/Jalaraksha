from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import WaterReport, ReportStatusHistory
from app.forms import ReportForm, TrackReportForm
from app.utils import generate_reference_code, save_uploaded_photo

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/report', methods=['GET', 'POST'])
def new_report():
    """Submit a new water-wastage report."""
    form = ReportForm()

    if form.validate_on_submit():
        # Handle optional photo upload safely
        photo_filename = None
        if form.photo.data:
            photo_filename = save_uploaded_photo(form.photo.data)
            if not photo_filename and form.photo.data.filename:
                flash("Uploaded image was invalid or unsupported. The report was submitted without an image.", "warning")

        # Generate unique secure random reference code
        reference_code = generate_reference_code()

        report = WaterReport(
            reference_code=reference_code,
            category=form.category.data,
            location_text=form.location_text.data.strip(),
            description=form.description.data.strip(),
            observed_on=form.observed_on.data,
            image_filename=photo_filename,
            status='Submitted',
            public_update='Report received and queued for review.',
            internal_note=None
        )
        db.session.add(report)
        db.session.flush()  # assign report.id

        # Log initial creation in status history
        history = ReportStatusHistory(
            report_id=report.id,
            admin_id=None,
            old_status=None,
            new_status='Submitted',
            public_update='Report received and queued for review.',
            internal_note='Initial community submission.'
        )
        db.session.add(history)
        db.session.commit()

        flash("Your water wastage report has been successfully submitted!", "success")
        return redirect(url_for('reports.report_success', reference_code=reference_code))

    return render_template('report_new.html', form=form)


@reports_bp.route('/report/success/<reference_code>')
def report_success(reference_code):
    """Display confirmation page with the newly generated reference code."""
    clean_code = reference_code.strip().upper()
    report = WaterReport.query.filter_by(reference_code=clean_code).first_or_404()
    return render_template('report_success.html', reference_code=report.reference_code)


@reports_bp.route('/track', methods=['GET', 'POST'])
@reports_bp.route('/track/<reference_code>', methods=['GET'])
def track_report(reference_code=None):
    """
    Public report status tracking.
    Enforces privacy by displaying only broad location, category, status, and public updates.
    Never exposes internal notes, descriptions, or private image paths.
    """
    form = TrackReportForm()
    searched = False
    report = None
    not_found = False

    # Extract search code from route param, query arg, or POST form
    lookup_code = None
    if reference_code:
        lookup_code = reference_code
    elif request.method == 'GET' and request.args.get('code'):
        lookup_code = request.args.get('code')
        form.reference_code.data = lookup_code
    elif form.validate_on_submit():
        lookup_code = form.reference_code.data

    if lookup_code:
        searched = True
        normalized = lookup_code.strip().upper()
        report = WaterReport.query.filter_by(reference_code=normalized).first()
        if not report:
            not_found = True

    return render_template(
        'track_report.html',
        form=form,
        searched=searched,
        report=report,
        not_found=not_found
    )
