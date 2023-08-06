import boto3
import pprint
import click
from botocore.exceptions import ClientError
import urllib.request

@click.command()
@click.option("--match-description", default='MyIp', help="Ingress rule description to match against")
def main(match_description):
    my_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    ec2 = boto3.client('ec2')

    try:
        pp = pprint.PrettyPrinter()
        response = ec2.describe_security_groups()
        if response['SecurityGroups']:
            for sg in response['SecurityGroups']:
                if sg['IpPermissions']:
                    for p in sg['IpPermissions']:
                        if p['IpRanges']:
                            for i in p['IpRanges']:
                                if 'Description' in i.keys() and i['Description'] == match_description:
                                    print('Updating permissions in group {}'.format(sg['GroupName']))
                                    ec2.revoke_security_group_ingress(IpProtocol=p['IpProtocol'],
                                                                      GroupId=sg['GroupId'],
                                                                      CidrIp=i['CidrIp'],
                                                                      FromPort=p['FromPort'],
                                                                      ToPort=p['ToPort'])
                                    ec2.authorize_security_group_ingress(GroupId=sg['GroupId'],
                                                                         IpPermissions=[{
                                                                             'FromPort': p['FromPort'],
                                                                             'IpProtocol': p['IpProtocol'],
                                                                             'IpRanges': [
                                                                                 {
                                                                                     'CidrIp': my_ip + "/32",
                                                                                     'Description': i['Description']
                                                                                     }],
                                                                             'ToPort': p['ToPort']
                                                                             }
                                                                         ])
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    main()
