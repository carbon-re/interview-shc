# Setup

We have a separate AWS Account for interviews "sandbox-interview" with account id 345594584316.
You should be able to access it with AWS SSO.

The repository is configured with pants, using the aws_lambda backend.
Pants package will create a lambda.zip in dist.

Terraform is set up with serverless.tf to deploy that zip file.

You'll need to attach a bucket policy for the lambda to read data. Just use the [Read Only managed policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonS3ReadOnlyAccess.html). There's an example of doing that in the [serverless.tf repo](https://github.com/terraform-aws-modules/terraform-aws-lambda/blob/master/examples/complete/main.tf#L155C1-L156C69)

You're also going to want to pass the bucket as an env var to the lambda, or ... hardcode it after getting it out of terraform state or something. Example again [here](https://github.com/terraform-aws-modules/terraform-aws-lambda/blob/master/examples/complete/main.tf#L50).

Bear in mind that your candidate may not have any AWS experience, or Terraform experience, so be prepared to baby step them if necessary. You don't need to go to the AWS console or understand much, so long as you package, deploy, and then run the test scripts.

See what they _do_ know. Make conversation. Let them ask questions and get stuck, but don't let them fall into a pit of despair.

## Before starting

-  Do a terraform init in the src/infra directory.
- `terraform destroy` any existing stuf
-  Create a branch for your candidate to work on. Remember to commit often and push.

## Getting started

- Package the lambda and run terraform apply to deploy the lambda function
- The script `src/tool/test-hello-world.sh` will invoke the lambda with no args and print its response
