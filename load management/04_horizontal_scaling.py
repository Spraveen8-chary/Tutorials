"""
===========================================================================
LESSON 4: HORIZONTAL VS VERTICAL SCALING
===========================================================================

1. VERTICAL SCALING (Scale UP):
   Buying a bigger computer. 
   - Example: Upgrading from 8GB RAM to 64GB RAM.
   - Limit: Eventually, there is no bigger computer you can buy.

2. HORIZONTAL SCALING (Scale OUT):
   Adding more computers.
   - Example: Instead of 1 big server, you have 10 small servers.
   - Industry Standard: This is done using **Docker** and **Kubernetes**.

3. THE ROLE OF CONTAINERS:
   You put your Flask app into a 'Docker Image'. 
   You can then 'Spin up' 50 copies of that image in seconds.

4. REAL WORLD ARCHITECTURE:
   [ Internet ] 
        |
   [ Load Balancer (Nginx/Cloudflare) ] 
      /     |      \
 [Server 1] [Server 2] [Server 3]  <-- All running your Flask app.
      \     |      /
   [ Shared Database ]
===========================================================================
"""

import threading
import requests
import time

def simulate_load_balancer():
    # In the real world, this logic is handled by Nginx or AWS Load Balancer
    servers = ["http://server-a.com", "http://server-b.com", "http://server-c.com"]
    
    for i in range(6):
        target = servers[i % len(servers)]
        print(f"Request {i+1} -> Sending to {target}")

if __name__ == "__main__":
    print("CONCEPTUAL SCALING GUIDE\n")
    simulate_load_balancer()
    print("\nRead the comments above to understand the difference between Scaling Up and Scaling Out.")
