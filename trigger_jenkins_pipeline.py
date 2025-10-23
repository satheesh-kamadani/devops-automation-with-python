"""
This script triggers a Jenkins job using the Jenkins REST API.
It authenticates with a Jenkins user and token, sends a POST request,
and provides clear logging and error handling for CI/CD automation.
"""
import requests
import logging
import os

TIMEOUT = int(os.getenv("JENKINS_TIMEOUT", 10))

# Configure logging for visibility in console or CloudWatch
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def trigger_jenkins_build(job_name, jenkins_url, jenkins_user, jenkins_token):
    # Construct jenkins job url
    url = f'{jenkins_url}/job/{job_name}/build'

    try:
        # Send post request with authentication
        response = requests.post(url, auth=(jenkins_user, jenkins_token), timeout=TIMEOUT)

        # Jenkins return 201 if the job was successfully triggered
        if response.status_code == 201:
            logging.info(f"Triggered Jenkins job: {job_name}")
            return True
        else:
            logging.error(
                 f"Failed to trigger Jenkins job: '{job_name}'."
                 f"Status code: {response.status_code}, Response: {response.text}"
            )
            return False
    except requests.exceptions.ConnectionError:
        logging.error("Connection error: Unable to reach jenkins server")
        return False
    except requests.exceptions.Timeout:
        logging.error("Timeout: Jenkins server did not respond")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
        # Jenkins connection details
        JOB_NAME = "Microservice build"
        JENKINS_URL = os.getenv("JENKINS_URL", "http://jenkins.example.com")
        JENKINS_USER = os.getenv("JENKINS_USER")
        JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

        # Trigger the jenkins job
        trigger_jenkins_build(JOB_NAME, JENKINS_URL, JENKINS_USER, JENKINS_TOKEN)




    






