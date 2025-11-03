"""
This script aggregates log files from a given directory,
analyzes them, and counts the number of error lines.
"""

import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def aggregate_logs(log_dir, output_file):
    """Combine all .log files in a directory into one output file."""
    try:
        with open(output_file, 'w') as outfile:
            for log_file in os.listdir(log_dir):
                if log_file.endswith(".log"):
                    log_path = os.path.join(log_dir, log_file)
                    logging.info(f"Reading log file: {log_path}")
                    try:
                        with open(log_path, 'r') as infile:
                            outfile.writelines(infile.readlines())
                    except Exception as e:
                        logging.error(f"Failed to read {log_file}: {str(e)}")
        logging.info(f"Logs aggregated into: {output_file}")
    except FileNotFoundError:
        logging.error(f"Log directory not found: {log_dir}")
    except PermissionError:
        logging.error(f"Permission denied accessing: {log_dir}")
    except Exception as e:
        logging.error(f"Unexpected error during log aggregation: {str(e)}")

def analyze_log(log_file):
    """Count the number of error lines in the aggregated log file."""
    error_count = 0
    try:
        with open(log_file, 'r') as file:
            for line in file:
                if "ERROR" in line:
                    error_count += 1
        logging.info(f"Total error lines found: {error_count}")
    except FileNotFoundError:
        logging.error(f"Log file not found: {log_file}")
    except Exception as e:
        logging.error(f"Error analyzing log: {str(e)}")

if __name__ == "__main__":
    # Directory containing log files
    log_directory = "/Users/satheesh/Documents/DevOps_Projects/devops-automation-with-python/log_directory"

    # Generate timestamped output file name
    aggregated_log_file = f"aggregated_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Aggregate and analyze logs
    aggregate_logs(log_directory, aggregated_log_file)
    analyze_log(aggregated_log_file)
