from create_AWS_cluster import parse_configFile, 
from cluster_status import get_cluster_status

def delete_cluster(redshift, DWH_CLUSTER_IDENTIFIER):
    """
    Request a deletion for Redshift cluster
    @type redshift --
    @param redshift -- Redshift resource client

    @type DWH_CLUSTER_IDENTIFIER -- string
    @param DWH_CLUSTER_IDENTIFIER -- value from config file

    @return -- None
    """
    return redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, SkipFinalClusterSnapshot = True)

def main():
    configs = parse_configFile()
    redshift = aws_client('redshift','us-east-2')

    if get_cluster_status(redshift,configs[10]) == 'available':
        print('Cluster is available and will begin the deletion process')
        delete_cluster(redshift,configs[10])
        print(get_cluster_status(redshift,configs[10]))
    else:
        print('Cannot Delete because Cluster is not available ')

if __name__ == '__main__':
    main()
