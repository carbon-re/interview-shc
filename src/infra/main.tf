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

resource "aws_s3_bucket" "this" {
  bucket_prefix = "cre-data-shc"
  force_destroy = true
}


resource "aws_s3_object" "this" {
  bucket = aws_s3_bucket.this.bucket
  key    = "abc.csv"
  source = "plant-data/abc.csv"
}
