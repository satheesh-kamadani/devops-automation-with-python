"""
This script builds a Docker image and pushes it to Amazon ECR.
"""
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_and_push_docker_image(repository_name, image_tag, aws_account_id, aws_region):
    # Define ECR repository URL and image name
    ecr_url = f"{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com"
    image_name = f"{ecr_url}/{repository_name}:{image_tag}"

    try:
        # Step 1: Build the Docker image
        logging.info(f"Building Docker image: {image_name}")
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        
        # Step 2: Get ECR login password
        logging.info("Logging in to Amazon ECR...")
        password = subprocess.check_output(
            ["aws", "ecr", "get-login-password", "--region", aws_region]
        ).decode().strip()

        # Step 3: Authenticate Docker with ECR
        subprocess.run(
            ["docker", "login", "--username", "AWS", "--password", password, ecr_url],
            check=True
        )

        # Step 4: Push the Docker image to ECR
        logging.info(f"Pushing image to ECR: {image_name}")
        subprocess.run(["docker", "push", image_name], check=True)

        logging.info(f"Image successfully pushed to ECR: {image_name}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
    except FileNotFoundError:
        logging.error("Docker or AWS CLI not found. Please install both before running this script.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    build_and_push_docker_image(
        repository_name="microservice_repo",
        image_tag="latest",
        aws_account_id="123456789012",
        aws_region="us-east-1"
    )
