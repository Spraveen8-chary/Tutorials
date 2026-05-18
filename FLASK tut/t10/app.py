import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
# The secret_key is required for 'flashing' (showing success/error popups)
app.secret_key = "supersecretkey" 

# =========================================================================
# 1. FILE UPLOAD CONFIGURATION
# =========================================================================

# Define where files go. We use os.path.join to make it work on Windows and Mac.
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SECURITY: Limit file size to 16MB. 
# This prevents hackers from crashing the server by uploading 100GB files.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Make sure the 'uploads' folder actually exists on the computer
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has a safe extension (e.g. .jpg and not .exe)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================================================================
# 2. ROUTES
# =========================================================================

@app.route('/')
def index():
    # List all files currently in the uploads folder to show them on screen
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Step 1: Did the browser even send a file?
    if 'file' not in request.files:
        flash('No file part in the request')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Step 2: Did the user select a file? (Empty filename means they clicked 'submit' with nothing)
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # Step 3: Validate and Save
    if file and allowed_file(file.filename):
        # SECURITY: 'secure_filename' is CRITICAL. 
        # It removes characters like '../' which hackers use to try and 
        # overwrite your system files (Path Traversal Attack).
        filename = secure_filename(file.filename)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 'flash' sends a message to the next page the user sees
        flash(f'File "{filename}" successfully uploaded!')
        return redirect(url_for('index'))
    else:
        flash('File type not allowed! Safe types: images, PDF, CSV.')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    This route serves the uploaded files.
    Without this, you could upload files but never see or download them.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
