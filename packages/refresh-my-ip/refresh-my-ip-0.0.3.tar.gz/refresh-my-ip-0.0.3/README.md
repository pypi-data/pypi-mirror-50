# refresh-my-ip

## Quick Overview
If you have EC2 instances locked down by IP address, it can be time annoying/frustrating/time-consuming if your IP address changes, or if you work in different locations.

Using the `Description` field, `refresh-my-ip` will scan through all of your security groups looking for `MyIp` and replace the IP address with your current public IP address.

## Quick Start
1. Install the app:

    `pip install refresh-my-ip`

2. In any of your security group ingress rules where you want to automatically refresh the IP address, simply change the description to `MyIp`.

3. Run `refresh-my-ip` anytime you want to update all the IP addresses.

## Optional Feature
If you don't want to use `MyIp` in the description, you can pass `--match-description` along with the text you want to match.

## IAM Policy
These are the minimum permissions to run `refresh-my-ip`.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```