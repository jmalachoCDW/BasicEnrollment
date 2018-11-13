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
    session = boto3.Session(profile_name=profile)
    sts_client = session.client('sts')

    role = "arn:aws:iam::" + account + ":role/OrganizationAccountAccessRole"
    sessionId = "create-cross-account-roles" 
    sts_response = sts_client.assume_role(RoleArn=role, RoleSessionName=sessionId)
    credentials = sts_response['Credentials']
    
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
    
    client=boto3.client('iam',aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'])
    
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
    
    #REM the next two commands create the AWSCloudFormationStackSetExecutionRole
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