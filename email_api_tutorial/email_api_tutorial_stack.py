from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from constructs import Construct
import yaml
import json


class EmailApiTutorialStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an IAM role for the Lambda function
        lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        # Attach the AdministratorAccess policy to the role
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        # Define create email template lambda resource
        create_email_lambda = _lambda.Function(
            self,
            "CreateEmailfxn",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="create_template.lambda_handler",
            code=_lambda.Code.from_asset("lambda/create"),
            role=lambda_role,
        )

        # Define send email template lambda resource
        send_email_lambda = _lambda.Function(
            self,
            "SendEmailfxn",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="send_templatedemail.lambda_handler",
            code=_lambda.Code.from_asset("lambda/send"),
            role=lambda_role,
        )

        # Define list template lambda resource
        list_templates_lambda = _lambda.Function(
            self,
            "ListTemplatesfxn",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="listTemplates.lambda_handler",
            code=_lambda.Code.from_asset("lambda/list"),
            role=lambda_role,
        )

        # Define get template lambda resource
        get_template_lambda = _lambda.Function(
            self,
            "GetTemplatefxn",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="get_template.lambda_handler",
            code=_lambda.Code.from_asset("lambda/get"),
            role=lambda_role,
        )

        # Define the REST API
        api = apigw.RestApi(
            self, "DeploymentSatgesAPI", rest_api_name="TestExportApi", deploy=False
        )

        # Create Resources
        templates = api.root.add_resource("templates")
        send = api.root.add_resource("send")
        templates_1 = templates.add_resource("{templateName}")

        # Add Methods
        templates.add_method("GET", apigw.LambdaIntegration(list_templates_lambda))
        templates.add_method("POST", apigw.LambdaIntegration(create_email_lambda))
        send.add_method("POST", apigw.LambdaIntegration(send_email_lambda))
        templates_1.add_method("GET", apigw.LambdaIntegration(get_template_lambda))

        # #Define lambda authorizer
        # authorizer_lambda = _lambda.Function(
        # self, "lambda_authorizern", runtime=_lambda.Runtime.PYTHON_3_10,
        # handler='lambda_auth.lambda_handler',
        # code = _lambda.Code.from_asset('lambda/send')
        # )

        # integration: apigw.Integration

        # # Read and process the OpenAPI specification
        # with open('openApi/openapispec.yml', 'r') as file:
        #     openapi_spec = yaml.safe_load(file)

        # # Replace placeholders with actual Lambda ARN and region
        # openapi_spec = json.loads(json.dumps(openapi_spec).replace('${lambdaArn}', list_templates_lambda.function_arn))
        # openapi_spec = json.loads(json.dumps(openapi_spec).replace('${region}', self.region))

        # # Define the API Gateway using the modified OpenAPI specification
        # api = apigw.SpecRestApi(
        #     self, "listtemps",
        #     api_definition=apigw.ApiDefinition.from_inline(openapi_spec)
        # )
