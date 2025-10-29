"""
Scan Docker images for vulnerabilities using Trivy.
This script pulls images from Docker Hub and scans them for security issues.
Generates a consolidated scan report saved to `trivy_scan_report.txt`.
"""

import subprocess
import logging
import os
import sys

# Configure logging for console or CI/CD visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# List of Docker images to scan
DOCKER_IMAGES = [
    "satheeshkamadani/stockmanager:latest",
    "satheeshkamadani/productcatalogue:latest",
    "satheeshkamadani/shopfront:latest"
]


def scan_docker_image(image_name):
    """Run a Trivy scan on a given Docker image and return the result."""
    logging.info(f"Scanning image: {image_name} ...")

    try:
        result = subprocess.run(
            ["trivy", "image", "--quiet", image_name],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit code
        )

        return result.stdout or result.stderr

    except FileNotFoundError:
        logging.error("Trivy is not installed or not found in PATH.")
        return f"Error: Trivy not found for image {image_name}\n"

    except subprocess.SubprocessError as e:
        logging.error(f"Subprocess error scanning image {image_name}: {str(e)}")
        return f"Error scanning image {image_name}: {str(e)}\n"

    except Exception as e:
        logging.exception(f"Unexpected error scanning image {image_name}: {str(e)}")
        return f"Error scanning image {image_name}: {str(e)}\n"


if __name__ == "__main__":
    report_file = "trivy_scan_report.txt"
    logging.info("Starting Docker image vulnerability scans...")

    try:
        # Open report file ONCE and keep it open during all scans
        with open(report_file, "w") as file:
            file.write("=== Docker Image Vulnerability Scan Report ===\n\n")

            for docker_image in DOCKER_IMAGES:
                scan_report = scan_docker_image(docker_image)
                file.write(f"--- Scan Report for Docker Image: {docker_image} ---\n")
                file.write(scan_report)
                file.write("\n\n")

        # Writing done safely inside `with` block
        logging.info(f" Scan completed. Full report saved to: {os.path.abspath(report_file)}")

    except PermissionError:
        logging.error("Permission denied: Unable to write report file.")
        sys.exit(1)

    except Exception as e:
        logging.exception(f"Unexpected error during report generation: {str(e)}")
        sys.exit(1)
