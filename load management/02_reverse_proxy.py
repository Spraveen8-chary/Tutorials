"""
===========================================================================
LESSON 2: THE REVERSE PROXY (Nginx Concept)
===========================================================================

1. THE PROBLEM:
   Python is great at logic, but it is SLOW at sending files (Images, CSS, 
   JS). If 100 people download a 5MB image from your Flask app, your 
   Python process will be too busy "sending bits" to handle AI logic.

2. THE SOLUTION:
   A Reverse Proxy like **Nginx** or **Apache**.
   Nginx is a "Traffic Controller". It sits in front of Flask.
   - If a user asks for 'image.jpg' -> Nginx sends it (Nginx is 10x faster).
   - If a user asks for '/predict' -> Nginx passes it to Flask.

3. INDUSTRY USE CASE:
   Every professional AI website (OpenAI, HuggingFace, etc.) uses Nginx.
   Nginx also handles SSL (HTTPS) and acts as a firewall to block bad 
   bots before they even reach your Python code.

4. THE "LOAD BALANCER" ROLE:
   Nginx can also do "Load Balancing". It can send the 1st request to 
   Flask-A, the 2nd to Flask-B, and the 3rd to Flask-C. This is how you 
   scale to millions of users.
===========================================================================
"""

import os

def generate_nginx_example_config():
    config = """
    # EXAMPLE NGINX CONFIGURATION (Conceptual)
    
    server {
        listen 80;
        server_name my-ai-app.com;

        # 1. SERVE STATIC FILES DIRECTLY (Fast!)
        location /static/ {
            root /var/www/my_app/;
        }

        # 2. PASS LOGIC TO FLASK (Waitress/Gunicorn)
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    """
    return config

if __name__ == "__main__":
    print("This file contains the concept of Reverse Proxies.")
    print("Read the comments above to understand how Nginx protects Flask.")
