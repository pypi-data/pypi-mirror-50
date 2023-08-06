import boto3
import time

# logs.create_log_group(logGroupName=LOG_GROUP)
# logs.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
class log(object):

    def __init__(self, region_name=None, aws_access_key_id=None,aws_secret_access_key=None, endpoint_url=None):
        if region_name == None and aws_access_key_id == None and aws_secret_access_key == None and endpoint_url == None:
            self.logger = boto3.client('logs')
        else:
            self.logger = boto3.client('logs',
                                region_name=region_name,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                endpoint_url='https://logs.ap-southeast-1.amazonaws.com')

    def create_log_group(self, LOG_GROUP):
        try:
            resp = self.logger .create_log_group(logGroupName=LOG_GROUP)
        except self.logger.exceptions.ResourceAlreadyExistsException as err:
            status = err.response["ResponseMetadata"]["HTTPStatusCode"]
            errcode = err.response["Error"]["Code"]
            if status == 404:
                resp = "Missing object, %s", errcode
            elif status == 403:
                resp = "Access denied, %s", errcode
            else:
                resp = "Error in request, %s", errcode
        print(resp)

    def create_log_stream(self, LOG_GROUP, LOG_STREAM):
        try:
            resp = self.logger.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
        except self.logger.exceptions.ResourceAlreadyExistsException as err:
            status = err.response["ResponseMetadata"]["HTTPStatusCode"]
            errcode = err.response["Error"]["Code"]
            if status == 404:
                resp = "Missing object, %s", errcode
            elif status == 403:
                resp = "Access denied, %s", errcode
            else:
                resp = "Error in request, %s", errcode
        return resp

    def log_message(self, LOG_GROUP, LOG_STREAM, message):
        timestamp = int(round(time.time() * 1000))
        response = self.logger.describe_log_streams(logGroupName=LOG_GROUP)
        # response['logStreams'][0]['uploadSequenceToken']
        response = self.logger.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ],
            sequenceToken=response['logStreams'][0]['uploadSequenceToken']
        )
        return response

