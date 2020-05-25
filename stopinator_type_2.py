'''
Auto-Stop Type 2: Stop/Terminate/Notify instances after given duration
by John Rotenstein (https://github.com/aws-john/simple-lambda-stopinator-for-ec2)
SPDX-License-Identifier: MIT-0

Tag Names (in priority order):
- Terminate-After: Terminate instance
- Stop-After: Stop instance
- Notify-After: Send SNS notification if still running
  (For multiple notifications, use 'Notify-After1', 'Notify-After2', etc)

Tag Value: Indicates running duration (eg '30m', '1.5h', '24h')

Schedule this Lambda function to run at regular intervals (eg every 5 minutes)

'''

import boto3
from datetime import datetime, timedelta

# To send a notification, insert SNS Topic ARN here
SNS_TOPIC_ARN = ''

TAG_STOP      = 'stop-after'
TAG_TERMINATE = 'terminate-after'
TAG_NOTIFY    = 'notify-after'

sns_resource = boto3.resource('sns')

def lambda_handler(event, context):
   
    # Provide regions here (eg ['us-west-2', 'ap-southeast-2'], or use [] for all regions
    regions_to_check = []

    # Check all regions?
    if not regions_to_check:
        regions_to_check = [r['RegionName'] for r in boto3.client('ec2').describe_regions()['Regions']]

    for region in regions_to_check:
        print('Region: ', region)
    
        ec2_resource = boto3.resource('ec2', region_name = region)
        
        running_filter = {'Name':'instance-state-name', 'Values':['running']}
        instances = ec2_resource.instances.filter(Filters=[running_filter])
        
        for instance in instances:
            
            # No tags?
            if instance.tags == None:
                continue

            # Terminate?
            if value := [tag['Value'] for tag in instance.tags if tag['Key'] == TAG_TERMINATE]:
                if check_duration(value[0], instance.launch_time):
                    print(f'Terminating instance {instance.id}')
                    instance.terminate()

            # Stop?
            elif value := [tag['Value'] for tag in instance.tags if tag['Key'] == TAG_STOP]:
                if check_duration(value[0], instance.launch_time):
                    print(f'Stopping instance {instance.id}')
                    instance.stop()

            # Notify? Check all and delete any that have elapsed to allow future notifications
            elif SNS_TOPIC_ARN != '' and (values := [tag for tag in instance.tags if tag['Key'].startswith(TAG_NOTIFY)]):
                notify = False
                for tag in values:
                    if check_duration(tag['Value'], instance.launch_time):
                        notify = True
                        instance.delete_tags(Tags=[tag])
                        duration = tag['Value']
                if notify:
                    message = f'Instance {instance.id} has been running for {duration}'
                    print('Sending notification:', message)
                    sns_resource.Topic(SNS_TOPIC_ARN).publish(Message=message)
            

def check_duration(duration_string, launch_time):
    
    # Extract duration to wait
    try:
        if duration_string[-1] == 'm':
            minutes = int(duration_string[:-1])
        elif duration_string[-1] == 'h':
            minutes = int(float(duration_string[:-1]) * 60)
        else:
            print(f'Invalid duration of "{duration_string}" for instance {instance.id}')
            return False
    except:
        print(f'Invalid duration of "{duration_string}" for instance {instance.id}')
        return False
    
    # Check whether required duration has elapsed
    return datetime.now().astimezone() > launch_time + timedelta(minutes=minutes)
