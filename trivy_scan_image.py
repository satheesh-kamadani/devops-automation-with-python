"""
Scan Docker images for vulnerabilities using Trivy.
This script pulls images from Docker Hub and scans them for security issues.
Generates a consolidated scan report saved to `trivy_scan_report.txt`.
"""
import subprocess

DOCKER_IMAGES = [
    "satheeshkamadani/stockmanager:latest", 
    "satheeshkamadani/productcatalogue:latest",
    "satheeshkamadani/shopfront:latest"
    ]
def scan_docker_image(image_name):
    # Run a trivy scan on a given docker image and return result
    print(f"Scanning image: {image_name}...")
    try:
        def scan_docker_image(image_name):
            result = subprocess.run(
                ["trivy", "image", "--quite", image_name],
                capture_output=True,
                text=True,
                check=False # Avoid exception on non-zero exit codes
            )
            return result.stdout
    except FileNotFoundError:
        print(f"Trivy is not installed or not found in PATH")
        return f"Error: Trivy not found for image {image_name}\n"
    except Exception as e:
        print(f"Error scanning image {image_name}: {str(e)}")
        return f"Error scanning image {image_name}: {str(e)}\n"
    
if __name__ == "__main__":
    report_file = "trivy_scan_report.txt"

    # Open the report file and write scan results
    with open(report_file, "w") as file:
        file.write("=== Docker image vulnerability scan report ===\n\n")

    for docker_image in DOCKER_IMAGES:
        scan_report = scan_docker_image(docker_image)
        file.write(f"--- Scan report for docker image {docker_image} ---\n")
        file.write(scan_report)
        file.write("\n\n")
    
    print(f"Scan completed full report saved to: {report_file}")

    
    

    

