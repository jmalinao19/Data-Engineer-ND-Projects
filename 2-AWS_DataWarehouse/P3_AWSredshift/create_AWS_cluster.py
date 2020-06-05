import configparser
import boto3

def parse_configFile():
    """
    Parses the dwh.config file and returns tuple of its contents

    @returns -- config contents. Tuple order follows the config.get executions order in this function  
    """
    config = configparser.ConfigParser()
    with open('dwh.cfg') as config_file:
        config.read_file(config_file)

        KEY = config.get('AWS','KEY') # Tuple order :0
        SECRET = config.get('AWS','SECRET') # : 1

        DB_NAME = config.get('CLUSTER','DB_NAME') # : 2
        DB_USER = config.get('CLUSTER','DB_USER') # : 3
        DB_PASSWORD = config.get('CLUSTER','DB_PASSWORD') # : 4
        DB_PORT = config.get('CLUSTER','DB_PORT') # : 5

        DWH_CLUSTER_TYPE = config.get('DWH','DWH_CLUSTER_TYPE') # : 6
        DWH_NUM_NODES = config.get('DWH','DWH_NUM_NODES') # : 7 
        DWH_NODE_TYPE = config.get('DWH','DWH_NODE_TYPE') # : 8

        DWH_IAM_ROLE_NAME = config.get('DWH','DWH_IAM_ROLE_NAME') # : 9
        DWH_CLUSTER_IDENTIFIER = config.get('DWH','DWH_CLUSTER_IDENTIFIER') # :10
    return KEY, SECRET, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, DWH_CLUSTER_TYPE, DWH_NUM_NODES, DWH_NODE_TYPE, DWH_IAM_ROLE_NAME, DWH_CLUSTER_IDENTIFIER



def build_iamRole(iam, DWH_IAM_ROLE_NAME):
    """
    Creates AWS IAM role and attaches AmazonS3ReadOnlyAccess Role policy
    @type iam -- object
    @param iam -- IAM client

    @type DWH_IAM_ROLE_NAME -- string
    @param DWH_IAM_ROLE_NAME -- value from config file

    @return dwhProjectRole with attached S3 read only policy access
    """
    try:
        print('Creating a new IAM role to enable read only access to S3 bucket from Redshift \n')
        dwhRole = iam.create_role(
            Path = '/',
            RoleName = DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift cluster to call AWS services",
            AssumeRolePolicyDocument = json.dumps(
            {'Statement' : [{'Action': 'sts:AssumeRole', 
            'Effect': 'Allow',
            'Principal': {'Service': 'redshift.amazonaws.com'}}],
            'Version': '2012-10-17'}))
        print('heheheheheheh')
    except Exception as e:
        print(e)
        dwhRole = iam.get_role(RoleName = DWH_IAM_ROLE_NAME)

    print('Attaching AmazonS3ReadOnlyAccess to IAM role.\n')
    return iam.attach_role_policy(RoleName = DWH_IAM_ROLE_NAME,
                                PolicyArn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")['ResponseMetadata']['HTTPStatusCode']
    

def get_role(iam, DWH_IAM_ROLE_NAME):
    """
    Retrieves the IAM role string
    @type iam  -- object
    @param iam -- IAM resource client

    @type DWH_IAM_ROLE_NAME -- string
    @param DWH_IAM_ROLE_NAME -- value from config file
    
    @return IAM role Arn
    """
    print('Getting the IAM role Arn\n')
    return iam.get_role(RoleName = DWH_IAM_ROLE_NAME)['Role']['Arn']

   


def begin_cluster_build(redshift, roleArn, DWH_CLUSTER_TYPE, DWH_NODE_TYPE, DWH_NUM_NODES, DB_NAME, DWH_CLUSTER_IDENTIFIER, DB_USER, DB_PASSWORD):
    """
    Begins creating the AWS redshift cluster 
    @type  redshift -- object
    @param redshift -- AWS Redshift resource client

    @type roleArn -- object
    @param roleArn -- created role ARN
    
    @return -- HTTP response if pass, False if fail
    """
    try:
        response = redshift.create_cluster(
            # Cluster
            ClusterType= DWH_CLUSTER_TYPE,
            NodeType = DWH_NODE_TYPE,
            NumberOfNodes = int(DWH_NUM_NODES),
            
            # Credentials
            DBName = DB_NAME,
            ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,
            MasterUsername = DB_USER,
            MasterUserPassword = DB_PASSWORD,
            
            # Role for accessing S3
            IamRoles = [roleArn]
        )
        print('Cluster is being created \n')
        print('Redshift cluster build http response status: \n')
        print(response['ResponseMetaData']['HTTPStatusCode'])
        return response['ResponseMetaData']['HTTPStatusCode']  == 200

    except Exception as e:
        print('Cluster was not created \n')
        print(e)
    return False


def aws_client(service,region,KEY,SECRET):
    """
    Creates AWS client
    @type service -- string
    @param service -- The AWS service to create

    @type region -- string
    @param region -- The region of the service

    @type KEY-- string
    @param KEY-- value from config file
    @type SECRET -- string
    @param SECRET-- value from config file

    @return -- client object for the requested service 
    """
    return boto3.client(service, region_name = region, aws_access_key_id = KEY, aws_secret_access_key= SECRET)


def aws_resource(name,region,KEY,SECRET):
    """
    Creates AWS client resource
    @type name -- string
    @param name -- Name of AWS resource 

    @type region -- string
    @param region -- Region of AWS resource
    """
    return boto3.resource(name, region_name = region, aws_access_key_id = KEY, aws_secret_access_key= SECRET) 

"""
def create_AWS_client(name,service,region):
    global KEY, SECRET
    
    client = boto3.client(service,region_name = region, aws_access_key_id = KEY, aws_secret_access_key= SECRET)
    resource = boto3.resource(name,region_name = region, aws_access_key_id = KEY, aws_secret_access_key= SECRET)
    return client, resource
"""

def main():
    configs =parse_configFile()
    iam = aws_client('iam','us-east-2',configs[0],configs[1])
    redshift = aws_client('redshift','us-east-2',configs[0],configs[1])
    build_iamRole(iam,configs[9])
    roleArn = get_role(iam,configs[9])
    begin_cluster_build(redshift,roleArn,configs[6],configs[8],configs[7],configs[2],configs[10],configs[3],configs[4])

if __name__ =='__main__':
    main()

