"""Initialize database tables for production deployment."""
from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print("✅ All database tables created successfully!")
