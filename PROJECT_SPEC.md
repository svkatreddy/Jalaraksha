# JalaRaksha — Complete Project Build Specification

**Purpose:** Attach this document to Antigravity as the source of truth for building the JalaRaksha application.  
**Project type:** Computer Science Community Service Project  
**Version:** 1.0  
**Target:** A complete, locally runnable Python web application suitable for a college demonstration and community fieldwork.  
**Required stack:** Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript.

---

# 0. Instructions to the Antigravity Coding Agent

Treat this document as the authoritative product and implementation specification. **Build the working application in the currently opened workspace; do not only return advice, sample snippets, or a plan.**

1. First inspect the workspace. If it already contains a project, understand its structure before editing. If it is empty, create the project structure described below.
2. Implement the Minimum Viable Product end-to-end. Prefer a stable, easy-to-explain application over unnecessary complexity.
3. Use the required stack: Python + Flask + SQLite + server-rendered Jinja templates + HTML/CSS/vanilla JavaScript. Do not replace it with Java, Spring Boot, React, Node.js, a cloud database, or a paid service.
4. The app must run locally without API keys, external services, real SMS, WhatsApp integration, map keys, IoT hardware, or internet access after dependencies are installed. External fonts or JavaScript libraries must not be required for core operation.
5. Implement the actual database models, forms, routes, authorization, validation, dashboard calculations, and tests. Do not use buttons that do nothing or display hard-coded dashboard numbers as if they were real.
6. Provide a safe local setup process, including a documented way to create the first administrator. Never commit a real password or secret key.
7. If there is a trade-off, prioritize in this order: application starts; reporting works; admin authentication and report management work; report tracking works; awareness and survey pages work; dashboard and CSV export work; visual polish.
8. Use sample/demo data only when explicitly created by a command or clearly labelled as demo data. Never present seeded examples as real community survey findings or real water savings.
9. After implementation, run the application checks and tests available in the environment. Fix failures. In the final response, accurately list what was built, how to run it, the test results, and anything that remains incomplete. Do not claim a test passed if it was not run.
10. Keep this specification in the project as `PROJECT_SPEC.md`, and create a practical `README.md` with installation, startup, database/admin setup, testing, and troubleshooting instructions.

# 1. Product Summary

## 1.1 Product name

**JalaRaksha — Community Water Conservation and Wastage Reporting System**

“JalaRaksha” means water protection. The product is a small community-focused web application that helps people learn about water conservation, record visible water wastage, track the status of reports, and document community survey findings.

## 1.2 Problem

Water-related issues such as leaking taps, overflowing tanks, damaged public outlets, and unnecessary water use may be observed by community members. People may not have a simple, organized way to document these observations or know whether a reported problem has been reviewed. Awareness of practical water-conservation measures may also be limited.

The project must **investigate the actual conditions of a selected community** rather than assume every listed issue exists. The application supports reporting and documentation; it does not itself repair infrastructure, measure water flow, or guarantee water savings.

## 1.3 Proposed solution

JalaRaksha provides:

- A public landing page explaining the project.
- A water-wastage reporting form.
- A private reference code to check a submitted report’s status.
- Water conservation tips and practical guidance.
- An anonymous, short community awareness survey.
- An administrator dashboard for reviewing reports and survey summaries.
- Status updates, resolution notes, filtering, and CSV export.

## 1.4 Main outcome

A demonstrable local web app that can support genuine community service activities: observe issues, record reports, conduct an awareness activity, record survey responses, and report results honestly.

# 2. Goals, Non-Goals, and Success Measures

## 2.1 Goals

1. Make it simple for a community member to submit a water-wastage observation.
2. Store and retrieve reports reliably using SQLite.
3. Allow an authorized administrator to review reports and update their status.
4. Provide accessible water conservation information.
5. Support a concise, privacy-conscious community survey.
6. Show dashboard statistics based on actual records in the database.
7. Make the project easy to install, demonstrate, test, and explain in a college presentation.

## 2.2 Non-goals for version 1

Do not implement the following in the MVP:

- IoT sensors, automatic leak detection, smart valves, or pump controls.
- Real SMS, WhatsApp, email, or push notifications.
- Real-time maps, GPS tracking, or paid third-party APIs.
- AI/ML prediction or automatically generated water-saving claims.
- Public user accounts or social networking features.
- Online payments or integrations with municipal systems.
- Automatic claims that a report has been fixed without administrator verification.

## 2.3 Success measures

Measure system activity from saved records:

- Number of reports submitted.
- Number of reports by category and status.
- Number of reports marked resolved after verification.
- Number of valid survey responses.
- Distribution of survey answers about observed wastage and conservation awareness.
- Number of community members engaged in real awareness activities, recorded by the student team.

The application must not claim a number of litres saved unless the team has reliable measurements and documents its method. More reports do not automatically mean more or less water wastage.

# 3. Users and Permissions

## 3.1 Public visitor / community member

Can:

- View home and awareness pages.
- Submit a water-wastage report without creating an account.
- Receive a random report reference code after submission.
- Check report status using the reference code.
- Submit an optional anonymous survey response.

Cannot:

- View the full list of community reports.
- View internal administrator notes.
- View uploaded photographs belonging to other reports.
- Change a report status or access admin pages.

## 3.2 Administrator

Can:

- Log in and log out.
- View summary dashboard statistics.
- View, filter, search, and open report records.
- Update a report’s status.
- Add an internal note and a separate public update.
- View an uploaded image through an authorized route.
- Review aggregate survey results.
- Export permitted report data to CSV.

Cannot:

- See stored passwords in plain text (passwords must only be hashed).
- Export password hashes or unnecessary secrets.

## 3.3 Student project team

Uses the application for the community service activity, records actual field observations with permission, conducts the awareness survey, verifies issue outcomes where possible, and uses genuine application data for the final report.

# 4. Functional Scope and Priority

**P0 = required for submission. P1 = important after the core works. P2 = optional enhancement.**

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Responsive home page and navigation | P0 |
| FR-02 | Submit water-wastage report and generate reference code | P0 |
| FR-03 | Administrator login/logout and route protection | P0 |
| FR-04 | Admin report list, detail, and status update | P0 |
| FR-05 | Public report status tracking by reference code | P0 |
| FR-06 | Water conservation awareness page | P0 |
| FR-07 | SQLite persistence and safe database initialization | P0 |
| FR-08 | Admin dashboard with live database counts | P0 |
| FR-09 | Community survey form and database persistence | P1 |
| FR-10 | Aggregate survey results on admin dashboard | P1 |
| FR-11 | Filter reports by status/category/area/date | P1 |
| FR-12 | CSV export for authorized admin | P1 |
| FR-13 | Optional image upload for a report | P1 |
| FR-14 | Report status history | P1 |
| FR-15 | Demo data command clearly labelled as test data | P2 |

The coding agent should complete all P0 requirements and implement P1 requirements if the P0 functionality is stable. Do not sacrifice working core features to implement optional enhancements.

# 5. Detailed Functional Requirements

## FR-01 — Home page

The home page must contain:

- Brand/title: JalaRaksha.
- Tagline: “Small actions. Responsible water use. Stronger communities.”
- Brief description of the problem and solution.
- Primary call-to-action: “Report Water Wastage”.
- Secondary action: “Track a Report”.
- Link to “Water Conservation”.
- Link to “Community Survey”.
- A small statistics area populated from the database; if there are no records, show an honest empty state such as “No community reports have been submitted yet.”
- Footer with project purpose and a note that the application is an educational community-service prototype.

Do not put made-up impact figures in the hero section.

## FR-02 — Water-wastage report form

Required fields:

- **Category:** one of `Leaking tap/pipe`, `Overflowing tank`, `Damaged public water outlet`, `Unnecessary water use`, or `Other`.
- **Area/location:** a short plain-text description, e.g. “College Block B, ground-floor wash area”. Avoid asking for exact home addresses.
- **Date observed:** date field; it must not be in the future.
- **Description:** concise details of what was observed; apply a sensible maximum length.

Optional field:

- **Photograph:** JPG, JPEG, PNG, or WebP only; size limit 3 MB. Reject SVG and executable/document formats. Generate a random server-side filename and never trust an uploaded filename. Store uploads outside the public static folder. Only a signed-in administrator may view an uploaded image.

On a valid submission:

1. Validate input on the server.
2. Create a report record with a cryptographically random, non-sequential reference code, such as `JR-` plus 10 uppercase letters/digits.
3. Avoid collisions by checking uniqueness and retrying if necessary.
4. Set status to `Submitted`.
5. Save creation and update timestamps.
6. Show a success page with the reference code and a clear instruction to save it. Do not expose the full report list.

The reference code is effectively a bearer token for status lookup. Generate it with a secure random generator, avoid predictable IDs, and do not include contact details in public tracking.

## FR-03 — Administrator authentication

- Admin login uses username and password.
- Store a password hash using Werkzeug’s password hashing utilities or an equivalent secure method.
- Use Flask-Login or an equally clear session mechanism.
- Protect every `/admin` route server-side, not just by hiding links in the UI.
- Include CSRF protection for state-changing forms (Flask-WTF or equivalent).
- Show generic login failure messages that do not disclose whether a username exists.
- Provide a logout route using POST where practical.
- Create the first administrator through a documented CLI command that prompts for username/password, or another secure setup flow.
- Do not hard-code a real admin password in source code or commit one to Git.

## FR-04 — Admin report management

The admin report list must show reference code, category, area, date observed, submitted date, and status. Include pagination or a reasonable page-size limit if needed.

An admin must be able to open a report detail page and update the status to one of:

- `Submitted`
- `Under Review`
- `In Progress`
- `Resolved`
- `Rejected`

When choosing `Resolved`, the admin must enter or confirm a resolution note describing how the outcome was verified. When choosing `Rejected`, a reason is required. Save the status update, timestamp, and status-history record.

Support two distinct note fields:

- **Public update:** short text safe to display on the report-tracking page.
- **Internal admin note:** private operational note visible only to administrators.

Never expose internal notes through public routes. A report must only be marked resolved when the responsible team has verified it; submission of a report does not itself mean a repair was completed.

## FR-05 — Public report tracking

- The visitor enters their reference code.
- Normalize surrounding whitespace and uppercase the code before lookup.
- Display only the minimum necessary fields: reference code, category, broad location text, date submitted, current status, latest public update, and last-updated timestamp.
- Do not display the original detailed description, uploaded photo, reporter identity, or internal note on public tracking.
- For a nonexistent code, display a neutral “No report found for that reference code” message.
- Ensure the lookup route does not permit enumeration of sequential numeric IDs.

## FR-06 — Water-conservation awareness page

Include plain-language, practical advice organized into sections:

**At home**
- Turn off taps when water is not needed.
- Repair leaking taps and pipes promptly.
- Use water efficiently during cleaning and washing.
- Reuse suitable non-contaminated household water for appropriate non-drinking purposes when safe.

**At school/college**
- Report leaking taps and overflowing storage tanks.
- Avoid unnecessary water use in washrooms and shared facilities.
- Place conservation reminders where water is used.
- Encourage students and staff to take part in conservation activities.

**In the community**
- Report damaged public outlets through the appropriate responsible authority.
- Promote rainwater harvesting only where suitable and properly designed.
- Keep drainage paths and rainwater collection areas clear where appropriate.
- Avoid claiming that every water reuse practice is safe for drinking.

Include a short “How to take part” section directing users to the report form and survey. Content must be editable in templates or a simple content module without changing business logic.

## FR-07 — Database persistence

Use SQLite for local development. Create the database in the Flask `instance/` directory (or another clearly documented local-data directory), not in an unpredictable current working directory. Database initialization must be documented.

Use Flask-SQLAlchemy or Python’s SQLite interface consistently. SQLAlchemy is preferred for clear models and testing.

## FR-08 — Admin dashboard

Show live metrics calculated from the database:

- Total reports.
- Reports in `Submitted` status.
- Reports in `Under Review` status.
- Reports in `In Progress` status.
- Reports in `Resolved` status.
- Reports in `Rejected` status.
- Counts by category.
- Counts by area (top areas only, with long labels truncated visually if required).
- Recent reports table.

If the database is empty, show zero counts and a friendly empty state. Graphs may use CSS bar charts or small locally implemented JavaScript charts; do not require an external CDN for the dashboard to function.

## FR-09 — Community survey

The survey must be brief and usable on mobile. Make the survey anonymous by default and do not ask for names, phone numbers, or exact addresses.

Suggested fields:

1. Broad area/landmark (optional; do not ask for a home address).
2. Have you observed water wastage in your area? (`Yes`, `No`, `Not sure`).
3. Which issue have you observed? Multi-select categories; optional if the answer above is No/Not sure.
4. How would you rate your awareness of water-conservation practices? (`Low`, `Moderate`, `High`).
5. Is rainwater harvesting used in a place you know? (`Yes`, `No`, `Not sure`).
6. Optional suggestion (length-limited).

Validate all choices server-side. Present a short privacy note before submission. Store the response and submission timestamp. Avoid duplicate submissions by aggressive tracking or invasive fingerprinting; simple validation and basic rate limiting are enough for the prototype.

## FR-10 — Survey results

Admin-only aggregate view:

- Total valid responses.
- Distribution of water-wastage observations.
- Distribution of awareness ratings.
- Reported issue categories.
- Rainwater harvesting responses.

The system must not present a tiny or unrepresentative sample as representative of the whole population. In the project report, show the actual sample size and dates of collection.

## FR-11 — Filters and search

On the admin reports page, support filters by status, category, area text, and date range. Filters must be combined correctly. Provide a “Clear filters” action. If no results match, display an empty-result message.

## FR-12 — CSV export

Admin-only CSV export for reports. Include reference code, category, area, observed date, submitted date, status, public update, and updated date. Exclude admin password hashes, internal notes, uploaded binary content, and any secrets. Use safe CSV serialization and handle values beginning with formula characters (`=`, `+`, `-`, `@`) so spreadsheet software does not execute user-supplied content as a formula.

## FR-13 — Image handling

This is P1 and can be omitted if it threatens core reliability. If implemented:

- Max size 3 MB.
- Allowed formats: JPG/JPEG, PNG, WebP.
- Validate extension and detected image content as far as practical.
- Generate a random filename.
- Store under `instance/uploads/` outside the public static directory.
- Restrict image viewing to authenticated administrators.
- Do not expose upload filesystem paths to users.
- Handle missing/deleted files gracefully.

## FR-14 — Status history

For every status change, store report ID, old status, new status, admin ID, note, and timestamp. This is preferred for accountability. If the history table is not implemented in the first iteration, at least persist `updated_at`, status, and resolution note, but clearly report the omission.

# 6. UI/UX and Visual Design

## 6.1 Design direction

Use a calm, clean environmental theme. Avoid excessive gradients, neon colours, busy animations, and generic “AI dashboard” styling. Make the interface look appropriate for a community initiative and college demonstration.

Suggested palette:

- Deep teal: `#155E75`
- Primary teal: `#0E7490`
- Water tint: `#ECFEFF`
- Soft background: `#F8FAFC`
- Leaf green accent: `#15803D`
- Main text: `#0F172A`
- Muted text: `#475569`
- Border: `#CBD5E1`
- Success: `#166534`
- Warning: `#92400E`
- Error: `#B91C1C`

Use semantic colours and ensure contrast. A small droplet/leaf symbol may be used as a simple icon or inline SVG created by the developer; do not depend on an icon library CDN.

## 6.2 Layout requirements

- Shared navigation/header and footer.
- Consistent page width and spacing.
- Responsive layout for common phone, tablet, and desktop widths.
- Clear form labels and error messages.
- Buttons with hover and keyboard focus states.
- Tables that remain readable on narrow screens, using horizontal scrolling or stacked cards where appropriate.
- Status badges for each report status.
- Empty states and success/error flash messages.
- No dead controls, placeholder links, Lorem Ipsum, or visual elements that imply a feature exists when it does not.

## 6.3 Accessibility

Use semantic headings in order, associated form labels, keyboard-accessible controls, sufficient contrast, meaningful button text, and alt text for meaningful images. Do not use colour as the only way to communicate report status.

# 7. Technical Architecture

## 7.1 Stack

- Python 3.11 or a compatible newer version.
- Flask.
- Flask-SQLAlchemy.
- Flask-Login.
- Flask-WTF for CSRF protection, or a clearly documented equivalent.
- python-dotenv for environment configuration.
- Werkzeug utilities for password hashing and safe file handling.
- SQLite.
- Jinja2 templates.
- HTML5, CSS3, vanilla JavaScript.
- pytest for automated tests.

Keep dependencies limited to what is needed. Do not add a large frontend build toolchain.

## 7.2 Recommended project structure

```text
jalaraksha/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py
│   │   ├── reports.py
│   │   ├── survey.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── report_new.html
│   │   ├── report_success.html
│   │   ├── track_report.html
│   │   ├── awareness.html
│   │   ├── survey.html
│   │   ├── survey_thanks.html
│   │   ├── errors/
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── admin/
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── reports.html
│   │       ├── report_detail.html
│   │       └── survey_results.html
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/ (only local, non-sensitive assets)
├── instance/ (database and private uploads; do not commit user data)
├── tests/
│   ├── conftest.py
│   ├── test_public_pages.py
│   ├── test_reports.py
│   ├── test_admin.py
│   └── test_survey.py
├── .env.example
├── .gitignore
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── PROJECT_SPEC.md
```

The agent may make small structural changes if they improve maintainability, but keep the project easy for a beginner to understand and start.

## 7.3 Application configuration

Use configuration values from environment variables where appropriate:

- `SECRET_KEY` for Flask sessions and CSRF.
- `DATABASE_URL` optional; default to SQLite in `instance/jalaraksha.db`.
- `UPLOAD_FOLDER` default to a private folder under `instance/`.
- `MAX_CONTENT_LENGTH` default to 3 MB if image uploads are enabled.
- `FLASK_ENV` or a clear `DEBUG` setting, if used.

Create `.env.example` with placeholders only. Add `.env`, local databases, private uploads, Python virtual environments, caches, and test artefacts to `.gitignore`.

Do not use a weak constant secret in production. Document that a strong local secret should be set in `.env`; a development fallback may be used only in explicitly local development mode and must be called out in the README.

## 7.4 Routes (suggested)

Public:

- `GET /` — home page.
- `GET, POST /report` — create report.
- `GET, POST /track` — search using a reference code.
- `GET /track/<reference_code>` — optional tracking detail route; must expose only allowed public fields.
- `GET /awareness` — education page.
- `GET, POST /survey` — submit anonymous survey.

Admin:

- `GET, POST /admin/login` — login.
- `POST /admin/logout` — logout.
- `GET /admin` — dashboard.
- `GET /admin/reports` — filtered report list.
- `GET, POST /admin/reports/<int:report_id>` — report details and update.
- `GET /admin/reports/export.csv` — CSV export.
- `GET /admin/survey-results` — aggregate results.
- `GET /admin/uploads/<filename>` or a report-bound route — serve private uploaded photo only after authorization.

The exact URL design can vary, but public and admin authorization rules must remain as specified. Never use an unprotected endpoint to serve private uploads.

# 8. Data Model

Use SQLAlchemy models and relationships. Add indexes for fields used frequently in lookups, especially report reference code, status, category, and timestamps where appropriate.

## 8.1 AdminUser

- `id`: integer primary key.
- `username`: unique, required.
- `password_hash`: required.
- `is_active`: boolean, default true.
- `created_at`: timestamp.
- `last_login_at`: nullable timestamp.

## 8.2 WaterReport

- `id`: integer primary key (internal only; never use as public tracking code).
- `reference_code`: unique secure random string.
- `category`: required category string/enum.
- `location_text`: required, length-limited broad location.
- `description`: required, length-limited.
- `observed_on`: required date.
- `image_filename`: nullable private filename.
- `status`: required; default `Submitted`.
- `public_update`: nullable text.
- `internal_note`: nullable text visible only to admin.
- `created_at`: timestamp.
- `updated_at`: timestamp.
- `resolved_at`: nullable timestamp.

## 8.3 SurveyResponse

- `id`: integer primary key.
- `area_label`: nullable, broad location only.
- `observed_wastage`: required choice.
- `observed_categories`: serialized JSON or related table; use a safe consistent representation.
- `awareness_level`: required choice.
- `rainwater_harvesting`: required choice.
- `suggestion`: nullable, length-limited text.
- `submitted_at`: timestamp.

Do not ask for names, phone numbers, or precise home addresses in the default anonymous survey.

## 8.4 ReportStatusHistory

- `id`: integer primary key.
- `report_id`: foreign key to WaterReport.
- `admin_id`: foreign key to AdminUser.
- `old_status`: nullable for creation event.
- `new_status`: required.
- `public_update`: nullable text.
- `internal_note`: nullable text.
- `created_at`: timestamp.

Ensure the initial report submission and later status changes can be audited.

# 9. Validation and Business Rules

- Categories must come from the allowed list; ignore unexpected client-supplied values.
- Date observed cannot be in the future. Define and document how old a report is allowed to be; do not silently reject legitimate historical observations without a reason.
- Area and descriptions must be stripped of surrounding whitespace and length-limited.
- Empty required fields must be rejected server-side.
- Report reference codes must be cryptographically random and unique.
- Only authenticated administrators may change status or view internal notes.
- A report marked `Resolved` must have a resolution note or public update that explains the verified outcome.
- A report marked `Rejected` must have a reason.
- Every status update must write `updated_at`; if status history is implemented, it must also create a history row in the same transaction.
- Survey responses must use allowed option values, not arbitrary strings.
- Public tracking displays only the approved public fields.
- CSV export is administrator-only and must neutralize spreadsheet formula injection.
- Uploaded files are optional and never trusted based solely on their filename extension.
- Flash messages and user-facing validation errors must not reveal stack traces, SQL errors, or secret values.

# 10. Privacy and Security Requirements

This project may collect details about public locations and community observations. Apply data minimization:

- Do not collect reporter names, phone numbers, emails, or home addresses by default.
- Explain briefly why report details and survey answers are stored.
- Keep uploaded photographs private and administrator-only.
- Do not put secret keys, passwords, or personal records in source control.
- Use CSRF protection for all state-changing form submissions, including admin changes and survey/report forms where supported.
- Use secure password hashing.
- Protect admin endpoints on the server.
- Escape rendered user input through Jinja auto-escaping; avoid `|safe` for user-controlled text.
- Use SQLAlchemy parameters/ORM rather than building SQL from user input.
- Limit uploads to 3 MB; reject unknown file types; use generated names.
- Handle 403/404/500 cases with helpful pages and log technical details privately.
- Do not log passwords, CSRF tokens, secrets, or full private form payloads.
- Add basic request throttling to public report and survey submissions if it can be done reliably without overcomplicating the app; document that this is prototype-level protection.
- Set session cookie security flags appropriately for the chosen deployment mode. HTTPS-specific settings should be enabled in production, while local HTTP development must remain usable.

# 11. Error and Empty States

Implement clean, understandable states for:

- Invalid report form submission.
- Successful report submission.
- Invalid/nonexistent tracking code.
- Failed administrator login.
- Empty report list.
- No filter matches.
- Empty dashboard.
- Empty survey statistics.
- Unauthorized admin access.
- Missing uploaded image.
- Unsupported or oversized upload.
- Unexpected internal server error.

Do not expose Python tracebacks to the browser.

# 12. Testing Requirements

Use pytest and Flask’s test client. Tests should use an isolated temporary SQLite database and should not alter a real local community database.

Minimum test cases:

1. Home page returns HTTP 200.
2. Awareness page returns HTTP 200.
3. Valid report submission stores a record and shows a reference code.
4. Missing required report field is rejected.
5. Future observed date is rejected.
6. Tracking by valid reference code shows current public status.
7. Invalid reference code shows a neutral not-found message.
8. Public tracking never contains an internal admin note.
9. Admin login succeeds with a valid password and fails with an invalid password.
10. Protected admin route rejects unauthenticated visitors.
11. Admin can update report status and the update persists.
12. Resolved status requires a resolution note or verified public update.
13. Valid survey response persists.
14. Invalid survey choice is rejected.
15. Dashboard counts match database records.
16. CSV export is protected and exports only approved fields.
17. Unsupported and oversized image uploads are rejected if uploads are implemented.
18. Status history is recorded for updates if that table is implemented.

Test names and implementation details may differ, but core behaviors must be verified. Document the actual test command and results in README.

# 13. Local Setup and Usage Requirements

README must document setup for Windows PowerShell first (the main expected classroom environment) and include equivalent concise macOS/Linux notes where feasible.

Expected installation workflow:

```powershell
# 1. Open the project folder in VS Code
# 2. Create a virtual environment
py -m venv .venv

# 3. Activate it in PowerShell
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Copy .env.example to .env and set a local SECRET_KEY
# 6. Create the first administrator using the documented CLI command
# 7. Start the application
python run.py
```

The app should print or clearly document the local URL, normally `http://127.0.0.1:5000`. Use `127.0.0.1` only for local demonstration; do not expose the Flask development server to the public internet.

README must also explain:

- How the SQLite database is created.
- How to create/reset a local administrator safely.
- Where the local database and private uploads are stored.
- How to run tests.
- How to reset demo/test data without deleting the source code.
- Common PowerShell virtual-environment activation issues.
- That actual community survey results must be entered from fieldwork, not copied from sample data.

# 14. Deliverables Required from the Coding Agent

The finished workspace must contain:

1. Complete source code.
2. `requirements.txt` with minimum required dependencies.
3. `.env.example` containing placeholders only.
4. `.gitignore` that excludes secrets, runtime database, uploads, virtual environments, and caches.
5. `README.md` with accurate setup and usage instructions.
6. This file copied to `PROJECT_SPEC.md`.
7. Templates and static files for all implemented pages.
8. SQLAlchemy models and routes.
9. Admin account creation command or secure setup flow.
10. Automated tests for core functionality.
11. Useful and safe error handling.
12. Optional sample-data command, only if sample data are clearly labelled as demonstration data.
13. Final handoff summary with setup instructions, routes/features, test results, and known limitations.

# 15. Definition of Done

The project is ready for a classroom demonstration when all of the following are true:

- [ ] A clean installation can be completed from README.
- [ ] The application starts with a documented local command.
- [ ] The home, report, track, awareness, survey, and admin pages render correctly, for all features implemented as P0/P1.
- [ ] A report can be submitted and saved to SQLite.
- [ ] A reference code is generated and can be used to check status.
- [ ] Admin login works and protected routes reject public visitors.
- [ ] Admin can review reports and update their status.
- [ ] Internal notes are never exposed publicly.
- [ ] Dashboard values come from saved database records.
- [ ] Survey answers, if implemented, are stored and displayed as aggregates.
- [ ] Invalid user input is handled safely.
- [ ] Core automated tests pass, or failures are explicitly documented with causes.
- [ ] README explains how to run the project and tests.
- [ ] No real passwords, secret keys, or private community data are committed.
- [ ] No fake survey findings or unsupported water-saving claims are presented as real.
- [ ] The visual design is responsive and has no nonfunctional buttons or placeholder text.

# 16. Suggested Presentation Demonstration

Use a short, repeatable workflow for the faculty demonstration:

1. Open the JalaRaksha home page and explain the problem.
2. Show the water conservation awareness page.
3. Submit a clearly labelled demonstration report, such as a fictional example in a local test environment.
4. Copy the generated reference code and show public status tracking.
5. Log in as the administrator using credentials created during setup.
6. Open the report, change the status to `Under Review`, and add a public update.
7. Track the same report again to show the status update.
8. Show the admin dashboard and explain that its counts are calculated from database records.
9. Submit a sample survey response only in the demo/test database and show aggregate results if that feature is enabled.
10. Explain the real community survey and awareness activity separately, using only observations the team actually collected.

Do not imply the fictional demonstration record is a real water-wastage incident, or that changing the app status itself repairs the problem.

# 17. Guidance for the Final Report

The coding agent should create software documentation (README and technical notes), but must not fabricate community service results. The student team must add its actual details after fieldwork:

- Study area and dates.
- Number of participants surveyed.
- Survey method and questions used.
- Actual observations, counts, and photographs where permission was granted.
- Awareness activity performed.
- Which reports were forwarded to a responsible person/team.
- Which issues were confirmed resolved, if any.
- Limitations and recommendations.

Clearly separate:

- Features implemented in software.
- Features planned for future work.
- Demonstration/test records.
- Verified observations from real community activities.
- Estimated impact versus measured impact.

# 18. Final Build Instruction

**Begin implementation now.** Inspect the current workspace, create or update the project files, implement the MVP according to this specification, run the tests, fix defects, and finish with a clear summary of how the user can launch and demonstrate JalaRaksha. Do not stop after writing a plan. If any optional feature would threaten the working MVP, defer it and state that clearly in the final summary.
