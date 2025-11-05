"""
This script will scale a Kubernetes deployment to the desired number of replicas.
"""

import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scale_kubernetes_deployment(deployment_name, namespace, replicas):
    logging.info(f"Starting to scale deployment '{deployment_name} in namespace '{namespace}")
    try:
        # Run the kubectl scale command
        result = subprocess.run(
            [
                "kubectl", "scale",
                f"--replicas={replicas}",
                "deployment", deployment_name,
                f"--namespace={namespace}"
            ],
            capture_output= True,
            text= True,
            check= True
        )

        # Log command output
        logging.info(f"command output: {result.stdout.strip()}")
        logging.info(f"Successfully scaled deployment '{deployment_name} to {replicas} replicas")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to scale deployment. Command error {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        # Handles if kubectl is not installed.
        logging.error("Error: 'kubectl' command not found. Please ensure kubectl is installed")
        return False
    except Exception as e:
        logging.error(f"Unexpected error occured {str(e)}")
        return False
    
if __name__ == "__main__":
    # You can modify this values or pass them from command line arguments
    deployment_name = 'my-microservice'
    namespace = 'default'
    replicas = 5

    # Scaling deployment
    success = scale_kubernetes_deployment(deployment_name, namespace, replicas)

    # Exit with non zero code if scaling failed
    if not success:
        sys.exit(1)
        