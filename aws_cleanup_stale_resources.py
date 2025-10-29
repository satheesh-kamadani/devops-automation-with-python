"""
Lambda function to delete unused AWS EBS snapshots.
"""

import boto3
import logging
from botocore.exceptions import ClientError

# Initialize AWS clients
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

# Replace with your SNS Topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:ebs-snapshot-cleanup"

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info("Fetching all EBS snapshots owned by the account...")
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        logger.info(f"Total snapshots found: {len(snapshots)}")

        logger.info("Fetching all EC2 instances to check attached volumes...")
        instances = ec2.describe_instances()['Reservations']
        active_volume_ids = set()

        for reservation in instances:
            for instance in reservation['Instances']:
                for block_device in instance.get('BlockDeviceMappings', []):
                    if 'Ebs' in block_device:
                        active_volume_ids.add(block_device['Ebs']['VolumeId'])

        stale_snapshots = []

        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            volume_id = snapshot.get('VolumeId')

            # Identify snapshots not linked to any active volume or instance
            if not volume_id or volume_id not in active_volume_ids:
                stale_snapshots.append(snapshot_id)

        if not stale_snapshots:
            logger.info("No stale snapshots found.")
            return {"status": "success", "message": "No unused snapshots to delete."}

        # Notify before deletion
        message = f"The following unused EBS snapshots will be deleted:\n{', '.join(stale_snapshots)}"
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EBS Snapshot Cleanup Notification",
            Message=message
        )
        logger.info("Sent SNS notification before deletion.")

        # Delete unused snapshots
        for snapshot_id in stale_snapshots:
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                logger.info(f"Deleted snapshot: {snapshot_id}")
            except ClientError as e:
                logger.error(f"Error deleting snapshot {snapshot_id}: {str(e)}")

        logger.info("EBS snapshot cleanup completed successfully.")
        return {"status": "success", "deleted_snapshots": stale_snapshots}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EBS Snapshot Cleanup Lambda Failed",
            Message=f"An error occurred: {str(e)}"
        )
        return {"status": "error", "message": str(e)}
