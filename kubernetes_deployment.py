"""
This script deploys a Kubernetes Deployment file to an EKS cluster.
It uses the provided kubeconfig path to authenticate and applies the deployment YAML.
"""

import subprocess
import os
import logging
import sys

# Configure structure logging(works well with Jenkins, GitHub Actions, CloudWatch, etc.)
logging.basicConfig(level=logging.info, format="%(asctime)s - %(levelname)s - %(message)s")

def deploy_to_eks(kubeconfig_path, deployment_file):
    # Deploy the given kubernetes deployment file to the EKS cluster
    try:
        # Validate file existance
        if not os.path.exists(kubeconfig_path):
            logging.error(f"Kubeconfig file not found: {kubeconfig_path}")
            return False
        if not os.path.exists(deployment_file):
            logging.error(f"Deployment file not found: {deployment_file}")
            return False
        
        # Set the kubeconfig environment variable safely
        os.environ["KUBECONFIG"] = kubeconfig_path
        logging.info(f"Using kubeconfig: {kubeconfig_path}")

        # Run kubectl apply
        result = subprocess.run(
            ["kubectl", "apply", "-f", deployment_file],
            capture_output= True,
            text= True
            )
        
        if result.returncode == 0:
            logging(f"Deployment applied successfully: {deployment_file}")
            return True
        else:
            logging.error(f"Deployment failed for {deployment_file}")
            logging.error(result.stderr.strip())
            return False
    except FileNotFoundError:
        logging.error("kubectl command not found. Ensure kubectl is installed and in Path")
        return False
    except subprocess.SubprocessError as e:
        logging.error(f"Subprocess execution error: {str(e)}")
        return False
    except Exception as e:
        logging.exception(f"Unknown error during deployment: {str(e)}")
        return False
    
if __name__ == "__main__":
    #Example usage
    kubeconfig_path = "/path/to/kubeconfig"
    deployment_file = "deployment.yaml"

    success = deploy_to_eks(kubeconfig_path, deployment_file)

    # Exit non zero if the deployment fails
    if not success:
        sys.exit(1)





