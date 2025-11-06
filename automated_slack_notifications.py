"""
This script sends Slack notifications for various events
(e.g., build failures, successful deployments).
"""

import requests
import logging
import sys

# Configuration
TIMEOUT = 5 # seconds
WEBHOOK_URL = "https://hooks.slack.com/services/T000000"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_slack_notification(webhook_url, message, timeout=TIMEOUT):
    """Send a message to Slack using an incoming webhook."""
    payload = {"text": message}
    try:
        logging.info("Sending slack notification")
        response = requests.post(webhook_url, json=payload, timeout=TIMEOUT)
        if response.status_code == 200:
            logging.info("Slack notification sent successfully")
            return True
        else:
            logging.error(f"Failed to send the slack notification. HTTP {response.status_code}")
            return False

    except requests.Timeout:
        logging.error("Request timed out, check your network or webhook URL")
        return False
    except requests.ConnectionError:
        logging.error("Connection error. Unable to reach slack servers.")
        return False
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    message = "Deployment completed successfully"
  
    success = send_slack_notification(WEBHOOK_URL, message)

    if not success:
        logging.error("Slack notification failed. Exiting with error code 1.")
        sys.exit(1)
    else:
        logging.info("Script completes successfully")

    

