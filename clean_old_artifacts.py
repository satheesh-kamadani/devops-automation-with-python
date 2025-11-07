"""
This script will delete old artifacts (older than 30 days) from Artifactory.
"""

import requests
import logging
from datetime import datetime, timedelta
import sys

TIMEOUT = 5

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_old_artifacts(artifactory_url, repo, retention_days, username, password):
    """
    Deletes artifacts older than 'retention_days' from the given repository.
    """
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    logging.info(f"Deleting artifacts older than {retention_days} days (before {cutoff_date.date()})")

    try:
        # Get the list of artifacts
        response = requests.get(
            f"{artifactory_url}/api/storage/{repo}?list&deep=1",
            auth=(username, password),
            timeout=TIMEOUT
        )

        if response.status_code != 200:
            logging.error(f"Failed to get artifact list: HTTP {response.status_code}")
            return False

        data = response.json()
        files = data.get("files", [])

        if not files:
            logging.info("No artifacts found in the repository.")
            return True

        deleted_count = 0

        for item in files:
            artifact_uri = item.get("uri")
            if not artifact_uri:
                continue

            # Get details of the artifact (to check created date)
            info_url = f"{artifactory_url}/api/storage/{repo}{artifact_uri}"
            info_resp = requests.get(info_url, auth=(username, password), timeout=TIMEOUT)

            if info_resp.status_code != 200:
                logging.warning(f"Could not get info for {artifact_uri}")
                continue

            info = info_resp.json()
            created_str = info.get("created")

            # Try to convert creation date to datetime
            try:
                created_date = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except Exception:
                logging.warning(f"Could not read date for {artifact_uri}")
                continue

            # If artifact is older than cutoff date, delete it
            if created_date < cutoff_date:
                delete_url = f"{artifactory_url}/{repo}{artifact_uri}"
                delete_resp = requests.delete(delete_url, auth=(username, password), timeout=TIMEOUT)

                if delete_resp.status_code == 200:
                    logging.info(f"Deleted old artifact: {delete_url}")
                    deleted_count += 1
                else:
                    logging.error(f"Failed to delete: {delete_url}")

        logging.info(f"Total deleted: {deleted_count}")
        return True

    except requests.Timeout:
        logging.error("Request timed out. Please check network connection.")
        return False
    except requests.ConnectionError:
        logging.error("Could not connect to Artifactory. Please check the URL.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Basic configuration
    artifactory_url = "http://artifactory.example.com/artifactory"
    repo = "libs-release-local"
    retention_days = 30
    username = "admin"
    password = "admin"

    success = clean_old_artifacts(artifactory_url, repo, retention_days, username, password)

    if not success:
        sys.exit(1)
