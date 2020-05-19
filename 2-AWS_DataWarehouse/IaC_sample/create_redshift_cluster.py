
import boto3

redshift = boto3.client ('redshift',
                        region_name = 'us-west-2',
                        aws_access_key_id = KEY,
                        aws_secret_key_id = SECRET,
)

response = redshift.create_cluster(
    #HardWare
    ClusterType = DWH_CLUSTER_TYPE,
    NodeType = DWH_NODE_TYPE,
    NumberOfNodes = int(DWH_NUM_NODES)

    #Identifiers and Credentials
    DBNAME = DWH_DB,
    ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,
    MasterUsername = DWH_DB_USER,
    MasterUserPassword = DWH_DB_PASSWORD,

    # Roles (for s3 access)
    IamRoles = [roleArn]
)