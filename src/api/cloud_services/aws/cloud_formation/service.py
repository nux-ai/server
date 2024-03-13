from troposphere.awslambda import Function, Code
from troposphere import Template, GetAtt, Ref, Sub, Parameter, Output
import json
import boto3
from troposphere.stepfunctions import StateMachine
from troposphere.iam import Role, Policy
from troposphere.awslambda import Function, Code, LayerVersion
from troposphere import Ref, Sub, Template, GetAtt, Parameter, Output
from config import nux_aws_creds as creds

from cloud_services.aws.s3 import S3Class

from utilities.helpers import generate_function_name


class CloudFormationHandler:
    def __init__(self, state_machine_name="hi"):
        self.state_machine_name = state_machine_name
        self.region = creds['region']
        self.account_id = creds['account_id']

        self.session = boto3.Session(
            aws_access_key_id=creds['aws_access_key'],
            aws_secret_access_key=creds['aws_secret_key'],
            region_name=self.region
        )
        # self.bucket_name = bucket_name

        self.client = self.session.client('cloudformation')

    def create_step_function(self):
        generator = CloudFormationTemplateGenerator()
        template_yaml = generator.generate_template()

        response = self.client.create_stack(
            StackName='YourStackName',
            TemplateBody=template_yaml,
            Parameters=[
                {
                    'ParameterKey': 'S3BucketName',
                    'ParameterValue': "Name of the S3 bucket containing Lambda function packages"
                },
            ],
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ],
        )

        print(response)

    def invoke_step_function(self):
        execution_response = self.session.start_execution(
            stateMachineArn=f"arn:aws:states:{self.region}:{self.account_id}:stateMachine:{self.state_machine_name}",
            input=json.dumps({
                "foo": "bar"
            })
        )
        return execution_response

    def get_stack_status(self, stack_name="hi"):
        # Retrieve the stack's details
        response = self.client.describe_stacks(StackName=stack_name)
        # Assuming the stack exists and there's only one stack with this name,
        # extract the stack status
        stack_status = response['Stacks'][0]['StackStatus']
        return stack_status


class CloudFormationTemplateGenerator:
    def __init__(self):
        self.template = Template()
        self.template.set_description(
            "Creates Lambda functions and a Step Function to orchestrate them.")

    def add_parameters(self):
        self.s3_bucket_name_param = self.template.add_parameter(Parameter(
            "S3BucketName",
            Description="Name of the S3 bucket containing Lambda function packages.",
            Type="String",
        ))

    def add_resources(self):
        self.add_lambda_execution_role()
        self.add_lambda_function()
        self.add_step_function_execution_role()
        self.add_state_machine()

    def add_lambda_execution_role(self):
        self.lambda_execution_role = self.template.add_resource(Role(
            "LambdaExecutionRole",
            AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }],
            },
            Policies=[Policy(
                PolicyName="LambdaExecutionPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": "logs:*",
                        "Resource": "arn:aws:logs:*:*:*",
                    }],
                },
            )],
        ))

    def add_lambda_function(self):
        # Adjust this to your specific function name
        function_name = "CYR3mIMfzM-4c14fa-976cf3dd-convert_file"

        self.lambda_function = self.template.add_resource(Function(
            "LambdaFunction1",
            FunctionName=function_name,
            # Ensure this matches your code's handler
            Handler=f'{function_name}.handler',
            Role=GetAtt(self.lambda_execution_role, "Arn"),
            Runtime="python3.10",  # Ensure this matches your Lambda's runtime
            Code=Code(
                S3Bucket="nux-api-python-packages",  # Directly specify the bucket name
                S3Key="CYR3mIMfzM-4c14fa-976cf3dd-convert_file.zip"
            )
        ))

    def add_step_function_execution_role(self):
        self.step_function_execution_role = self.template.add_resource(Role(
            "StepFunctionExecutionRole",
            AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "states.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }],
            },
            Policies=[Policy(
                PolicyName="StepFunctionExecutionPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": "lambda:InvokeFunction",
                        "Resource": "*",
                    }],
                },
            )],
        ))

    def add_state_machine(self):
        definition = {
            "StartAt": "Function1",
            "States": {
                "Function1": {
                    "Type": "Task",
                    "Resource": "${LambdaFunctionArn}",
                    "End": True,
                    "Retry": [
                        {
                            "ErrorEquals": [
                                "Lambda.ClientExecutionTimeoutException",
                                "Lambda.ServiceException",
                                "Lambda.AWSLambdaException",
                                "Lambda.SdkClientException"
                            ],
                            "IntervalSeconds": 2,
                            "MaxAttempts": 6,
                            "BackoffRate": 2
                        }
                    ]
                }
            }
        }

        definition_string = Sub(json.dumps(definition), {
            "LambdaFunctionArn": GetAtt(self.lambda_function, "Arn")
        })

        self.state_machine = self.template.add_resource(StateMachine(
            "MyStateMachine",
            RoleArn=GetAtt(self.step_function_execution_role, "Arn"),
            DefinitionString=definition_string,
        ))

    def add_outputs(self):
        self.template.add_output(Output(
            "StepFunctionArn",
            Description="ARN of the Step Function",
            Value=Ref(self.state_machine),
        ))

    def generate_template(self):
        self.add_parameters()
        self.add_resources()
        self.add_outputs()
        return self.template.to_yaml()

# Example usage:
# generator = CloudFormationTemplateGenerator()
# template_yaml = generator.generate_template()
# print(template_yaml)
