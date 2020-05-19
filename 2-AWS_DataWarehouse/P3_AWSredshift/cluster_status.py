from create_AWS_cluster import aws_client, aws_resource, parse_configFile
import configparser
import pandas as pd
import boto3
import json
import time


def persist_cluster_configInfo(Redshift, DWH_CLUSTER_IDENTIFIER):
    """
    Writes the cluster endpoint and IAM ARN to the dwh.cfg config file 
    @type redshift -- client
    @param redshift -- Redshift resource client

    @type DWH_CLUSTER_IDENTIFIER -- string
    @param DWH_CLUSTER_IDENTIFIER -- value from config file
    
    @return -- None
    """
    print('Cluster address and IamRoleARN is being written to the config file.')
    cluster_properties = Redshift.describe_clusters(ClusterIdentifier = DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    config = configparser.ConfigParser()

    config.read_file(open('dwh.cfg'))

    config.set('CLUSTER','HOST',cluster_properties['Endpoint']['Address'])
    config.set('IAM_ROLE','ARN',cluster_properties['IamRoles'][0]['IamRoleArn'])

    with open('dwh.cfg','w+') as configFile:
        config.write(configFile)
    parse_configFile()



def get_cluster_status(redshift,DWH_CLUSTER_IDENTIFIER):
    """
    Checks the Redshift cluster status, retuns True or False
    @type redshift -- redshift 
    @param redshift -- AWS Redshift resource client

    @type DWH_CLUSTER_IDENTIFIER -- string
    @param DWH_CLUSTER_IDENTIFIER -- value from config file

    @return -- boolean True or False
    """
    cluster_properties = redshift.describe_clusters(ClusterIdentifier = DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    clusters_status = cluster_properties['ClusterStatus']
    return clusters_status.lower()

def describe_clust(redshift,DWH_CLUSTER_IDENTIFIER):
    return redshift.describe_clusters(ClusterIdentifier = DWH_CLUSTER_IDENTIFIER)['Clusters'][0]

def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

def open_redshift_port (ec2,redshift, DWH_CLUSTER_IDENTIFIER, DB_PORT):
    """
    Redshift post on VPC security group is opened
    @type ec2 -- clinet
    @param ec2 -- AWS EC2 resource client

    @type redshift -- client
    @param redshift -- Redshift resource client

    @return -- none
    """
    myClusterProps = redshift.describe_clusters(ClusterIdentifier = DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        secur_group = list(vpc.security_groups.all())
        print(secur_group)
        defaultSg = secur_group[1]
        
        defaultSg.authorize_ingress(
            GroupName= defaultSg.group_name,
            CidrIp='0.0.0.0/0',  
            IpProtocol='TCP',  
            FromPort=int(DB_PORT),
            ToPort=int(DB_PORT)
        )
    except Exception as e:
        print(e)


def main():
    """
    Checks the Redshift cluster status and opens the Port
    """
    # parse config file
    configs=parse_configFile()

    #get redshift client
    redshift = aws_client('redshift','us-east-2',configs[0],configs[1])

    # check if cluster was created
        # add port thing, and create ec2 resource object to do so
    if get_cluster_status(redshift,configs[10]):
        print('Cluster is available:')
        print(prettyRedshiftProps(describe_clust(redshift,configs[10])))
        ec2 = aws_resource('ec2','us-east-2',configs[0],configs[1])
        persist_cluster_configInfo(redshift,configs[10])
        open_redshift_port(ec2,redshift,configs[10],configs[5])
        print('Cluster is up and running')
    else:
        print('Cluster is not available yet')

if __name__ =='__main__':
    main()