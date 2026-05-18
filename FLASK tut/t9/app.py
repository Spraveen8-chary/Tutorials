from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import functools

app = Flask(__name__)

# =========================================================================
# 1. RATE LIMITING (The "Traffic Police")
# =========================================================================
# We use 'Flask-Limiter' to prevent automated bots or hackers from 
# spamming our expensive AI models.

limiter = Limiter(
    key_func=get_remote_address,    # Tracks users by their IP Address
    app=app,
    default_limits=["200 per day"], # General safety net for the whole site
    storage_uri="memory://",         # Store hit counts in RAM (simple for tutorials)
)

# =========================================================================
# 2. SECURITY DECORATOR (The "Bouncer")
# =========================================================================
# A Decorator is a function that "wraps" another function to add security checks.

# In a real app, these would be in a database.
VALID_API_KEYS = {"sk-ai-12345", "sk-ml-67890"}

def require_api_key(original_route):
    """
    This custom bouncer checks for an 'X-API-KEY' in the request headers.
    If the key is missing or wrong, it stops the request immediately.
    """
    @functools.wraps(original_route) # Keeps the original function name for Flask
    def security_check(*args, **kwargs):
        # STEP 1: Look at the headers sent by the client
        provided_key = request.headers.get('X-API-KEY')

        # STEP 2: Validate the key
        if provided_key in VALID_API_KEYS:
            # Success! Let the request through to the real function.
            return original_route(*args, **kwargs)
        else:
            # Failure! Block the user with a 401 Unauthorized error.
            return jsonify({"error": "Unauthorized", "message": "Invalid API Key"}), 401
            
    return security_check

# =========================================================================
# 3. SECURE ROUTES
# =========================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
# Order of Security:
# 1. @limiter -> "Are you a bot spamming me?" (Max 3 per minute)
# 2. @require_api_key -> "Do you have the right key?"
# 3. predict() -> "Okay, here is your AI result."
@limiter.limit("3 per minute") 
@require_api_key
def predict():
    """This route represents a high-cost AI calculation."""
    return jsonify({
        "status": "success",
        "prediction": "Positive Sentiment Detected!",
        "security_note": "You passed both the Rate Limit and the API Key check."
    })

# CUSTOM ERROR HANDLER
# If a user hits the rate limit (3/min), Flask-Limiter triggers a 429 error.
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": f"Too many requests! Please slow down. (Limit: {e.description})"
    }), 429

if __name__ == '__main__':
    app.run(debug=True)
