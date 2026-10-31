from datetime import date, timedelta
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, SelectMultipleField,
    DateField, PasswordField, SubmitField, widgets, RadioField
)
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models import (
    REPORT_CATEGORIES, REPORT_STATUSES,
    SURVEY_OBSERVED_CHOICES, SURVEY_AWARENESS_CHOICES, SURVEY_RAINWATER_CHOICES,
    SURVEY_RWH_PIT_CHOICES, SURVEY_CYCLONE_IMPACT_CHOICES
)

class MultiCheckboxField(SelectMultipleField):
    """Multiple checkbox widget for survey multi-selection."""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ReportForm(FlaskForm):
    """Form for public water-wastage report submission."""
    category = SelectField(
        'Wastage Category',
        choices=[('', '-- Select Category --')] + [(c, c) for c in REPORT_CATEGORIES],
        validators=[DataRequired(message="Please select a category.")]
    )
    location_text = StringField(
        'General Area / Location Description',
        validators=[
            DataRequired(message="Please enter a broad location description."),
            Length(min=3, max=200, message="Location must be between 3 and 200 characters.")
        ],
        description="E.g., College Block B ground floor wash area, Main Street public tap."
    )
    observed_on = DateField(
        'Date Observed',
        validators=[DataRequired(message="Please enter the date you observed the issue.")],
        default=date.today
    )
    description = TextAreaField(
        'Incident Details',
        validators=[
            DataRequired(message="Please provide a concise description of the observation."),
            Length(min=5, max=1500, message="Description must be between 5 and 1500 characters.")
        ],
        description="Describe what you observed (e.g., continuous leak, broken valve, overflowing storage tank)."
    )
    photo = FileField(
        'Optional Photo (JPG, PNG, WebP up to 3 MB)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Only JPG, JPEG, PNG, or WebP images are allowed.')
        ]
    )
    submit = SubmitField('Submit Report')

    def validate_observed_on(self, field):
        if field.data:
            today = date.today()
            if field.data > today:
                raise ValidationError("The observed date cannot be in the future.")
            if field.data < today - timedelta(days=365):
                raise ValidationError("Observations older than one year cannot be accepted.")


class TrackReportForm(FlaskForm):
    """Form to lookup report status by reference code."""
    reference_code = StringField(
        'Report Reference Code',
        validators=[
            DataRequired(message="Please enter your report reference code."),
            Length(min=5, max=32, message="Invalid reference code format.")
        ],
        description="E.g., JR-XXXXXXXXXX"
    )
    submit = SubmitField('Track Status')


class AdminLoginForm(FlaskForm):
    """Administrator login form."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Please enter your username."),
            Length(min=3, max=80)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Please enter your password.")]
    )
    submit = SubmitField('Sign In')


class AdminReportUpdateForm(FlaskForm):
    """Form for administrator to update report status and add notes."""
    status = SelectField(
        'Report Status',
        choices=[(s, s) for s in REPORT_STATUSES],
        validators=[DataRequired(message="Please select a valid status.")]
    )
    public_update = TextAreaField(
        'Public Status Update',
        validators=[Optional(), Length(max=500, message="Public update cannot exceed 500 characters.")],
        description="Visible to the reporter on the public tracking page (e.g., 'Inspected by college maintenance team')."
    )
    internal_note = TextAreaField(
        'Internal Administrator Note',
        validators=[Optional(), Length(max=1000, message="Internal note cannot exceed 1000 characters.")],
        description="Strictly private to administrators (e.g., 'Work order #104 issued to campus plumber')."
    )
    submit = SubmitField('Update Report Status')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        # When status is Resolved, require a resolution note in public_update
        if self.status.data == 'Resolved':
            if not self.public_update.data or not self.public_update.data.strip():
                self.public_update.errors.append(
                    "When marking a report as Resolved, you must provide a public update confirming how the resolution was verified."
                )
                return False
        
        # When status is Rejected, require a reason in public_update or internal_note
        if self.status.data == 'Rejected':
            has_pub = self.public_update.data and self.public_update.data.strip()
            has_int = self.internal_note.data and self.internal_note.data.strip()
            if not (has_pub or has_int):
                self.public_update.errors.append(
                    "When rejecting a report, please provide a reason in the public update or internal note."
                )
                return False
        return True


class SurveyForm(FlaskForm):
    """Anonymous community water conservation survey form."""
    area_label = StringField(
        'Broad Area / Landmark (Optional)',
        validators=[Optional(), Length(max=150, message="Area label cannot exceed 150 characters.")],
        description="E.g., North Campus, Ward 4 Market Area (Do not enter your private home address)."
    )
    observed_wastage = RadioField(
        '1. Have you observed water wastage in your area recently?',
        choices=[(c, c) for c in SURVEY_OBSERVED_CHOICES],
        validators=[DataRequired(message="Please select an answer.")]
    )
    observed_categories = MultiCheckboxField(
        '2. Which of the following issues have you noticed? (Optional)',
        choices=[(c, c) for c in REPORT_CATEGORIES]
    )
    awareness_level = RadioField(
        '3. How would you rate your awareness of daily water-saving practices?',
        choices=[(c, c) for c in SURVEY_AWARENESS_CHOICES],
        validators=[DataRequired(message="Please select your awareness rating.")]
    )
    rainwater_harvesting = RadioField(
        '4. To your knowledge, is rainwater harvesting practiced in buildings in your community?',
        choices=[(c, c) for c in SURVEY_RAINWATER_CHOICES],
        validators=[DataRequired(message="Please select an option.")]
    )
    rwh_pit = RadioField(
        '5. Does your residence or campus have a functional Rainwater Harvesting (RWH) pit?',
        choices=[(c, c) for c in SURVEY_RWH_PIT_CHOICES],
        validators=[DataRequired(message="Please indicate whether your residence or campus has an RWH pit.")]
    )
    cyclone_impact = SelectField(
        '6. How was your local water infrastructure affected by the recent Cyclone Arnab?',
        choices=[('', '-- Select Impact Level --')] + [(c, c) for c in SURVEY_CYCLONE_IMPACT_CHOICES],
        validators=[DataRequired(message="Please select how infrastructure was affected by Cyclone Arnab.")]
    )
    suggestion = TextAreaField(
        '7. Any suggestion or comment regarding local water conservation or cyclone resilience? (Optional)',
        validators=[Optional(), Length(max=500, message="Suggestion cannot exceed 500 characters.")],
        description="Keep comments respectful and privacy-conscious (max 500 characters)."
    )
    submit = SubmitField('Submit Survey Response')
