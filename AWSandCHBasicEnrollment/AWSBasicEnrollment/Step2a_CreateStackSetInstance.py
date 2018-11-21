'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
import sys
from botocore.exceptions import ClientError

parameters=sys.argv

account = parameters[1]
account = account[account.find("=")+1:]

profile = parameters[2]
profile = profile[profile.find("=")+1:]


try:
    # this code writes a new profile to the AWS config file to allow BlueMoon to use the CDWCustomerAccountAccessRole
    # to administer customer resources in the target environment
    f=open("config","a")
    f.write("\n")
    f.write("[profile "+profile+"]\n")
    f.write("role_arn = arn:aws:iam::"+account+":role/CDWCustomerAccountAccessRole\n")
    f.write("source_profile = default\n")
    f.write("region = us-east-2\n")
    f.close()

    # this next section creates a stack instance from the BlueMoon account to run in the target account
    cfm_client = boto3.client('cloudformation')
    
    response = cfm_client.create_stack_instances(
        StackSetName='cloudhealth-enrollment',
        Accounts=[
            account
        ],
        Regions=[
            'us-east-2'
        ]
    )
    print ("Stack Instance created successfully")
   
except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)