import copy
import json
import boto3
import datetime
import os
import traceback
from urllib.parse import unquote
from botocore.config import Config
# config = Config(retries={'max_attempts': 10, 'mode': 'standard'})
# env_map = {
#     'dev': 'development',
#     'qa': 'quality_assurance',
#     'qa-pr': 'quality_assurance',
#     'prod': 'production'
# }
# ddb_client = boto3.client(
#     'dynamodb', region_name='us-west-2', config=config)
# sns_client = boto3.client('sns', region_name='us-west-2', config=config)


# def read_s3_json_file(bucket, key):
#     s3 = boto3.resource('s3', region_name='us-west-2', config=config)
#     content_object = s3.Object(bucket, key)
#     file_content = content_object.get()['Body'].read().decode('utf-8')
#     json_content = json.loads(file_content)
#     return json_content


# def get_data_from_sns(event):
#     event_obj_invoke_job = {
#         's3_mls_file': None,
#     }
#     feed_type = None
#     feed_stage = None

#     todays_date = datetime.date.today()
#     date_path = 'year=' + str(todays_date.year) + '/month=' + \
#                 str(todays_date.month).zfill(2) + \
#                 '/day=' + str(todays_date.day).zfill(2)

#     if event.get('Records')[0].get('EventSource') == "aws:sns":
#         record = event.get('Records')[0].get('Sns')
#         sns_msg = json.loads(record.get('Message'))
#         bucket = sns_msg['Records'][0]['s3']['bucket']['name']
#         key = sns_msg['Records'][0]['s3']['object']['key']
#         decoded_key = unquote("/".join(key.split("/")))
#         s3_folder_key = unquote("/".join(key.split("/")[:-1]))
#         manifest_json = read_s3_json_file(bucket, decoded_key)
#         for file in manifest_json.get('files', None):
#             file_name = file.get('name', None)
#             if ("Inc_Extract" in file_name and ".zip" in file_name):
#                 feed_type = "incremental"
#                 feed_stage = "transform"
#                 event_obj_invoke_job['s3_mls_file'] = 's3://' + \
#                     bucket + '/' + s3_folder_key + "/" + file_name

#     return {
#         "event_obj_invoke_job": event_obj_invoke_job,
#         "feed_type": feed_type,
#         "feed_stage": feed_stage,
#         "date_path": date_path
#     }


# def create_sfn_input(event, gtid):
#     env = env_map[os.getenv('ENV')]
#     event_details = {
#         'event': json.dumps(event),
#         'event_ts': event.get('Records')[0].get('Sns').get('Timestamp')
#     }
#     event_data = get_data_from_sns(event)
#     log_object = {'message': 'Files From SNS Event', 'global_tracking_id':
#                                 gtid, 'files': event_data['event_obj_invoke_job']}
#     print(json.dumps(log_object))

#     return {
#         'env': env,
#         'event_details': event_details,
#         'global_tracking_id': gtid,
#         'files': event_data['event_obj_invoke_job'],
#         'feed_type': event_data['feed_type'],
#         'feed_stage': event_data['feed_stage'],
#         'date_path': event_data['date_path']
#     }


# def create_sfn_input_history(event, gtid):
#     env = env_map[os.getenv('ENV')]
#     event_details = {
#         'event': json.dumps(event),
#         'event_ts': event.get('Records')[0].get('Sns').get('Timestamp')
#     }
#     event_data = get_data_from_sns_history(event)
#     log_object = {'message': 'Files From SNS Event', 'global_tracking_id':
#                                 gtid, 'files': event_data['event_obj_invoke_job']}
#     print(json.dumps(log_object))

#     return {
#         'env': env,
#         'event_details': event_details,
#         'global_tracking_id': gtid,
#         'files': event_data['event_obj_invoke_job'],
#         'feed_type': event_data['feed_type'],
#         'feed_stage': event_data['feed_stage'],
#         'date_path': event_data['date_path']
#     }

# def get_data_from_sns_history(event):
#     event_obj_invoke_job = {
#         's3_mls_file': None,
#     }
#     feed_type = 'mls_history'
#     feed_stage = 'write_history_to_s3'

#     todays_date = datetime.date.today()
#     date_path = 'year=' + str(todays_date.year) + '/month=' + \
#                 str(todays_date.month).zfill(2) + \
#                 '/day=' + str(todays_date.day).zfill(2)

#     if event.get('Records')[0].get('EventSource') == "manual trigger":
#         record = event.get('Records')[0].get('Sns')
#         sns_msg = json.loads(record.get('Message'))
#         bucket = sns_msg['Records'][0]['s3']['bucket']['name']
#         key = sns_msg['Records'][0]['s3']['object']['key']
#         event_obj_invoke_job['s3_mls_file'] = 's3://' + \
#             bucket + '/' + key + '/'

#     return {
#         "event_obj_invoke_job": event_obj_invoke_job,
#         "feed_type": feed_type,
#         "feed_stage": feed_stage,
#         "date_path": date_path
#     }

def handler(event, context):
    print("test lambda invoked")
    # log_object = {'message': 'Event received', 'Event': event}
    # print(json.dumps(log_object))

    # gtid = 'sdp_mls.'+context.aws_request_id

    # try:
    #     # process only mls feed
    #     if isMlsEvent(event):
    #         sfn = os.getenv('SFN')
    #         client = boto3.client(
    #                 'stepfunctions', region_name='us-west-2', config=config)
    #         response = client.start_execution(stateMachineArn=sfn,
    #                                                     input=json.dumps(
    #                                                         create_sfn_input(event, gtid)))
    #         formatted_response = json.dumps(
    #             response, default=datetime_handler)

    #         return {'ReturnValue': formatted_response}
    #     elif isHistoryFlow(event):
    #         sfn = os.getenv('SFN')
    #         client = boto3.client(
    #                 'stepfunctions', region_name='us-west-2', config=config)
    #         response = client.start_execution(stateMachineArn=sfn,
    #                                             input=json.dumps(
    #                                                 create_sfn_input_history(event, gtid)))
    #         formatted_response = json.dumps(
    #                 response, default=datetime_handler)

    #         return {'ReturnValue': formatted_response}

    #     else:
    #         print('Event is not for manifest.json file of mls, returning without processing')
    #         return
        
    # except Exception as e:
    #     print('Error Message : ', e)
    #     log_object = {'error': traceback.format_exc()}
    #     print('Error from lambda handler', log_object)
    #     return



# def isHistoryFlow(event):
#     if event.get('Records')[0].get('EventSource') == "manual trigger":
#         return True
#     else:
#         False


# def isMlsEvent(event):
#     if event.get('Records')[0].get('EventSource') == "aws:sns":
#         record = event.get('Records')[0].get('Sns')
#         sns_msg = json.loads(record.get('Message'))
#         key = sns_msg['Records'][0]['s3']['object']['key']
#         if 'MLS' in key and 'manifest.json' in key:
#             return True
#         return False


# def datetime_handler(data):
#     if isinstance(data, datetime.datetime):
#         return data.isoformat()
#     raise TypeError("Unknown type")
