import pulumi
import pulumi_aws as aws

# Define a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "my-vpc"},
)

# Define a subnet
subnet = aws.ec2.Subnet("my-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-west-2a",
    tags={"Name": "my-subnet"},
)

# Define a security group
security_group = aws.ec2.SecurityGroup("my-security-group",
    vpc_id=vpc.id,
    egress=[
        {
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    tags={"Name": "my-security-group"},
)

# Define an EC2 instance
instance = aws.ec2.Instance("my-instance",
    instance_type="t2.micro",
    ami="ami-0182f373e66f89c85",  
    vpc_security_group_ids=[security_group.id],
    subnet_id=subnet.id,
    tags={"Name": "my-instance"},
)

pulumi.export("instance_id", instance.id)

