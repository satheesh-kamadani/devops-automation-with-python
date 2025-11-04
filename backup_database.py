"""
This script takes a backup of a PostgreSQL database using pg_dump.
"""

import subprocess
import os
import datetime
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read timeout(default 5 minutes if not set)
TIMEOUT = int(os.getenv("DB_TIMEOUT", 5)) * 60

def backup_database(db_name, db_user, db_password, backup_dir, timeout=TIMEOUT):
    # Backup a postgresql into a .sql file
    try:
        # Ensure backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f"Created backup directory: {backup_dir}")

        # Generate backup file name with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

        # Build pg_dump command
        command = [
            "pg_dump",
            f"--dbname=postgresql://{db_user}:{db_password}@localhost/{db_name}",
            "--file", backup_file
        ]

        logging.info(f"Starting database backup for '{db_name}....")
        subprocess.run(command, check=True, timeout=TIMEOUT)
        logging.info(f"Database backup completed successfully: {backup_file}")
        return True
    
    except subprocess.TimeoutExpired:
        logging.error(f"Backup process timeout after {timeout} seconds.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"pg_dump failed with exit code: {e.returncode}.")
        return False
    except FileNotFoundError:
        logging.error("pg_dump command not found. Please install postgresql client tools")
        return False
    except PermissionError:
        logging.error(f"Permission denied for directory: {backup_dir}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    # Example values - replace these or load from environment variables
    DB_NAME = "mydatabase"
    DB_USER = "dbuser"
    DB_PASSWORD = "dbpassword"
    BACKUP_DIR = "/path/to/backupdir"

    # Run backup
    success = backup_database(DB_NAME, DB_USER, DB_PASSWORD, BACKUP_DIR)

    # Exit code for automation tools(0 = success, 1 = failure)
    if not success:
        sys.exit(1)