# Open an incoming TPC port to access the cluster
import boto3

vpc = ec2.Vpc(id =myClusterProps['VpcID'])
defaultSg = list(vpc.security_groups.all())[0]
defaultSg.authorize_ingress(
    Group_name = defaultSg.Group_name,
    CidrIp = '0.0.0.0/0',
    IpProtocol = 'TCP',
    FromPort = int(DWH_PORT),
    ToPort = int(DWH_PORT)
)
