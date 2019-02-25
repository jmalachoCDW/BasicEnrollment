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
account = account[account.find("=")+1:]

profile = parameters[2]
profile = profile[profile.find("=")+1:]

bluemoon = parameters[3]
bluemoon = bluemoon[bluemoon.find("=")+1:]



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
            "AWS": "arn:aws:iam::"+ bluemoon +":root"
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

    roles_list = []
    roles = client.list_roles()
    Role_list = roles['Roles']
    for key in Role_list:
        roles_list.append(key['RoleName'])
    # create the first role and apply the permissions policy
    if  'CDWCustomerAccountAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWCustomerAccountAccessRole',
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
            RoleName='CDWCustomerAccountAccessRole'
        )

        print ("CDWCustomerAccessRole created Successfully")

    else:
        print ("CDWCustomerAccessRole Already Exists")


    # create the second role and apply the permissions policy
    if  'AWSCloudFormationStackSetExecutionRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='AWSCloudFormationStackSetExecutionRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to access Customer Account'
        )

        response = client.put_role_policy(
            PolicyDocument=json.dumps(permissions_policy),
            PolicyName='cdw-cloudhealth-readonly-policy',
            RoleName='AWSCloudFormationStackSetExecutionRole'
        )

        print ("AWSCloudFormationStackSetExecutionRole created Successfully")

    else:
        print ("AWSCloudFormationStackSetExecutionRole Already Exists")

    # create the third role and apply the permissions policy
    if  'CDWComputeAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWComputeAccessRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to access Compute service'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/job-function/SystemAdministrator'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWComputeAccessRole'
            )

        print (" CDWComputeAccessRole created Successfully")

    else:
        print ("CDWComputeAccessRole Already Exists")

    # create the fourth role and apply the permissions policy
    if  'CDWStorageAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWStorageAccessRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to access Storage service'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/AmazonS3FullAccess',
        'arn:aws:iam::aws:policy/AmazonGlacierFullAccess',
        'arn:aws:iam::aws:policy/AWSStorageGatewayFullAccess'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWStorageAccessRole'
            )

        print ("CDWStorageAccessRole created Successfully")

    else:
        print ("CDWStorageAccessRole Already Exists")

    # create the fifth role and apply the permissions policy
    if  'CDWNetworkAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWNetworkAccessRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to access Network services'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/job-function/NetworkAdministrator'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWNetworkAccessRole'
            )

        print ("CDWNetworkAccessRole created Successfully")

    else:
        print ("CDWNetworkAccessRole Already Exists")

    # create the sixth role and apply the permissions policy
    if  'CDWDatabaseAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWDatabaseAccessRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to access Database service'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/job-function/DatabaseAdministrator'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWDatabaseAccessRole'
            )

        print ("CDWDatabaseAccessRole created Successfully")

    else:
        print ("CDWDatabaseAccessRole Already Exists")

    # create the seventh role and apply the permissions policy
    if  'CDWCustomerEnrollmentRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWCustomerEnrollmentRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to Enroll'
        )

        CDWCustomerEnrollmentRole_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "iam:CreateRole",
                        "iam:AttachRolePolicy",
                        "iam:CreatePolicy",
                        "cloudformation:CreateStackSet*",
                        "stepfunctions:ListStateMachines",
                        "stepfunctions:StartExecution",
                        "s3:PutObject*"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                }
            ]
        }

        response = client.put_role_policy(
            PolicyDocument=json.dumps(CDWCustomerEnrollmentRole_policy),
            PolicyName='cdw-cloudhealth-readonly-policy',
            RoleName='CDWCustomerEnrollmentRole'
        )

        print ("CDWCustomerEnrollmentRole created Successfully")

    else:
        print ("CDWCustomerEnrollmentRole Already Exists")

    # create the eighth role and apply the permissions policy
    if  'CDWSecurityAccessRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWSecurityAccessRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to security access'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/IAMFullAccess'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWSecurityAccessRole'
            )

        print ("CDWSecurityAccessRole created Successfully")

    else:
        print ("CDWSecurityAccessRole Already Exists")

    # create the Ninth role and apply the permissions policy
    if  'CDWECCAnalystRole' not in roles_list:
        response = client.create_role(
            Path="/",
            RoleName='CDWECCAnalystRole',
            AssumeRolePolicyDocument=json.dumps(my_managed_policy),
            Description='Cross Account role for CDW to ECC Analyst access'
        )

        policy_arn = [
        'arn:aws:iam::aws:policy/ReadOnlyAccess'
        ]
        for policy in policy_arn:
            response = client.attach_role_policy(
                PolicyArn=policy,
                RoleName='CDWECCAnalystRole'
            )

        print ("CDWECCAnalystRole created Successfully")

    else:
        print ("CDWECCAnalystRole Already Exists")

except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)
