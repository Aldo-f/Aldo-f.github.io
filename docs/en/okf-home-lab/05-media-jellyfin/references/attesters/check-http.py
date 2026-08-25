#!/usr/bin/env python3
"""
Jellyfin Health Check Attester
Validates that the Jellyfin health check was executed correctly
"""

import subprocess
import sys
import os

def test_jellyfin_healthcheck():
    """Test the Jellyfin health check by running the executor script"""
    
    # Path to the executor script
    executor_script = os.path.join(os.path.dirname(__file__), '..', 'skills', 'run-jellyfin-check.sh')
    
    try:
        # Run the health check script
        result = subprocess.run(
            ['bash', executor_script, 'http://127.0.0.1:8096/health'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print(f"ERROR: Health check failed with exit code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("ERROR: Health check timed out")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run health check: {e}")
        return False

if __name__ == "__main__":
    if test_jellyfin_healthcheck():
        sys.exit(0)
    else:
        sys.exit(1)