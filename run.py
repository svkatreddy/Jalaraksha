import os
from dotenv import load_dotenv
from app import create_app, db

# Load local environment variables from .env file if present
load_dotenv()

app = create_app()

# Auto-initialize SQLite database tables on startup if not yet created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Run locally on 127.0.0.1 (Never expose debug server publicly)
    debug_mode = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f" JalaRaksha — Water Conservation & Wastage Reporting")
    print(f" Local URL: http://127.0.0.1:{port}")
    print(f" Administrator Login: http://127.0.0.1:{port}/admin/login")
    print(f"=======================================================\n")
    app.run(host='127.0.0.1', port=port, debug=debug_mode)
