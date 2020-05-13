'''
Auto-Stop Type 1: Run on a schedule to auto-stop EC2 instances
by John Rotenstein (https://github.com/aws-john/simple-lambda-stopinator-for-ec2)
SPDX-License-Identifier: MIT-0

By default, all Amazon EC2 instances will be stopped.

Add an 'Auto-Stop' tag to an instance to change behaviour, with a Value of:
- 'Stop' to stop the instance (same as default)
- 'Terminate' to terminate the instance (good for temporary instances)
- 'Ignore' to skip-over the instance
'''

import boto3

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
            action = 'stop' # Default action
            
            # Extract action from 'Auto-Stop' tag (if present)
            for tag in instance.tags:
                if tag['Key'].lower() == 'auto-stop':
                    action = tag['Value'].lower()
            
            if action == 'stop':
                print(f'Stopping instance {instance.id}')
                instance.stop()
                
            elif action == 'terminate':
                print(f'Terminating instance {instance.id}')
                instance.terminate()
                 
            else:
                print(f'Ignoring instance {instance.id}')
