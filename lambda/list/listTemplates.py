# import boto3
# import json

# def list_templates(event, context):
#     # Initialize the SES client
#     ses_client = boto3.client('ses')

#     try:
#         # List the SES templates
#         response = ses_client.list_templates()
        
#         # Extract the template data from the response
#         templates = response.get('TemplatesMetadata', [])
        
#         return {
#             'statusCode': 200,
#             'body': json.dumps({'templates': templates})
#         }
    
#     except Exception as e:
#         # Handle any errors that occur
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }

# def lambda_handler(event, context):
#     return list_templates(event, context)

import boto3
import json
from datetime import datetime

def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()

def list_templates(event, context):
    # Initialize the SES client
    ses_client = boto3.client('ses')

    try:
        # List the SES templates
        response = ses_client.list_templates()
        
        # Extract the template data from the response
        templates = response.get('TemplatesMetadata', [])
        
        # Convert datetime objects to strings
        for template in templates:
            if 'CreatedTimestamp' in template:
                template['CreatedTimestamp'] = datetime_converter(template['CreatedTimestamp'])
            if 'LastUpdatedTimestamp' in template:
                template['LastUpdatedTimestamp'] = datetime_converter(template['LastUpdatedTimestamp'])
        
        return {
            'statusCode': 200,
            'body': json.dumps({'templates': templates})
        }
    
    except Exception as e:
        # Handle any errors that occur
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def lambda_handler(event, context):
    return list_templates(event, context)
