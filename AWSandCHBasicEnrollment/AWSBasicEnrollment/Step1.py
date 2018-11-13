'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
import sys
from botocore.exceptions import ClientError

try: 
    parameters=sys.argv
    profile = parameters[1]
    emailId = parameters[2]
    accountName = parameters[3]
    roleName = parameters[4]
    iamUserAccessToBilling = parameters[5]
    
    session = boto3.Session(profile_name=profile)
    client = session.client('organizations')
    
    # create account code  
    response = client.create_account(Email = emailId, AccountName = accountName, RoleName = roleName, IamUserAccessToBilling = iamUserAccessToBilling)
    
    # manually create the response dict object for testing downstream code
    # response = {"CreateAccountStatus":{"Id":"car-23cb28e0e20911e89dd950d5029d06f1","AccountName":"Test customer 2","State":"IN_PROGRESS","RequestedTimestamp":"2002-12-25 00:00:00-06:39","CompletedTimestamp":"2002-12-25 00:00:00-06:39","AccountId":"123456789123","FailureReason":""}}
    #response = {"CreateAccountStatus":{"Id":"car-f36663c0d96811e880da50d50297c2c5","AccountName":"Test customer 2","State":"IN_PROGRESS","RequestedTimestamp":"2002-12-25 00:00:00-06:39","CompletedTimestamp":"2002-12-25 00:00:00-06:39","AccountId":"123456789123","FailureReason":""}}
    
    
    # response object contains Id, AccountName, AccountId and State which we capture here
    Id = response['CreateAccountStatus']['Id']
    AccountName = response['CreateAccountStatus']['AccountName']
    # AccountId may take upto 5 minutes to create - therefore we now check it in a second call
    # AccountId = response['CreateAccountStatus']['AccountId']
    State = response['CreateAccountStatus']['State']

    print (Id)

except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)
