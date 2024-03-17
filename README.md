
# Serverless LLM - Text Embeddings Inference

This is a proof-of-concept (PoC) where I adapted TEI (Text Embedding Inference) framework to run as a serverless application in AWS Lambda. You can find more information about this project here.


## Results

We conducted an experiemnt to evaluate the effectiveness of this PoC. The experiment consisted of the following steps:

- The intfloat/multilingual-e5-small was chosen as the embedding model.
- We sent A 600-hundred token text to the model and measured the time to return its result.
- We took two differents measurements with this 600-hundred token text processing time - the time spent with cold-start and without it.
- With the processing time in hands, we determined (1) the cost per million tokens processed (assuming 10% of executions with cold-start and 90% without) and (2) how many tokens can be processed per month for free with AWS quota.


|    Model   | Time w/coldstart | Time w/o coldstart | Free M tokens/month | Cost/M tokens |
|:----------:|-----------------:|-------------------:|--------------------:|--------------:|
|  E5 small  |               4 s |             300 ms |                17.8 |        $0.03  |


# Running on AWS

Considering that you have configured AWS CLI on your computer, use the following steps to deploy:

<details>
<summary>Build docker image</summary>
First, download this repo and build its docker image, setting which model you want to use:

```sh
docker buildx build --build-arg MODEL_ID=<model_id> --platform linux/amd64 --tag <account_id>.dkr.ecr.<region>.amazonaws.com/<ecr_repo_name>:latest . 
```

This command can take several minutes since TEI is a Rust framework and needs to compile everything.
</details>

<details>
<summary>Pull image to AWS</summary>

Login at AWS ECR, create the image repository, and pull the build:

```sh
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com  

aws ecr create-repository --repository-name <ecr_repo_name> --region <region>

docker push <account_id>.dkr.ecr.<region>.amazonaws.com/<ecr_repo_name>:latest  
```
</details>

<details>
<summary>Create Lambda</summary>

Create the Lambda service and its role:

```sh
aws iam create-role --role-name lambda-basic-execution --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "lambda.amazonaws.com"},"Action": "sts:AssumeRole"}]}'   
 
aws lambda create-function --region <region> --function-name tei_test --package-type Image --code ImageUri=<account_id>.dkr.ecr.`<region>`.amazonaws.com/<ecr_repo_name>:latest   --role arn:aws:iam::<account_id>:role/lambda-basic-execution --environment "Variables={MODEL_ID=<model_id>" --timeout <timeout> --memory-size <memory>
```
</details>
<br />

# Running locally

<details>
<summary>Build & Run</summary>
In one terminal, execute:

```sh
docker buildx build --build-arg MODEL_ID=`<model_id>` --platform linux/amd64 --tag serverless_tei_test . 

docker run -e MODEL_ID=`<model_id>` --rm -p 9000:8080 --name serverless_tei_test serverless_tei_test
```
</details>

<details>
<summary>Calling the service</summary>
And in the other:

```sh
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations -H 'Content-Type: application/json' -d '{"inputs":["First text", "Second text"]}' | python3 -m json.tool
```
</details>
<br />

# Next steps

Let's hope Hugging Face implements this kind of feature at TEI. Or you can help me transform this PoC into a fully functional application. You are more than welcome to contribute.