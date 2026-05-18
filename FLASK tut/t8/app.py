from flask import Flask, render_template, Response
import time
import random

# =========================================================================
# 1. THE CORE CONCEPT: GENERATORS
# =========================================================================

app = Flask(__name__)

def generate_ai_response(prompt):
    """
    This is a Python 'Generator' (it uses 'yield' instead of 'return').
    Instead of sending the whole text at once, it yields one word at a time.
    
    In a real AI app, this is where you'd call your LLM (like GPT-4) and
    receive tokens one-by-one.
    """
    full_text = f"As an AI, I have analyzed your prompt: '{prompt}'. Here is a detailed response generated token-by-token to demonstrate streaming efficiency. Streaming is better than waiting for the whole response because the user sees progress immediately!"
    
    words = full_text.split()
    
    for word in words:
        # We yield each word formatted as a 'Server-Sent Event' (SSE).
        # Standard format: "data: YOUR_CONTENT \n\n"
        # The two newlines (\n\n) tell the browser "this message is finished".
        yield f"data: {word} \n\n"
        
        # We simulate the AI "thinking" or "generating" by sleeping briefly.
        time.sleep(random.uniform(0.1, 0.4))

# =========================================================================
# 2. FLASK ROUTES
# =========================================================================

@app.route('/')
def index():
    """Serves the main chat-like interface."""
    return render_template('index.html')

@app.route('/stream')
def stream():
    """
    The endpoint that returns a 'Streaming Response'.
    
    1. We call our generator function.
    2. We wrap it in a Flask 'Response' object.
    3. We set mimetype='text/event-stream'. This is the standard for 
       keeping the connection open so the server can "push" words.
    """
    prompt = "Tell me about Web Streaming"
    
    # Return the special Response object initialized with our generator
    return Response(generate_ai_response(prompt), mimetype='text/event-stream')

if __name__ == '__main__':
    for i in generate_ai_response("Hello, world!"):
        print(i, end='', flush=True)
    app.run(debug=True)
