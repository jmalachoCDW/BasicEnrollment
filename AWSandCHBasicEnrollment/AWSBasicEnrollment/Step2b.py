'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
from botocore.exceptions import ClientError

try:
    # this code copies the new config.json file to the CFT bucket for use by the state machine
    # the object is made public read to allow for all linked accounts to read the file
    
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