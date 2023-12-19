import aws_cdk as core
import aws_cdk.assertions as assertions

from email_api_tutorial.email_api_tutorial_stack import EmailApiTutorialStack

# example tests. To run these tests, uncomment this file along with the example
# resource in email_api_tutorial/email_api_tutorial_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EmailApiTutorialStack(app, "email-api-tutorial")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
