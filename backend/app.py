from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from extensions import db, jwt

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres/patient_ai')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

db.init_app(app)
jwt.init_app(app)

from routes.auth import auth_bp
from routes.ai_routes import ai_bp
from routes.lab_routes import lab_bp
from routes.med_routes import meds_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(lab_bp, url_prefix='/api/lab')
app.register_blueprint(meds_bp, url_prefix='/api/meds')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "AI Patient Assistant API"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
