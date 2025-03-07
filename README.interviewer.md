# Setup

We have a separate AWS Account for interviews "sandbox-interview" with account id 345594584316.
You should be able to access it with AWS SSO.

The repository is configured with pants, using the aws_lambda backend.
Pants package will create a lambda.zip in dist.

Terraform is set up with serverless.tf to deploy that zip file.


## Before starting

-  Do a terraform init in the src/infra directory.
- `terraform destroy` any existing stuff

## Getting started

- Package the lambda and run terraform apply to deploy the lambda function
- The script `src/tool/test-hello-world.sh` will invoke the lambda with no args and print its response

## Tips

- It will be annoying to remember to pants package then deploy. Consider scripting it.

