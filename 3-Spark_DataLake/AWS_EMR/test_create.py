aws emr create-cluster --name <YOUR_CLUSTER_NAME> 
--use-default-roles  
--release-label emr-5.28.0
--instance-count 2 
--applications Name=Spark  
#--bootstrap-actions Path=<YOUR_BOOTSTRAP_FILENAME> 
--ec2-attributes KeyName=<YOUR_KEY_NAME> 
--instance-type m5.xlarge 
--instance-count 3 
--auto-terminate`

# Specify your cluster name 
`YOUR_CLUSTER_NAME: test-create-cluster

# Insert your IAM KEYNAME - 
# Remember, your IAM key name is saved under .ssh/ directory
YOUR_KEY_NAME: spark-cluster

# Specify your bootstrap file. Please note that this step is optional. 
# It should be an executable (.sh file) in an accessible S3 location. 
# If you aren't going to use the bootstrap file, 
# you can remove the `--bootstrap-actions` tag above.
# This file is provided in the zipped folder titled
# “Exercise_Creating EMR Cluster” at the bottom of this page.

# In this EMR script, execute using Bootstrap
#YOUR_BOOTSTRAP_FILENAME: bootstrap_emr.sh 
```