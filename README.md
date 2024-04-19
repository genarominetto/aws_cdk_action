# Introduction

**Define your cloud application resources using Python and automate their deployment using the AWS CDK, GitHub Actions, and Docker. The Project Structure includes components such as the application script, Docker configuration files, and the CDK deployment workflow. The Tutorial section guides developers through the setup and deployment processes, from creating an AWS IAM user to managing access keys and configuring the deployment region.**

# Table of Contents

- [Project Structure](#project-structure)
- [Tutorial](#tutorial)
    - [Fork the Repository](#fork-the-repository)
    - [Create an IAM User](#create-an-iam-user)
    - [Attach Policies](#attach-policies)
        - [Option 1: Attach managed policies directly (Not Recommended)](#option-1-attach-managed-policies-directly-not-recommended)
        - [Option 2: Attach custom policies](#option-2-attach-custom-policies)
    - [Save Your Access Keys](#save-your-access-keys)
    - [Store Keys as GitHub Secrets](#store-keys-as-github-secrets)
    - [Configure the Region](#configure-the-region)
    - [Bootstrap](#bootstrap)
    - [Trigger the Workflow](#trigger-the-workflow)
    - [View the Stack in the AWS Console](#view-the-stack-in-the-aws-console)
- [Contributing](#contributing)

# Project Structure

```
.
├── app.py
├── cdk.json
├── .github
│   ├── Dockerfile
│   ├── setup.sh
│   └── workflows
│       └── cdk-deploy.yml
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── stacks
│   ├── __init__.py
│   └── my_cdk_stack.py
└── tests
    ├── __init__.py
    └── unit
        ├── __init__.py
        └── test_my_cdk_project_stack.py

```

# TUTORIAL

# Fork the Repository

To start using this project, fork the repository to create a personal copy.

- At the top-right of the page, you will see a button labeled "Fork". Click on this button.
- GitHub will then create a copy of the repository under your GitHub account, effectively creating a fork.

# Create an IAM User

Create a new IAM user in your AWS account.

- **Navigate** to the **AWS Management Console**.
- **Type "IAM"** in the search bar and **select it**.
- Go to **"Users"** and click on **"Create user"**.
- Name the user `my_new_user`  or any other name of your choice.

# Attach Policies


### Option 1: Attach Managed Policies Directly (Not recommended)
⚠️ **Warning**

When you give a user full access to IAM, there is no limit to the permissions that user can grant to him/herself or others. The user can create new IAM entities (users or roles) and grant those entities full access to all resources in your AWS account. When you give a user full access to IAM, you are effectively giving them full access to all resources in your AWS account. This includes access to delete all resources. You should grant these permissions to only trusted administrators, and you should enforce multi-factor authentication (MFA) for these administrators.

To attach these policies:
1. Select the newly created user.
2. Click on **Add permissions**.
3. Click on **Attach policies directly**.
4. Select the following policies from the list of available policies:
   - `AmazonS3FullAccess`
   - `AmazonSQSFullAccess`
   - `AmazonSSMReadOnlyAccess`
   - `AWSCloudFormationFullAccess`
   - `AWSCodeDeployFullAccess`
   - `IAMFullAccess`

### Option 2: Attach Custom Policies

Instead of using broad, predefined permissions, create custom policies tailored to the specific needs of your tasks and projects. This approach enhances security by strictly limiting access according to the principle of least privilege. Once these custom policies are crafted, attach them to a group and then add users to this group. This method consolidates policy management and streamlines user permissions oversight. For more detailed instructions on creating and managing custom policies, refer to the [AWS IAM permissions delegation documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_delegate-permissions_examples.html).



# Save Your Access Keys

- Find the newly created user.
- Click on **"Create access key"**.
- **Select the CLI option** and acknowledge the recommendations.

# Store Keys as GitHub Secrets

To securely store your AWS access keys in GitHub:

1. Go to your repository on GitHub.
2. Click on **Settings** at the top-right of the page.
3. On the left sidebar, expand the dropdown menu called **Secrets and variables**.
4. Click on **Actions**.
5. Click on **New repository secret**.
6. Name the secrets as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` respectively and paste their values into the fields provided.

# Configure the Region

To specify the AWS region for your CDK deployment, update the `setup.sh` file. This configuration ensures that your AWS resources deploy to the intended geographical region. Follow these steps to modify the region setting:

1. Open the `setup.sh` file located in the `.github` directory.
2. Find the line that configures the region. It will look like this:
   ```bash
   aws --profile default configure set region "us-east-1"
   ```
3. Replace "us-east-1" with your desired AWS region code.
4. Save the changes to the `setup.sh` file.

By setting the region in the `setup.sh` script, you control where AWS deploys the resources for your project. This change will take effect the next time you trigger the deployment workflow.


# Bootstrap

Before deploying cloud applications with the AWS Cloud Development Kit (CDK) in a new region, you must bootstrap your environment. This setup process prepares necessary resources like an S3 bucket for storing assets and IAM roles for CDK operations.

### Bootstrap Command
Use the command below to bootstrap your AWS environment:

```
cdk bootstrap aws://ACCOUNT_ID/REGION
```

- **ACCOUNT_ID**: Replace with your AWS account ID, a 12-digit number found in your account settings or user ARN.
- **REGION**: Specify the AWS region code, e.g., `us-east-1`.

Example for account ID `123456789012` and the region `us-east-1`:

```
cdk bootstrap aws://123456789012/us-east-1
```

### Options for Bootstrapping
1. **Locally**: Run the bootstrap command from your local machine with AWS CLI configured.
2. **Via setup.sh**: Temporarily add the bootstrap command to your `setup.sh` script used in GitHub Actions. `setup.sh` is located at `.github`. Remove the command after initial setup.

Bootstrapping is essential for the first-time deployment of a CDK stack in any AWS region to ensure your infrastructure manages resources effectively.

# Trigger the Workflow

The GitHub Action workflow `cdk-deploy.yml` automates the deployment of the AWS CDK stack and triggers on any push that modifies `app.py` or any files within the `stacks/**` directory.

### Workflow Details

The workflow operates on an Ubuntu latest environment and includes these steps:

1. **Checkout**: Retrieves the latest code using `actions/checkout@v2`.
2. **Build Docker Image**: Constructs a Docker image named `mycdkproject` from the Dockerfile located at `.github/Dockerfile`. This Dockerfile uses Alpine Linux as the base.
3. **Run Docker Container**: Runs the Docker container with `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` set from the repository secrets. It executes the `setup.sh` script within the container.

### About the setup.sh Script

The `setup.sh` script configures the environment for the AWS CDK deployment:


1. Link Python and pip to version 3 and install all required Python packages including `aws-cdk-lib`, `constructs`, and dependencies from `requirements.txt`.
2. Configure AWS CLI settings for the "us-east-1" region with JSON output.
3. Synthesize and deploy the CDK stack to AWS using `cdk synth` and `cdk deploy`.


To initiate this workflow, commit changes to `app.py` or any files in the `stacks` directory and push them to your GitHub repository.


# View the Stack in the AWS Console

After the deployment completes, you can view the status and configuration of your CDK stack in the AWS Management Console. Here are the steps to locate and review your deployed stack:

1. Log into your **AWS Management Console**.
2. Navigate to **CloudFormation**.
3. Click on **MyCdkProjectStack** to open the stack's overview.
4. Select the **Resources** tab to view all the resources associated with the stack, such as `MyCdkProjectQueue`.
5. If you do not see the expected resources, ensure that the region at the top-right of the console is set to **us-east-1** (or the region you have configured your stack for).
6. If the resources are still not visible, review the logs of the GitHub Action to check for any deployment errors.

These steps will help you verify the deployment and ensure that the AWS CDK stack is configured and running as expected.


# Contributing

To contribute to this project, please fork the repository, make your changes, and submit a pull request.
