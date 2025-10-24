"""
This script performs health checks for deployed services.
It sends HTTP GET requests to /health endpoint and logs the results.
Includes robust exception handling and logging for production monitoring.
"""
import requests
import logging
import os
import sys

# Timeout for each health check (seconds)
TIMEOUT = int(os.getenv("SERVICE_HEALTH_TIMEOUT", 5))

# Configure logging for visibility in console or CloudWatch
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_environment_health(service_url):
    # Check the health of the service by calling its /health endpoint
    try:
        response = requests.get(service_url, timeout=TIMEOUT)

        if response.status_code == 200:
            logging.info(f"Service is healthy: {service_url}")
            return True
        else:
            logging.warning(f"Service is unhealthy ({response.status_code}): {service_url}")
            return False
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection error: Unable to reach {service_url}")
        return False
    except requests.exceptions.Timeout:
        logging.error(f"Timeout: {service_url} took too long to respond")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Unexpected error for {service_url}: {str(e)}")
        return False

if __name__ == "__main__":
    # List of services to check
    services = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/10",
    "https://api.github.com",
    "http://nonexistent-domain-for-test.com"
]
    
    # Run health checks
    results = [check_environment_health(service) for service in services]

    # Exit with non-zero code if any service is unhealthy (useful for CI/CD)
    if not all(results):
        sys.exit(1)
