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

- Do a terraform init in the src/infra directory. If you are running on your own
  machine you can use a profile:

  ```sh
  AWS_PROFILE=sandbox-interview.Platform terraform -chdir=src/infra init
  ```

  Or if you are running on the interviewee's machine get AWS environment variables
  for the `sandbox-interview` account from the AWS SSO access portal and set them
  in their environment, then run:

  ```sh
  terraform -chdir=src/infra init
  ```

- `terraform destroy` any existing stuff
- Create a branch for your candidate to work on. Remember to commit often and push.

## Getting started

- Package the lambda and run terraform apply to deploy the lambda function
- The script `src/tool/test-hello-world.sh` will invoke the lambda with no args and print its response

## Creating a virtualenv

There's a pants alias `export_venv` that will export the python deps into dist. Personally, I set it up with

```terminal
$ pants export_venv

17:36:18.55 [INFO] Completed: Build pex for resolve `python-default`
Wrote symlink to immutable virtualenv for python-default (using Python 3.11.11) to dist/export/python/virtualenvs/python-default/3.11.11

$ ln -sf $PWD/dist/export/python/virtualenvs/python-default/3.11.11 ~/.pyenv/versions/shc

soft-sensor-kata on  main [$!] on ☁️  (eu-west-2)
$ pyenv local shc
```

But your mileage may vary, especially if you're mucking about with one of those Apple thingies. Once you have that venv in pyenv, you should be able to use it in vscode, but I've not tested that cos emacs.
