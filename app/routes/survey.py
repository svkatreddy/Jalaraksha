from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import (
    SurveyResponse, REPORT_CATEGORIES,
    SURVEY_OBSERVED_CHOICES, SURVEY_AWARENESS_CHOICES, SURVEY_RAINWATER_CHOICES,
    SURVEY_RWH_PIT_CHOICES, SURVEY_CYCLONE_IMPACT_CHOICES
)
from app.forms import SurveyForm

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/survey', methods=['GET', 'POST'])
def take_survey():
    """Anonymous community water conservation and climate resilience survey."""
    form = SurveyForm()

    if form.validate_on_submit():
        # Validate choices server-side against allowed enumerations
        if form.observed_wastage.data not in SURVEY_OBSERVED_CHOICES:
            flash("Invalid choice for observed water wastage.", "danger")
            return render_template('survey.html', form=form)

        if form.awareness_level.data not in SURVEY_AWARENESS_CHOICES:
            flash("Invalid choice for awareness rating.", "danger")
            return render_template('survey.html', form=form)

        if form.rainwater_harvesting.data not in SURVEY_RAINWATER_CHOICES:
            flash("Invalid choice for rainwater harvesting.", "danger")
            return render_template('survey.html', form=form)

        if form.rwh_pit.data not in SURVEY_RWH_PIT_CHOICES:
            flash("Invalid choice for rainwater harvesting pit question.", "danger")
            return render_template('survey.html', form=form)

        if form.cyclone_impact.data not in SURVEY_CYCLONE_IMPACT_CHOICES:
            flash("Invalid choice for cyclone impact question.", "danger")
            return render_template('survey.html', form=form)

        # Sanitize categories: only keep valid ones
        selected_categories = [
            cat for cat in (form.observed_categories.data or [])
            if cat in REPORT_CATEGORIES
        ]

        response = SurveyResponse(
            area_label=form.area_label.data.strip() if form.area_label.data else None,
            observed_wastage=form.observed_wastage.data,
            awareness_level=form.awareness_level.data,
            rainwater_harvesting=form.rainwater_harvesting.data,
            rwh_pit=form.rwh_pit.data,
            cyclone_impact=form.cyclone_impact.data,
            suggestion=form.suggestion.data.strip() if form.suggestion.data else None
        )
        response.set_categories(selected_categories)

        db.session.add(response)
        db.session.commit()

        return redirect(url_for('survey.survey_thanks'))

    return render_template('survey.html', form=form)


@survey_bp.route('/survey/thanks')
def survey_thanks():
    """Community survey thank you page."""
    return render_template('survey_thanks.html')
