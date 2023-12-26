import boto3
import json


def get_template(event, context):
    ses_client = boto3.client("ses")
    template_name = event["pathParameters"]["templateName"]

    try:
        response = ses_client.get_template(TemplateName=template_name)
        template = response["Template"]

        return {"statusCode": 200, "body": json.dumps(template)}
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving template"}),
        }


def lambda_handler(event, context):
    return get_template(event, context)
