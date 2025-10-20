# Triggering jenkins pipeline using python script

import requests

def trigger_jenkins_build(job_name, jenkins_url, jenkins_user, jenkins_token):
    url = f"{jenkins_url}/job/{job_name}/build"
    response = requests.post(url, auth=(jenkins_user, jenkins_token))
    if response.status_code == 201:
        print(f"Successfully triggered jenkins job: {job_name}")
    else:
        print(f"Failed to trigger jenkins job: {job_name}, status_code: {response.status_code}")

if __name__ == "__main()":
    trigger_jenkins_build("Microservices-Build", "http://jenkins.example.com", "jenkins_user", "jenkins_token")
    

