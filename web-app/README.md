# Streamlit Web Application Homework 3

This document will be a quick guideline of how I ran my streamlit applications.

## Repository Structure

```
423-2024-hw3-mnk1906/
│
├── dockerfiles/
│   ├── Dockerfile
├── src/
│   ├── app.py
│   ├── aws_import.py
│   ├── generate_features.py
├── config/
│   ├── config.yaml
│   ├── logging/
│       └── local.conf
├── tests/
│   ├── unit_test.py
├── joblib_folder/
│   ├── gb_model.joblib
│   ├── rf_model.joblib
└── requirements.txt
```

- `config`: Main config and logging command center.
- `dockerfiles`: File that is used to buid image and run the image. This is for `pipeline.py`.
- `src`: Contains all source codes to power-up the `app.py`, also inside `src`, and `test_modules.py` under `tests` folder.
- `joblib_folder`: Reference of the models I previously saved using joblib in homework 2. I used the two models for my homework 3.
- `tests`: Contains another Dockerfile for Unit Testing purpose, and `test_modules.py` for unit testing.

In order to run streamlit here are some pre-steps to undertake:

#### Git clone the repository

```bash
git clone https://github.com/MSIA/423-2024-hw3-mnk1906.git
cd MLDS-423-HW2
```

#### AWS SSO Configuration

```bash
aws configure sso --profile default
```

Ensure that you are using the same SSO session that you created the first time.

```bash
aws sso login --profile default
```

**Important Note**:
- This document assumes that you have 2 joblib files located in the tested s3 bucket from Homework 2.
- If you have the bucket from s3 that you used for a test in HW2, please download the two files inside `joblib_folder` and move them to the s3.
- In addition, ensure to update your bucket under `config` `bucket_name`.

### AWS IAM Instance Role
Ensure that you have IAM EC2 Instance Role set up so that you will have rights to access S3, ECR, and ECS.

For the convenience purpose, I set the IAM Role name as `hw3-streamlit` that has Administrator Access.

## Docker + AWS Combination

### If requires test in Docker

```bash
docker build -t hw3-streamlit -f ./dockerfiles/Dockerfile .
```

```bash
docker run -v ${HOME}/.aws/:/root/.aws/ --platform=linux/x86_64 -p 80:80 --name streamlit_app hw3-streamlit
```

Because this is under docker, not local, you will not be able to access. We will now move onto ECR and ECS for construction.

### ECR

To build the streamlit image, I ran these commands step-by-step:

```bash
docker build -t hw3-streamlit -f ./dockerfiles/Dockerfile .
```

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/j7z5l7y2
```

I called my ECR repostiory as `homework3_streamlit`. I created a new repostiroy directly in AWS.

This sets up my connection to the newly created public ECR in my AWS account. Depending on your sso configuration and the
existence of your repository, you will have to adjust this part accordingly as the unique access id will be different.

From Docker Image, I tagged the local docker image into AWS ECR

```bash
docker tag hw3-streamlit public.ecr.aws/j7z5l7y2/homework3_streamlit:latest
```

Finally, I pushed the change into the existing ECR repository.

```bash
docker push public.ecr.aws/j7z5l7y2/homework3_streamlit:latest
```

### ECS

For this purpose, I created a new cluster called `hw3-streamlit-v2` in ECS.
- Make sure you create new Security Group with Northwestern VPN IP `165.124.160.0/21`.
    - Make sure you are giving an access to HTTP port 80 in Dockerfile.
    - Also, ensure that you give an access to FARGATE.

Then, I created a new Task Definition, calling it `hw3-web-app`.
- If you have your own SSH Key Pair, I will recommend matching it.
- I created Task Execution Role that gives an authority to use S3, ECS, ECR.
- I called the container as `ecs-hw3-task`.
- Set up the port as 80 as noted in Dockerfile in Port Mappings, calling it `hw3-port`.
- I added Key-Value pair of `BUCKET_NAME` and `mnk1906-clouds` in Environment Variable.

Finally, create a service for `hw3-web-app`. I called it `hw3-service`.
- For ECS, I ensured to use `FARGATE` with streamlit application, instead of EC2.
- When I tried to instruct ECS to create an environment with EC2, the created URL address failed to redirect me to the web application.

Once it looks good, I will be able to access the open address set in Networking to the Streamlit Web Application.

## Unit Testing

I applied two happy paths and two unhappy paths for both cases.
I primarly focused on testing `generate_features.py` and `aws_import.py` for the testing purpose.

```bash
pytest test/unit_test.py
```

You will be able to verify defined functions went through the pytest accordingly, and they are not showing any potential Error and confirm that pytest worked.