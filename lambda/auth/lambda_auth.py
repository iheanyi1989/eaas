import json
import uuid
import logging 

def check_auth(event, context):
    try:
        headers = event['headers']
        stage_variables = event['stageVariables']
        query_string_params = event['queryStringParameters']

        if (headers["HeaderAuth1"] == "headerValue1" and 
            stage_variables["StageVar1"] == "stageValue1" and 
            query_string_params["QueryString1"] == "queryValue1"):
            return pass_auth()
        else:
            return fail_auth()

    except KeyError as e:
        logging.error(f"Missing key in event: {e}")
        return fail_auth()

def pass_auth():
    arn = "arn:aws:execute-api:us-east-1:123456789012:3az8ghhm0l/testauth/*/*"
    response = {
        "principalId": f"{uuid.uuid4().hex}",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Action": "execute-api:Invoke",
                "Effect": "Allow",
                "Resource": arn
                }
            ]
        }
    }
    return response
    
def fail_auth():
    arn = "arn:aws:execute-api:us-east-1:123456789012:3az8ghhm0l/testauth/*/*"
    response = {
        "principalId": f"{uuid.uuid4().hex}",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Action": "execute-api:Invoke",
                "Effect": "Deny",
                "Resource": arn
                }
            ]
        }
    }
    return response
        
        
def lambda_handler(event, context):
    try:
       return check_auth(event)
       
    except Exception as e:
        logging.error(f"Error in Lambda authorizer: {e}, Event: {json.dumps(event)}")
        raise  # Reraise the exception after logging