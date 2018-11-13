'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
import sys
import json
from botocore.exceptions import ClientError

parameters=sys.argv
account = parameters[1]
profile = parameters[2]

try: 
    # by using the profile included in the arguments, we can switch to the master account 
    # this allows use of the OrganizationAccountAccessRole to create the other two cross account access roles
    session = boto3.Session(profile_name=profile)
    sts_client = session.client('sts')

    role = "arn:aws:iam::" + account + ":role/OrganizationAccountAccessRole"
    sessionId = "create-cross-account-roles" 

    # next access the STS service to receive credentials for the OrganizationAccountAccessRole
    # once we have the credentials, we will use them to create the next boto3 client
    sts_response = sts_client.assume_role(RoleArn=role, RoleSessionName=sessionId)
    credentials = sts_response['Credentials']
    
    # the new roles will allow BlueMoon enabled engineers to use the cross account access roles
    my_managed_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::706839808421:root"
          },
          "Action": "sts:AssumeRole",
          "Condition": {}
        }
      ]
    }
    # unlike the typical client invocations you need to supply the credentials and the session token received from 
    # the earlier call to STS
    client=boto3.client('iam',aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'])
    
    # create the first role and apply the permissions policy
    response = client.create_role(
        Path="/",
        RoleName='CDWCustomerAccountAccessRole-joe',
        AssumeRolePolicyDocument=json.dumps(my_managed_policy),
        Description='Cross Account role for CDW to access Customer Account'
    )
    
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }
    
    response = client.put_role_policy(
        PolicyDocument=json.dumps(permissions_policy),
        PolicyName='cdw-cloudhealth-readonly-policy',
        RoleName='CDWCustomerAccountAccessRole-joe'
    )
    
    # create the second role and apply the permissions policy
    response = client.create_role(
        Path="/",
        RoleName='AWSCloudFormationStackSetExecutionRole-joe',
        AssumeRolePolicyDocument=json.dumps(my_managed_policy),
        Description='Cross Account role for CDW to access Customer Account'
    )
    
    response = client.put_role_policy(
        PolicyDocument=json.dumps(permissions_policy),
        PolicyName='cdw-cloudhealth-readonly-policy',
        RoleName='AWSCloudFormationStackSetExecutionRole-joe'
    )

except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)