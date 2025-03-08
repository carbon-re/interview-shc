# Soft Sensor Kata

This exercise is designed as a fun toy problem that's similar to the work we do every day on the platform team.

It has a bit of cloud engineering, a bit of TDD, a bit of cement knowledge, a bit of data engineering. You are not expected to understand it all, or to finish the exercise: we want to see how you work when you are in an unfamiliar, complex domain.

Your interviewer is here to help! You can ask them any questions about the code, the problem, or the context. They want to see you do well, because that's more fun for everybody.

There is [some background information](https://carbonre.notion.site/SHC-1ae57d5bd89d80ac8c8bfcf85f264c4e?pvs=74) on our notion site.

Your interviewer will already have a laptop set up, but you may use your own laptop if you wish. For that to work, you will need a few tools.

* Terraform 1.2.3
* The pants launcher (www.pantsbuild.org)
* Python 3.11
* Gnu tools (diff, grep, bash)

Your interviewer can provide an access key and secret so that you can access a sandbox environment.

## The task

You must build a lambda function that:

* Reads a CSV file from S3
* Calculates the specific heat consumption of a cement plant
* Returns the calculated values

## The data

Each cement plant has a CSV file stored in an S3 bucket. The files are in this repository at `src/infra/plant-data`.
Each csv file is accompanied with a README. 
The csvs are readmes are uploaded to an S3 bucket with a random name in the root of the bucket, eg. "$BUCKET_NAME/abc.csv" and "$BUCKET_NAME/abc.README.md"

We suggest starting with `abc.csv` (Al Buraimi Cement).

## The Lambda

Your lambda function will be invoked directly, as though from the AWS console.
The input to the lambda is a json object containing a plant code, eg.

``` json
{
  "plant": "abc"
}
```

The response from your lambda function must be a json object where the keys are timestamps and the values are the calculated specific heat consunption, eg.

``` json
{ 
  "2023-03-01 17:00:00": 812, 
  "2023-03-01 18:00:00": 801, 
  "2023-03-01 19:00:00": 780
}
```

You must round the SHC _down_ to the nearest integer.

## Building code

We use a tool to manage our monorepo. It's called [pants](www.pantsbuild.org), which is an endless source of juvenile humour.

You can build the lambda file by running `pants package ::` in the root of the repository. This will build a zip file containing your source code in `dist`. The zip file will contain the file `src/python/soft_sensors/handler.py`, plus any libraries or files that you import.

## Deploying the lambda

We use terraform to deploy the lambda function, upload the files, and create the S3 bucket.
You can run `terraform apply` from `src/infra` assuming you have credentials for an AWS account.
From the root of the project, you can run `terraform -chdir src/infra apply`. To skip confirmation, add the `-auto-approve` flag. You should avoid doing this on real world projects!

## Testing the lambda

We recommend using unit tests to make sure that your code works as expected. In particular, it is useful to unit test the ShcSoftSensor class. You may not need to test the lambda handler if it is simple.

There is a script under `src/tool` for each plant, that will

* Invoke your lambda function
* Check that the result matches the expected output

eg. `src/tool/test-abc.sh`

If the lambda raises an error, or the output doesn't match, some diagnostic info, including any logs or print statements from your lambda, will be printed to the screen.

## Tips

* It'll be annoying to run `pants package` and `terraform apply` all the time. Can you write a script to make it a single command?
* The lambda function ships with pandas, and a library called [awswrangler](https://aws-sdk-pandas.readthedocs.io/en/latest/stubs/awswrangler.s3.read_csv.html) that makes it easy to read CSV files from S3.
