import boto3  # Import the AWS SDK for Python (Boto3).
import json  # Import the JSON library for parsing JSON.
import logging  # Import the logging module for error logging.

ses_client = boto3.client("ses")  # Create an AWS SES client instance.


def parse_template(event):
    try:
        template_data = json.loads(event["body"])
        print(f"This is template data: {template_data}")

        # Define the required fields for the template.
        required_fields = ["TemplateName", "SubjectPart", "HtmlPart", "TextPart"]

        # Check if all required fields are in the template data.
        if all(field in template_data for field in required_fields):
            return template_data  # Return the template data if valid.
        else:
            logging.error(
                "Invalid or missing template parameters"
            )  # Log error for missing/invalid fields.
            return None  # Return None to indicate an error.
    except json.JSONDecodeError as e:  # Handle JSON parsing errors.
        logging.error(
            f"Invalid JSON format in request body: {e}"
        )  # Log the specific JSON error.
        return None
    except KeyError as e:  # Handle missing keys in the data.
        logging.error(f"Missing key: {e}")  # Log the specific missing key.
        return None


def create_template(template_data):
    try:
        # Call AWS SES to create an email template with the provided data.
        response = ses_client.create_template(Template=template_data)
        # Return a success response with a status code and message.
        return {
            "statusCode": "200",
            "body": json.dumps({"message": "Template created successfully"}),
        }
    except Exception as e:  # Catch any exceptions during template creation.
        logging.error(f"Error creating template: {e}")  # Log the error.
        # Return an error response with a status code and message.
        return {
            "statusCode": "500",
            "body": json.dumps({"message": "Could not create template"}),
        }


def lambda_handler(event, context):
    parsed_template_data = parse_template(event)  # Parse the incoming template data.

    if parsed_template_data:
        # If parsing is successful, create the template.
        return create_template(parsed_template_data)
    else:
        # If parsing fails, return an error response.
        return {
            "statusCode": "400",
            "body": json.dumps({"message": "Failed to parse template"}),
        }
