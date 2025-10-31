"""
This script uploads build JAR files to Artifactory.
"""
from pathlib import Path
import requests
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def upload_to_artifactory(artifact_path, artifact_url, repo, artifact_user, artifact_password):
    try:
        # Ensure artifact file exists
        file_path = Path(artifact_path)
        if not file_path.is_file():
            logging.error(f"File not found: {file_path}")
            return False

        # Construct full Artifactory upload URL
        upload_url = f"{artifact_url}/{repo}/{file_path.name}"
        logging.info(f"Uploading artifact to: {upload_url}")

        # Upload the file to Artifactory
        with open(file_path, "rb") as file:
            response = requests.put(upload_url, data=file, auth=(artifact_user, artifact_password), timeout=30)

        # Check response status
        if response.status_code in [200, 201]:
            logging.info(f"✅Artifact uploaded successfully: {upload_url}")
            return True
        else:
            logging.error(f"Failed to upload artifact. Status code: {response.status_code}, Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        logging.error("Upload request timed out. Check your network or Artifactory server.")
        return False
    except requests.exceptions.ConnectionError:
        logging.error("Connection error: Unable to reach Artifactory server.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Artifactory connection details
    ARTIFACTORY_PATH = os.getenv("ARTIFACTORY_PATH", "builds/myapp.jar")
    ARTIFACTORY_URL = os.getenv("ARTIFACTORY_URL", "https://example.jfrog.io/artifactory")
    REPO = os.getenv("REPO", "libs-release-local")
    ARTIFACTORY_USER = os.getenv("ARTIFACTORY_USER", "admin")
    ARTIFACTORY_PASSWORD = os.getenv("ARTIFACTORY_PASSWORD", "password")

    # Upload JAR file to Artifactory
    success = upload_to_artifactory(
        ARTIFACTORY_PATH,
        ARTIFACTORY_URL,
        REPO,
        ARTIFACTORY_USER,
        ARTIFACTORY_PASSWORD
    )

    # Exit with non-zero code if upload fails (useful for CI/CD)
    if not success:
        sys.exit(1)
