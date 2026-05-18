from flask import Flask, request, jsonify, render_template
from celery import Celery
import time
import random

# =========================================================================
# 1. FLASK AND CELERY SETUP
# =========================================================================

app = Flask(__name__)
# Redis is also used foe cache memory
# Celery needs a "Broker" to send messages and a "Backend" to store results.
# We use Redis for both. 
# Think of Redis as a "Post Office" where Flask drops off tasks, 
# and Celery workers pick them up to process them.
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery and link it with the Flask configuration
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# =========================================================================
# 2. BACKGROUND TASK DEFINITION (The Worker's Job)
# =========================================================================

# The @celery.task decorator tells Celery "this function can run in the background".
# 'bind=True' gives us access to 'self', allowing us to update the task's progress.
@celery.task(bind=True)
def heavy_ml_task(self, model_name):
    """
    Simulates a heavy AI/ML task (like training a model or generating an image).
    This function runs in a SEPARATE process from the Flask app.
    """
    print(f"Starting heavy background task for model: {model_name}")
    
    total_steps = 10
    for i in range(total_steps):
        # We update the 'state' to 'PROGRESS' and store metadata.
        # This allows the Flask app to tell the user "X% complete".
        self.update_state(state='PROGRESS',
                          meta={'current': i + 1, 'total': total_steps,
                                'status': f'Processing step {i+1} of 10...'})
        
        # Simulate heavy work (e.g., matrix multiplication or data cleaning)
        time.sleep(random.uniform(1, 2))
    
    # The return value is stored in the 'Backend' (Redis) for the app to retrieve later.
    return {'current': 10, 'total': 10, 'status': 'Task completed!',
            'result': f'Final prediction for {model_name}: SUCCESS'}

# =========================================================================
# 3. FLASK ROUTES (The User Interface)
# =========================================================================

@app.route('/')
def index():
    """Serves the dashboard where the user can click 'Run Model'."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """
    Starts the background task. 
    It returns a 'Task ID' immediately so the user isn't kept waiting.
    """
    model_name = request.json.get('model', 'DefaultModel')
    
    # '.delay()' tells Celery to run this function in the background.
    # It does NOT wait for the function to finish.
    task = heavy_ml_task.delay(model_name)
    
    # Return the unique ID for this specific task
    return jsonify({'task_id': task.id}), 202

@app.route('/status/<task_id>')
def task_status(task_id):
    """
    Checks the status of a specific task using its unique ID.
    The browser calls this every second (polling) to show the progress bar.
    """
    # Ask Celery for the result of the task with this ID
    task = heavy_ml_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        # Task is waiting in the queue
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        # Task is either in PROGRESS or SUCCESS
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        # If finished, add the final result to the response
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # Something went wrong (the function crashed)
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info), # The error message
        }
    return jsonify(response)

if __name__ == '__main__':
    # Note: To run this properly, you also need to start a Celery worker:
    # celery -A app.celery worker --loglevel=info
    app.run(debug=True)
