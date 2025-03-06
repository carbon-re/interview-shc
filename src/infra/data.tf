data "archive_file" "lambda_zip" {
  type = "zip"

  # Note: this includes both .py files and the contents of site-packages if you're installing dependencies.
  # Adjust the "source_file" / "source_dir" below as needed.
  source_dir  = "${path.module}/../../dist/"
  output_path = "${path.module}/lambda.zip"
}
