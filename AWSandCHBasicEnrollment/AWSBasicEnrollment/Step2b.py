'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
from botocore.exceptions import ClientError

try:
    # this code writes a new profile to the AWS config file to allow BlueMoon to use the CDWCustomerAccountAccessRole
    # to administer customer resources in the target environment

    # this next section creates a stack instance from the BlueMoon account to run in the target account
    client = boto3.client('s3')
    
    response = client.put_object(
        ACL='public-read',
        Body="config.json",
        Bucket="cft-crossaccount-organizationaccessrolev2",
        Key="config.json"
    )
   
except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)