from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    App,
    Tags,
    Environment,
    aws_ssm as ssm
)
from constructs import Construct

class EC2SSMSessionManagerStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Use configuration from the passed dictionary
        ami = config["ami_type"]
        instance_type = config["instance_type"]

        # Create or use an existing VPC
        if config["vpc_id"]:
            vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=config["vpc_id"])
        else:
            vpc = ec2.Vpc(self, "VPC")

        # IAM role for the EC2 instance
        role = iam.Role(self, "InstanceSSMRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(policy) for policy in config["role_policies"]])

        # Security Group
        sg = ec2.SecurityGroup(self, "SecurityGroup",
                               vpc=vpc,
                               description=config["sg_description"],
                               allow_all_outbound=True)
        sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(443))

        # EC2 instance
        ec2_instance = ec2.Instance(self, "Instance",
                                    instance_type=ec2.InstanceType(instance_type),
                                    machine_image=ami,
                                    vpc=vpc,
                                    role=role,
                                    security_group=sg)

        # SSM Parameter
        ssm.StringParameter(self, "InstanceInfoParameter",
                            parameter_name=config["ssm_parameter_name"],
                            string_value=ec2_instance.instance_id)

        # Alternatively, tag all resources in this stack
        Tags.of(self).add("project", "ec2_ssm_instance_setup")



if __name__ == "__main__":
    import os
    import aws_cdk as cdk
    
    # Configuration dictionary
    config = {
        "instance_type": "t2.micro",
        "ami_type": ec2.MachineImage.latest_amazon_linux2(),
        "vpc_id": None,  # Specify VPC ID if not creating a new one
        "role_policies": [
            "AmazonSSMManagedInstanceCore",
            "EC2InstanceProfileForImageBuilderECRContainerBuilds"
        ],
        "sg_description": "Allow SSM access",
        "ssm_parameter_name": "/ec2/instance/info"
    }

    # CDK application setup
    app = App()
    EC2SSMSessionManagerStack(app, "EC2SSMSessionManagerStack", config=config,
                              env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
    app.synth()



