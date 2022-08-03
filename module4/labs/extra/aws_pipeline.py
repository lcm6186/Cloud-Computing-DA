import boto3
import os

class KinesisStream(object):

    CLIENT = boto3.client('kinesis')
    SHARD_COUNT = 2

    def __init__(self, stream_name):
        self.stream_name = stream_name

    def list(self):
        return self.CLIENT.list_streams()['StreamNames']

    def create(self):
        self.CLIENT.create_stream(
            StreamName=self.stream_name,
            ShardCount=self.SHARD_COUNT
            )

    def add_tags(self):
        self.CLIENT.add_tags_to_stream(
            StreamName=self.stream_name,
            Tags=self.build_tags()
            )

    def build_tags(self):
        return {
            'BUSINESS_REGION': 'NORTHAMERICA',
            'BUSINESS_UNIT': 'DATASERVICES',
            'CLIENT': 'NONE',
            'ENVIRONMENT': 'POC',
            'NAME': self.stream_name,
            'PLATFORM': 'ATLAS'
        }

    def get_arn(self):
        return self.CLIENT.describe_stream(
            StreamName=self.stream_name
            )['StreamDescription']['StreamARN']

class KinesisFirehose(object):
    CLIENT = boto3.client('firehose')
    iam = boto3.client('iam')

    def __init__(self, firehose_name, bucket_name, prefix_name):
        self.firehose_name = firehose_name
        self.bucket_name = bucket_name
        self.prefix_name = prefix_name

    def list(self):
        return self.CLIENT.list_delivery_streams()['DeliveryStreamNames']

    def create(self):
        print("********************")
        print(self.config)
        return self.CLIENT.create_delivery_stream(
            DeliveryStreamName=self.firehose_name,
            S3DestinationConfiguration=self.config()
            )
    
    def create_role(name,policies=None):
        """ Create a role with an optional inline policy """
        policydoc = {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Principal": {"Service": ["lambda.amazonaws.com"]}, "Action": ["sts:AssumeRole"]},
            ]
        }
        roles = [r['RoleName'] for r in iam.list_roles()['Roles']]
        if name in roles:
            print('IAM role %s exists' % (name))
            role = iam.get_role(RoleName=name)['Role']
        else:
            print('Creating IAM role %s' % (name))
            role = iam.create_role(RoleName=name, AssumeRolePolicyDocument=json.dumps(policydoc))['Role']

        # attach managed policy
        if policies is not None:
            for p in policies:
                iam.attach_role_policy(RoleName=role['RoleName'], PolicyArn=p)
        return role
    
    
    def config(self):
        role=self.create_role('lambda', policies=['arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole'])
        return {
            'RoleARN': role,
            'BucketARN': 'arn:aws:s3:::' + self.bucket_name,
            'Prefix': self.prefix_name,
            'BufferingHints': {
                'SizeInMBs': 128,
                'IntervalInSeconds': 900
            },
            'CompressionFormat': 'Snappy',
            'EncryptionConfiguration': {
                'NoEncryptionConfig': 'NoEncryption'
            },
            'CloudWatchLoggingOptions': {
                'Enabled': True,
                'LogGroupName': '/aws/kinesisfirehose/' + self.firehose_name,
                'LogStreamName': 'S3Delivery'
            }
        }


class S3(object):
    RESOURCE = boto3.resource('s3')
    CONFIG_FILE_BUCKET = 'dsabucket1'
    CONFIG_FILE_PREFIX = 'lambda-configs/'

    def __init__(self, config_file):
        self.file = config_file

    def upload_file_to_config_folder(self):
        print(self.file)
        self.RESOURCE.meta.client.upload_file(
            os.path.realpath(self.file),
            self.CONFIG_FILE_BUCKET, 
            self.CONFIG_FILE_PREFIX + self.file
            )

class Lambda(object):

    CLIENT = boto3.client('lambda')

    def __init__(self, stream_arn, function_name):
        self.stream_arn = stream_arn
        self.function_name = function_name

    def event_source_list(self):
        return self.CLIENT.list_event_source_mappings(
            EventSourceArn=self.stream_arn, 
            FunctionName=self.function_name
            )['EventSourceMappings']

    def create_event_source(self):
        self.CLIENT.create_event_source_mapping(
            EventSourceArn=self.stream_arn,
            FunctionName=self.function_name,
            Enabled=True,
            BatchSize=100,
            StartingPosition='LATEST'
            )