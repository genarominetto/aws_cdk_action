#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks.my_cdk_stack import MyCdkProjectStack


app = cdk.App()
MyCdkProjectStack(app, "MyCdkProjectStack",
    # Specialize this stack for the AWS Account and Region
    # that are implied by the current CLI configuration.
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
    )

app.synth()
