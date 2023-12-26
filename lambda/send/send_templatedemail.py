import boto3  # Import the AWS SDK for Python.
import json  # Import the JSON library for handling JSON data.
import logging  # Import the logging module for error logging.

ses_client = boto3.client(
    "ses"
)  # Create a client to interact with the AWS Simple Email Service (SES).


def check_templated_email(event, context):
    try:
        templated_email = json.loads(event["body"])
        print(f"This is templated email: {templated_email}")

        # Define the required fields for the email template.
        required_fields = ["Source", "TemplateData", "Template", "Destination"]

        # Check if all required fields are present.
        if all(field in templated_email for field in required_fields):
            print(templated_email)  # Print the template data for debugging.
            return templated_email  # Return the validated template data.
        else:
            # Log an error if required fields are missing.
            logging.error("Missing Required parameter in templated")
            return None
    except json.JSONDecodeError as e:
        # Log JSON parsing errors.
        logging.error(e)
        return None
    except KeyError as e:
        # Log errors related to missing keys.
        logging.error(e)
        return None


def send_email(templated_email):
    try:
        # Use the SES client to send an email using the provided template.
        response = ses_client.send_templated_email(
            Source=templated_email["Source"],
            Destination=templated_email["Destination"],
            TemplateData=templated_email["TemplateData"],
            Template=templated_email["Template"],
        )
        # Return a success response if the email is sent.
        return {
            "statusCode": "200",
            "body": json.dumps({"message": "Email Sent successfully"}),
        }
    except Exception as e:
        # Log any errors encountered during email sending.
        logging.error(f"there was a problem, message not sent: {e}")
        return None


def lambda_handler(event, context):
    # Validate the email template data.
    validated_template = check_templated_email(event, context)
    if validated_template:
        # If validation is successful, send the email.
        return send_email(validated_template)
    else:
        # Return an error response if validation fails.
        return {
            "statusCode": "400",
            "body": json.dumps({"message": "Failed to validate template"}),
        }
