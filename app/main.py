import logging
from src.llm_integration import initialize_llm, analyze_codebase, format_for_report

# Mock data for testing
code_snippets = [
    {
        "code": """
import hashlib
import hmac
import os

def hash_password(password: str, salt: bytes = None) -> bytes:
    salt = salt or os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed
""",
        "description": "A function for hashing passwords using PBKDF2 with a salt."
    },
    {
        "code": """
import jwt
import datetime

def generate_token(user_id: str, secret: str, expires_in: int = 3600) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, secret, algorithm='HS256')
""",
        "description": "A function for generating JWT tokens for user authentication."
    },
    {
        "code": """
def validate_token(token: str, secret: str) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
""",
        "description": "A function for validating JWT tokens, handling expiration and invalid tokens."
    },
    {
        "code": """
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing credentials'}), 400
        # Mock user validation
        if data['username'] == 'testuser' and data['password'] == 'securepassword':
            token = generate_token('testuser', 'secret')
            return jsonify({'token': token}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
""",
        "description": "A simple Flask endpoint for user login with mock user validation and token generation."
    },
    {
        "code": """
def log_failed_attempt(username: str) -> None:
    with open('failed_attempts.log', 'a') as log_file:
        log_file.write(f"Failed login attempt for user: {username}\\n")
""",
        "description": "A function to log failed login attempts for security monitoring."
    }
]


# Mock recommendations
mock_recommendations = {
    "Debugging": "Add more contextual logging, such as request ID and user context. Use structured logging.",
    "Reliability": "Increase test coverage and add error recovery mechanisms.",
    "Security": "Move sensitive keys and secrets to environment variables or a secure vault.",
    "Minimalism": "Remove unnecessary dependencies and simplify the function design."
}

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    # Set the model type dynamically (either "smart" or "fast")
    model_type = "fast"  # You can change this to "smart" to use the smart model

    # Step 1: Initialize the LLM (using the model type from config.json)
    logging.info(f"Initializing LLM with model type: {model_type}")
    llm = initialize_llm(model_type=model_type, temperature=0.7)
    logging.info("LLM initialized successfully.")

    # Step 2: Analyze the codebase using the LLM
    logging.info("Starting code analysis...")
    analysis_results = analyze_codebase(llm, code_snippets)
    logging.info("Code analysis complete.")

    # Step 3: Format the results for the report
    logging.info("Formatting the results for the report...")
    formatted_results = format_for_report(
        llm=llm,
        analysis_results=analysis_results,
        prompts_file="app/llm/prompts.json",
        sample_report_path="app/llm/context/sample-report.md"
    )
    logging.info("Results formatted successfully.")

    # Step 4: Save the report directly as markdown
    output_path = "./compliance_report.md"
    logging.info(f"Saving the report to {output_path}...")
    with open(output_path, "w") as report_file:
        report_file.write(formatted_results)
    logging.info(f"Report saved successfully at {output_path}.")


if __name__ == "__main__":
    main()
