"""
This script performs static code analysis using SonarQube.
It invokes the SonarQube scanner with provided project and server details.
"""
import subprocess
import os
import sys
import logging

# Configure logging for CI/CD visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_sonar_qube_analysis(project_key, project_name, project_version, sonar_host, sonar_login):
    # Run the sonar qube analysis via sonar-scanner
    try:
        # Validate input parameters
        if not all([project_key, project_name, project_version, sonar_host, sonar_login]):
            logging.error("Missing required sonarQube parameters, please configure it before running this script")
            return False
        
        # Check if sonar scannar is installed
        result_check = subprocess.run("which", "sonar-scanner", capture_output=True, text=True)
        if result_check.returncode != 0:
            logging.error("sonar-scanner not found in the path, please install or configure it")
            return False
        
        # Construct sonnar-scanner command
        command = [
            "sonar-scanner",
            f"-Dsonar.projectKey={project_key}",
            f"-Dsonar.projectName={project_name}",
            f"-Dsonar.projectVersion={project_version}",
            f"-Dsonar.host.url={sonar_host}",
            f"-Dsonar.login={sonar_login}"
        ]

        logging.info("Starting SonarQube analysis")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info("Sonarqube analysis completed successfully")
            return True
        else:
            logging.error("Sonarqube analysis failed")
            logging.error(result.stderr.strip())
            return False
    except FileNotFoundError as e:
        logging.error("sonar-scanner executable not found, Ensure it is installed or accesible")
        return False
    except subprocess.SubprocessError as e:
        logging.error(f"Subprocess execution error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during SonarQube analysis: {str(e)} ")
        return False
    
if __name__ == "__main__":
    # Example configuration(can be parameterized via environment variables in CI/CD)
    project_key = os.getenv("SONAR_PROJECT_KEY", "my-project-key")
    project_name = os.getenv("SONAR_PROJECT_NAME", "my-project")
    project_version = os.getenv("SONAR_PROJECT_VERSION", "1.0")
    sonar_host = os.getenv("SONAR_HOST_URL", "http://sonar.example.com")
    sonar_login = os.getenv("SONAR_LOGIN_TOKEN", "my-sonar-token")

    success = run_sonar_qube_analysis(project_key, project_name, project_version, sonar_host, sonar_login)

    # Exit with failure code if analysis fails
    if not success:
        sys.exit(1)

