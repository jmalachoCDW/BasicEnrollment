'''
Created on Nov 13, 2018

@author: jmalach
'''
import boto3
import sys

parameters=sys.argv

account = parameters[1]
account = account[account.find("=")+1:]

profile = parameters[2]
profile = profile[profile.find("=")+1:]


from botocore.exceptions import ClientError

# does the AWS account exist in CloudHealth already - true or false
newaccount = parameters[3]
arn = "arn:aws:states:us-east-2:"+account+":stateMachine:CloudHealth-Basic-Enrollment"

input_line="{\"role\":\"CDW-CH-ReadOnly-Role\",\"account\":\""+account+"\",\"newaccount\":"+newaccount+"}"

try:
    # in order to start the state machine execution the user needs to user the profile in the AWS config
    # file to use the CDWClientAccountAccessRole
    
    session = boto3.Session(profile_name=profile)
    client = session.client('stepfunctions')
    
    response = client.start_execution(
        stateMachineArn=arn,
        name='CreateLinktoCH-3',
        input=input_line
    )
    print ("State Machine sucessfully started")
    
except ClientError as e:
    print ("Unexpected Error:", e)
    errorText = e.response['Error']['Message']
    print ("Error Text: ", errorText)