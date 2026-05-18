from flask import Flask, jsonify
import time

"""
===========================================================================
LESSON 3: RESOURCE LIMITS & TIME-OUTS
===========================================================================

1. THE PROBLEM:
   What if a user sends a request that causes an infinite loop in your 
   AI model? Or what if 1,000 users send massive 1GB images?
   A single "bad" request can consume all your RAM or CPU and crash the 
   entire server for everyone else.

2. THE SOLUTION:
   - Request Timeouts: Stop any request that takes too long.
   - Size Limits: Reject any file that is too big.
   - Resource Monitoring: Watch your RAM/CPU and stop accepting new 
     work if you are at 95% capacity.

3. INDUSTRY USE CASE:
   Public APIs (like OpenAI) always have "Timeouts". If an AI model 
   doesn't answer in 60 seconds, they cut the connection to save resources.
===========================================================================
"""

app = Flask(__name__)

# ---------------------------------------------------------
# PROTECTION 1: Limit the size of incoming data (e.g., 2MB max)
# ---------------------------------------------------------
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

@app.route('/predict', methods=['POST'])
def predict():
    # ---------------------------------------------------------
    # PROTECTION 2: Manual Timeout Check
    # In production servers like Waitress/Gunicorn, you set 'timeout=30'
    # in the configuration.
    # ---------------------------------------------------------
    start_time = time.time()
    
    # Simulate an AI model that might take too long
    while True:
        # Check if we have been running for more than 5 seconds
        if time.time() - start_time > 5:
            return jsonify({
                "error": "Timeout", 
                "message": "AI model took too long to respond. Task cancelled."
            }), 504
        
        # Simulate small steps of model processing
        time.sleep(1)
        break # Exit loop for this demo
        
    return jsonify({"status": "success", "prediction": "Done"})

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        "error": "File Too Large",
        "message": "Maximum allowed size is 2MB."
    }), 413

if __name__ == "__main__":
    app.run(debug=True)
