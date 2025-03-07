module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "shc-calculator"
  description   = "My awesome lambda function"
  handler       = "src.python.soft_sensors.handler.handle"
  runtime       = "python3.11"

  create_package         = false
  local_existing_package = "../../dist/src.python.soft_sensors/lambda.zip"

  tags = {
    Name = "my-lambda1"
  }
}
