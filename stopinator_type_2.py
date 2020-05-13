'''
Auto-Stop Type 2: Stop instances after given duration
by John Rotenstein (https://github.com/aws-john/simple-lambda-stopinator-for-ec2)
SPDX-License-Identifier: MIT-0

- Stop any running Amazon EC2 instance with a 'Stop-After' tag
- Terminate any running Amazon EC2 instance with a 'Terminate-After' tag
- The tag Value indicates running duration (eg '30m', '24h')

Schedule this Lambda function to run at regular intervals (eg every 5 minutes)

'''

import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
   
    # Provide regions here (eg ['us-west-2', 'ap-southeast-2'], or use [] for all regions
    regions_to_check = ['ap-southeast-2']

    # Check all regions?
    if not regions_to_check:
        regions_to_check = [r['RegionName'] for r in boto3.client('ec2').describe_regions()['Regions']]

    for region in regions_to_check:
        print('Region: ', region)
    
        ec2_resource = boto3.resource('ec2', region_name = region)
        
        running_filter = {'Name':'instance-state-name', 'Values':['running']}
        instances = ec2_resource.instances.filter(Filters=[running_filter])
        
        for instance in instances:
            action = 'ignore' # Default action
            
            # Check for 'Stop-After' or 'Terminate-After' tag
            for tag in instance.tags:
                if tag['Key'].lower() in ['stop-after', 'terminate-after']:
                    action = tag['Key'].lower().split('-')[0]
                    duration_string = tag['Value'].lower()
                    
                    if duration_string[-1] == 'm':
                        minutes = int(duration_string[:-1])
                    elif duration_string[-1] == 'h':
                        minutes = int(duration_string[:-1]) * 60
                    else:
                        print(f'Invalid duration of "{duration_string}" for instance {instance.id}')
                        action = 'ignore'
            
            if action == 'ignore':
                continue

            # Check if duration has expired
            if datetime.now().astimezone() > instance.launch_time + timedelta(minutes=minutes):

                if action == 'stop':
                    print(f'Stopping instance {instance.id}')
                    instance.stop()
                    
                elif action == 'terminate':
                    print(f'Terminating instance {instance.id}')
                    instance.terminate()
