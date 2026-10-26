# JalaRaksha (जल रक्षा)
### Community Water Conservation & Wastage Reporting System
*A Computer Science Community Service Project (CSP)*

---

## 1. Project Overview

**JalaRaksha** ("Water Protection") is a lightweight, responsive, and privacy-focused local web application designed to support genuine community fieldwork, campus water audits, and conservation awareness campaigns.

### Key Capabilities
- **Water Wastage Reporting:** Community members can document visible leaks, overflowing tanks, broken standposts, or excessive water use without creating an account.
- **Privacy-Preserving Public Tracking:** Submissions generate a cryptographically random reference code (`JR-XXXXXXXXXX`). Visitors track status without exposing private descriptions, photos, or personal data.
- **Secure Administrator Portal:** Protected role-based admin dashboard with live database counts, CSS bar charts, status transitions, verified resolution notes, and audit trails.
- **Spreadsheet Formula-Safe CSV Export:** Authorized administrators can export report records with automated formula injection neutralization.
- **Water Conservation Awareness Hub:** Educational guidance tailored for homes, educational campuses, and community public outlets.
- **Anonymous Community Survey:** Mobile-friendly survey capturing local water awareness, observed wastage issues, and rainwater harvesting practices with aggregate administrative analytics.
- **100% Local & Free:** Built with Python, Flask, and SQLite. No paid APIs, external map keys, cloud accounts, or frontend build toolchains required.

---

## 2. Technical Stack

- **Backend:** Python 3.11+ with Flask
- **ORM & Database:** Flask-SQLAlchemy with SQLite (stored in `instance/jalaraksha.db`)
- **Authentication & Security:** Flask-Login, Flask-WTF (CSRF protection), Werkzeug password hashing
- **Frontend:** Server-rendered Jinja2 templates, clean semantic HTML5, pure Vanilla CSS (zero external CDNs required), and Vanilla JavaScript
- **Image Handling:** Secure validation and storage outside public static folders via Pillow
- **Testing:** pytest with Flask test client and isolated in-memory test database

---

## 3. Local Installation & Setup Guide (Windows PowerShell)

Follow these steps in **Windows PowerShell** to set up and run the application locally:

### Step 1: Open the Project Directory
```powershell
cd c:\Users\saika\Documents\CSP\JalaRaksha
```

### Step 2: Create a Virtual Environment
Use Python 3.11 (or newer) via the Windows Python launcher:
```powershell
py -3.11 -m venv .venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
> **PowerShell Execution Policy Note:** If PowerShell shows a script execution error (`Execution_Policies`), run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

### Step 4: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Copy the example environment file to `.env`:
```powershell
Copy-Item .env.example .env
```
*(The application includes safe local development fallbacks, but you can set a custom `SECRET_KEY` in `.env` if desired.)*

### Step 6: Initialize the SQLite Database
```powershell
python -m flask --app run.py init-db
```
This creates the database tables under `instance/jalaraksha.db`.

### Step 7: Create the Administrator Account
Run the interactive CLI command to securely create your local admin credentials:
```powershell
python -m flask --app run.py create-admin
```
You will be prompted for:
- **Administrator username:** e.g., `admin`
- **Administrator password:** enter your secure password (input hidden)

*(Alternatively, pass non-interactively for testing: `python -m flask --app run.py create-admin --username admin --password YourSecurePassword123!`)*

### Step 8: (Optional) Seed Clearly-Labelled Demonstration Data
To test dashboard graphs and sample workflows for a college presentation before conducting field observations:
```powershell
python -m flask --app run.py seed-demo-data
```
> **Fieldwork Note:** Sample records are prefixed with `[DEMO TEST RECORD]`. Real community service report submissions must come from genuine observations and survey responses collected during fieldwork.

### Step 9: Launch the Application
```powershell
python run.py
```
Open your browser and navigate to:
- **Public Portal:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Administrator Login:** [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)

---

## 4. macOS / Linux Setup Instructions

```bash
cd JalaRaksha
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
flask --app run.py init-db
flask --app run.py create-admin
python run.py
```

---

## 5. Running Automated Tests

Run the full pytest suite (19 test cases covering public routes, report validation, privacy guarantees, admin authentication, status audits, CSV formula protection, and survey analytics):

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

All tests execute against an isolated temporary in-memory database and will not overwrite your local development data.

---

## 6. Application Routes & Architecture

### Public Routes
| Route | Method | Description |
|---|---|---|
| `/` | GET | Home landing page with real database summary counts and quick action cards. |
| `/report` | GET, POST | Incident submission form with category, location, date, description, and optional photo upload. |
| `/report/success/<ref>` | GET | Confirmation page displaying the unique reference code with copy button. |
| `/track` | GET, POST | Public status tracking form by reference code. |
| `/track/<ref>` | GET | Direct public status tracking route (exposes only non-sensitive fields). |
| `/awareness` | GET | Practical water conservation guidance for home, campus, and community. |
| `/survey` | GET, POST | Anonymous community awareness survey. |
| `/survey/thanks` | GET | Confirmation page for survey participants. |

### Administrator Routes (Protected)
| Route | Method | Description |
|---|---|---|
| `/admin/login` | GET, POST | Secure administrator authentication. |
| `/admin/logout` | POST | Safe administrator sign-out. |
| `/admin` | GET | Real-time operations dashboard with live status counts and CSS distribution charts. |
| `/admin/reports` | GET | Filterable, searchable list of all water wastage reports. |
| `/admin/reports/<id>` | GET, POST | Detailed report inspection, status update form, and full status audit trail. |
| `/admin/reports/export.csv`| GET | Formula-sanitized CSV export of permitted report fields. |
| `/admin/survey-results` | GET | Aggregated community survey analytics and suggestions. |
| `/admin/uploads/<file>` | GET | Authenticated-only route to inspect private uploaded report photos. |

---

## 7. Security & Privacy Safeguards

1. **Password Security:** Administrator passwords are never stored in plaintext; Werkzeug scrypt/pbkdf2 hashing is used.
2. **CSRF Protection:** State-changing POST forms are protected via Flask-WTF tokens.
3. **Data Minimization:** Reporters do not submit names, phone numbers, or private addresses.
4. **Public Privacy Fence:** Public tracking only reveals broad area, category, submitted date, status, and public updates. Full incident descriptions, private internal notes, and photos are strictly restricted to administrators.
5. **Private Uploads:** Uploaded photos are verified with Pillow, assigned random UUID filenames, and stored under `instance/uploads/` outside the public static directory.
6. **CSV Injection Defense:** Spreadsheet formulas starting with `=`, `+`, `-`, `@` are automatically sanitized with leading single quotes.
7. **Input Validation:** Observational dates cannot be in the future, categories and survey options are validated against strict server-side enumerations.

---

## 8. Resetting the Local Database

To reset the database back to a clean state:
```powershell
# Stop the running app (Ctrl + C)
Remove-Item instance\jalaraksha.db -Force
python -m flask --app run.py init-db
python -m flask --app run.py create-admin
```

---

## 9. College Presentation Demonstration Workflow

1. **Home Page (`/`):** Demonstrate the responsive interface, brand identity, and live database counts.
2. **Conservation Guidance (`/awareness`):** Review everyday water-saving practices for homes, institutions, and communities.
3. **Submit Report (`/report`):** Submit a sample incident (e.g., leaking tap in campus block). Show validation error handling if a future date is chosen.
4. **Copy Reference Code (`/report/success/<ref>`):** Copy the newly generated reference code.
5. **Track Status (`/track`):** Show the public tracking view displaying `Submitted` status and broad location only.
6. **Administrator Portal (`/admin/login`):** Log in with admin credentials. Show the live metrics dashboard.
7. **Update Report (`/admin/reports/<id>`):** Change status to `Under Review` or `In Progress`, add a public update note, and review the audit history timeline.
8. **Verify Public Update (`/track/<ref>`):** Revisit public tracking to demonstrate how updates are safely communicated to the reporter.
9. **Survey Analytics (`/admin/survey-results`):** Display real aggregated distribution charts from survey submissions.
10. **CSV Export (`/admin/reports/export.csv`):** Download report data for academic analysis.
