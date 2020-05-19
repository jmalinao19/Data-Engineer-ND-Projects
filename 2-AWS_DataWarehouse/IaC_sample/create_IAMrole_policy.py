
import boto3


dwhRole = iam.create_role (
        Path = '/',
        RoleName = DWH_IAM_ROLE_NAME,
        Description = 'Allows Redshift Clusters to call AWS services on your behalf.',
        AssumeRolePolicyDocument =json.dumps(
            {'Statement' : [{'Action': 'sts:AssumeRole', 
            'Effect': 'Allow',
            'Principal': {'Service': 'redshift.amazon.com'}}],
            'Version': '2012-10-17'}))

iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME, 
                        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                        )['ResponseMetadata']['HTTPStatusCode']
