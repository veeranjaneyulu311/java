import unittest
from unittest.mock import patch, Mock, mock_open
import os
import json
from io import StringIO
from requests.models import Response
import requests

os.environ = {'LOG_LEVEL': 'DEBUG',
              'conversations_url': 'https://contactconversations-qal.api.intuit.com/v1/conversations/',
              'region': 'us-east-1',
              'tablename': 'intuit-expert-contact-history-dev-us-east-1', 'auth_key': 'testauth',
              'user_id': 'test_user', 'source_bucket': 'bucket'}

import ctr_record_reader
from botocore.exceptions import ClientError


class TestCtrRecordReader(unittest.TestCase):

    @classmethod
    def setUp(self):
        print(self)
        self.s3_success_event = {"Records": [{"eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "us-east-1",
                                              "eventTime": "2019-08-13T21:35:04.067Z",
                                              "eventName": "ObjectCreated:Copy", "userIdentity": {
                "principalId": "AWS:AROAJYWPN6RJBSK3YQY5A:IntuitOlympus-mstraathof-50002143090-1565725936755"},
                                              "requestParameters": {"sourceIPAddress": "65.204.229.83"},
                                              "responseElements": {"x-amz-request-id": "D79E8ABFD216178E",
                                                                   "x-amz-id-2": "LkwXh6cdwwXYM1l19t9MC6tUhEJVUgk1RrtDSbq1N0e4X1MglrcW2L6Qa3H3DeQeyk2y7T91jEU="},
                                              "s3": {"s3SchemaVersion": "1.0",
                                                     "configurationId": "45fca787-c271-4cc3-b172-11498f716db1",
                                                     "bucket": {
                                                         "name": "intuit-firehoses3failures-default-dev-us-east-1",
                                                         "ownerIdentity": {"principalId": "A1XM9MBLPWFH1C"},
                                                         "arn": "arn:aws:s3:::intuit-firehoses3failures-default-dev-us-east-1"},
                                                     "object": {
                                                         "key": "connectCtrAmericas2019/08/13/17/intuit-connectCtrAmericasFirehoseS3-default-prd-us-east-1-4-2019-08-13-19-12-49-19f4c4b8-01a6-4dfc-95d5-d6ecb00ea741",
                                                         "size": 254506, "eTag": "8b7eb3faae5f9f1d426ee64de6edd401",
                                                         "sequencer": "005D532D07F5FE703E"}}}]}
        self.conversations_response_success = {"channelType": "VOICE", "modality": "INBOUND",
                                               "temporality": "UNSCHEDULED",
                                               "participant": {"fName": "defaultName", "lName": "defaultName",
                                                               "telephone": "+16174291336",
                                                               "email": "default@intuit.com"},
                                               "queueName": "sbseg-dt_proprem_en_us_supphv_phn", "priority": "Medium",
                                               "caseID": "5003j00001cwGbUAAU", "caseNum": "537740803",
                                               "generatedConversationId": "NA", "conversationState": "DISCONNECTED_CCP",
                                               "nextGenWorkgroup": "true", "dnis": "+18772234713",
                                               "contactId": "e91b68eb-00e9-4948-840b-8fd3aea44dc1",
                                               "wsPhoneNumber": "+16174291336", "searchData": "transfer",
                                               "productPlatform": "DESKTOP",
                                               "inetCallId": "be430763d1a6b01dc3f0b36f8763806a",
                                               "intent": "USER_MANAGEMENT", "subject": "subject", "chatDetails": {}}
        self.valid_json_data = {"AWSAccountId": "348016918056", "AWSContactTraceRecordFormatVersion": "2017-03-10",
                                "Agent": {
                                    "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/agent/d6b46bfb-40d9-4ab4-bdc7-0105049fce90",
                                    "AfterContactWorkDuration": 116,
                                    "AfterContactWorkEndTimestamp": "2019-08-13T19:11:57Z",
                                    "AfterContactWorkStartTimestamp": "2019-08-13T19:10:01Z",
                                    "AgentInteractionDuration": 2257,
                                    "ConnectedToAgentTimestamp": "2019-08-13T18:15:23Z", "CustomerHoldDuration": 1021,
                                    "HierarchyGroups": {"Level1": {
                                        "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/agent-group/178f4beb-5a1a-4108-91a2-ec62d80568eb",
                                        "GroupName": "SBSEG"}, "Level2": {
                                        "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/agent-group/1a0fcc4b-88fc-479a-9f77-f523b2bfd05f",
                                        "GroupName": "Convergys"}, "Level3": {
                                        "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/agent-group/9cd0272b-5900-46fc-b090-3fc085f317fb",
                                        "GroupName": "Cebu"}, "Level4": {
                                        "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/agent-group/729fb994-0fe9-4108-b918-7cd3d0276e78",
                                        "GroupName": "Global Online CAN Tier 1"}, "Level5": None},
                                    "LongestHoldDuration": 1021, "NumberOfHolds": 1, "RoutingProfile": {
                                        "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/routing-profile/fce86b6d-7599-4ed6-9a69-19822c201b02",
                                        "Name": "sbseg-ol_qbo_en_can_payrollagent"}, "Username": "stceb5953"},
                                "AgentConnectionAttempts": 1,
                                "Attributes": {"intuAccountName": "", "intuAcwQueueDuration": "",
                                               "intuAcwQueueOverrideEnabled": "", "intuAgentHoldLoopDuration": "60",
                                               "intuAgentId": "stceb5953", "intuAgentType": "",
                                               "intuAgentWhisperCallbackMessage": "Callback request. Customer will join shortly after being connected",
                                               "intuAgentWhisperMessage": "Q B O A Platinum",
                                               "intuAgentWhisperOverride": "", "intuAgentWhisperOverrideMessage": "",
                                               "intuAgentsAvailableCount": "0", "intuAgentsStaffedCount": "22",
                                               "intuAwsVoice": "Joanna", "intuCallQualityStatsEnabled": "true",
                                               "intuCallRecordingEnabled": "true",
                                               "intuCallType": "SBSEG_CAN_QBOA_EN_HOO", "intuCallTypeForcedMessage": "",
                                               "intuCallbackConfigurationId": "SBSEG_AutoCallback_Config",
                                               "intuCallbackNumber": "+14167884774", "intuCompanyId": "193514500293409",
                                               "intuConnectFlow": "sbseg-can_qbo_en_main_menu",
                                               "intuContactFlow": "plt-uq_dynamic_queue_loop",
                                               "intuContactId": "11460ea0-b994-49a1-bfe4-f2e34bf2f237",
                                               "intuContactType": "Transfer", "intuCustomerAccountId": "",
                                               "intuCustomerAccountNumber": "None", "intuCustomerInput": "4169896527",
                                               "intuCustomerValue": "false", "intuCustomerWhisperInboundMessage": "-",
                                               "intuDataDipResult": "sfdcPhLkupForCompanyIdandTier:SingleRecordFound",
                                               "intuDefaultQueryEnabled": "true",
                                               "intuDefaultQueryName": "sfdcPhLkupForCompanyIdandTier",
                                               "intuDefaultQueryType": "SF_B2B", "intuDefaultQueue": "",
                                               "intuDialedNumber": "+19999999999", "intuDialedNumberType": "",
                                               "intuDisplayQualityStats": "false", "intuEmergencyMessage": "",
                                               "intuEntryPoint": "", "intuEwtEnabled": "true", "intuEwtMethod": "Range",
                                               "intuEwtTtsEnabled": "true", "intuFeatureCustomAcd": "",
                                               "intuFeatureLiveCallStreaming": "", "intuFeatureOneStepTransfer": "",
                                               "intuFlowArn": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/contact-flow/de11c87b-f894-44b7-abc7-d55031ebc9ad",
                                               "intuForcedMessage": "-", "intuFraudDetectionEnabled": "",
                                               "intuFraudDetectionMessage": "", "intuHVAssistedPayroll": "",
                                               "intuHmsCallbackConfirm": "", "intuHmsCallbackConfirmTts": "",
                                               "intuHmsEnabled": "false", "intuHmsEnteredPhoneMessage": "",
                                               "intuHmsEnteredPhoneMessageTts": "", "intuHmsFailout": "",
                                               "intuHmsFailoutTts": "", "intuHmsGoodbye": "", "intuHmsGoodbyeTts": "",
                                               "intuHmsMaxThreshold": "15", "intuHmsPhoneConfirmMenu": "",
                                               "intuHmsPhoneConfirmMenuTts": "", "intuHmsPhoneInputPrompt": "",
                                               "intuHmsPhoneInputPromptTts": "", "intuHmsPhoneMakeGoodPrompt": "",
                                               "intuHmsPhoneMakeGoodPromptTts": "", "intuHmsScheduleStatus": "Open",
                                               "intuHmsSecondaryThreshold": "0", "intuHmsThreshold": "0",
                                               "intuHmsTtsEnabled": "true", "intuHmsType": "Optional",
                                               "intuHolidayMessage": "Thank you for calling Intuit. Our offices are closed today in observance of the holiday. Please try your call again during our normal business hours. Again, thank you for calling Intuit.",
                                               "intuHooLambdaArn": "arn:aws:lambda:us-east-1:348016918056:function:intuit-getHoursOfOperation-default-prd-us-east-1",
                                               "intuIfOnlineQueueCall": "", "intuIfStaffedQueueCall": "",
                                               "intuInputRetry": "0", "intuIntegraID": "", "intuLabel": "-",
                                               "intuLambda": "UniversalQueue:Found",
                                               "intuLastContactFlow": "UQ_ExpectedWaitTime",
                                               "intuLocalPhone": "4167884774", "intuLocale": "",
                                               "intuMeetingMessage": "Thank you for calling Intuit. We are currently closed for a company meeting. Please try your call again later.",
                                               "intuMenu": "QBOSubMenuOpt1:2", "intuMenuRetry": "0",
                                               "intuMissedCallMessage": "",
                                               "intuMonitorMessage": "One moment while we connect you with a representative. This call may be monitored and recorded by Intuit for quality assurance purposes.",
                                               "intuOfferQualityFeedback": "false", "intuOldestContactAge": "0",
                                               "intuPCFlag": "", "intuParseAttempt": "5", "intuParseKey": "-",
                                               "intuParseKey1": "LITE", "intuParseKey2": "latinum",
                                               "intuParseKey3": "old", "intuParseKey4": "ilver", "intuParseKey5": "-",
                                               "intuPhoneFormatLambda": "arn:aws:lambda:us-east-1:348016918056:function:intuit-formatPhoneNumber-default-prd-us-east-1",
                                               "intuPhoneNumber": "+14167884774",
                                               "intuPlayMissedCallMessageEnabled": "",
                                               "intuPlayMissedCallWaitDurationMS": "", "intuPracticeType": "",
                                               "intuPriority": "HIGH",
                                               "intuQueueArn": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/queue/a7e0027f-c43b-4ed8-aa07-be972ec9cc81",
                                               "intuQueueLoop": "dynamic",
                                               "intuQueueName": "sbseg-ol_acct_en_can_platinum_phn",
                                               "intuQueueType": "", "intuRating": "", "intuRegionCode": "CA",
                                               "intuReleaseNote": "TEST", "intuRoutingAge": "0",
                                               "intuSchedule": "Bypass", "intuScheduleBypassEnabled": "false",
                                               "intuScheduleStatus": "Open", "intuScreenPopEnabled": "true",
                                               "intuScreenPopParameters": "intuCaseNumber=intuCaseNumber,intuCompanyId=intuCompanyId,intuCustomerAccountNumber=intuCustomerAccountNumber,intuPhoneNumber=intuPhoneNumber,intuCaseId=intuCaseId,intuUniversalIdentifier=intuUniversalIdentifier,intuLastContactId=intuContactId,intuQueueName=intuQueueName,p1=intuScreenPopPriority,intuTransfer=intuTransfer",
                                               "intuScreenPopPriority": "intuCaseNumber|intuCaseId|intuCompanyId|intuCustomerAccountNumber|intuPhoneNumber",
                                               "intuScreenPopUri": "/apex/Intuit_CCP_CTI_Screen_Pop?",
                                               "intuStoreCustomerInputRetry": "1", "intuStoredInput": "4169896527",
                                               "intuTemporality": "None", "intuTenantId": "17",
                                               "intuTierLevel": "NotFound",
                                               "intuTimeOfDayMessage": "Thank you for calling Intuit Canada. Our offices are currently closed. For Canada QBO - Please call back during our office hours, Monday to Friday, 9 am to 8 pm Eastern Standard Time. Or for Canada QBO Techincal Support, visit our webiste at https://quickbooks.intuit.com/ca/ For Canada Accountant - Please call back during our office hours, Monday to Friday, 9 am to 8pm Eastern Standard Time, and Saturday from 9 am - 6 pm Eastern Standard Time\nOr for Canada Accountant technical support, visit our website at quickbookscanada-francais.lc.intuit.com/quickbooks-accountant.",
                                               "intuTransfer": "true", "intuTransferType": "_TRANSFER",
                                               "intuUniversalIdentifier": "a373989e-2c38-4c25-984a-36ab10538449",
                                               "intuUqConfigLambdaArn": "arn:aws:lambda:us-east-1:348016918056:function:intuit-getUniversalQueueData-default-prd-us-east-1",
                                               "intuUqLeg": "5", "intuVocabName": "SBSEG_EN_UniversalQueueVocab",
                                               "intuVoicemailDestinationEmail": "", "intuVoicemailEnabled": "",
                                               "intuVoicemailInterrupt": "", "intuVoicemailMessageQueue": "",
                                               "intuVoicemailSendEmailForMissedCall": "", "intuYearsWithPcg": "",
                                               "inuInputRetry": "0", "looper": "3"}, "Channel": "VOICE",
                                "ConnectedToSystemTimestamp": "2019-08-13T18:01:18Z",
                                "ContactId": "a373989e-2c38-4c25-984a-36ab10538449",
                                "CustomerEndpoint": {"Address": "+14167884774", "Type": "TELEPHONE_NUMBER"},
                                "DisconnectTimestamp": "2019-08-13T19:09:37Z", "InitialContactId": None,
                                "InitiationMethod": "INBOUND", "InitiationTimestamp": "2019-08-13T18:01:18Z",
                                "InstanceARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539",
                                "LastUpdateTimestamp": "2019-08-13T19:12:59Z", "MediaStreams": [{"Type": "AUDIO"}],
                                "NextContactId": "11460ea0-b994-49a1-bfe4-f2e34bf2f237", "PreviousContactId": None,
                                "Queue": {
                                    "ARN": "arn:aws:connect:us-east-1:348016918056:instance/78f0690b-6fff-40de-b956-bc208c34a539/queue/9e27638f-7788-45fd-a4c9-ca25125649ab",
                                    "DequeueTimestamp": "2019-08-13T18:15:23Z", "Duration": 753,
                                    "EnqueueTimestamp": "2019-08-13T18:02:50Z",
                                    "Name": "sbseg-ol_qbo_en_can_advpayroll_phn"}, "Recording": {"DeletionReason": None,
                                                                                                 "Location": "intuit-connectcallrecordings-default-prd-us-east-1/connect/intuit-connect-americas-prd/CallRecordings/2019/08/13/a373989e-2c38-4c25-984a-36ab10538449_20190813T18:15_UTC.wav",
                                                                                                 "Status": "AVAILABLE",
                                                                                                 "Type": "AUDIO"},
                                "Recordings": [
                                    {"DeletionReason": None, "FragmentStartNumber": None, "FragmentStopNumber": None,
                                     "Location": "intuit-connectcallrecordings-default-prd-us-east-1/connect/intuit-connect-americas-prd/CallRecordings/2019/08/13/a373989e-2c38-4c25-984a-36ab10538449_20190813T18:15_UTC.wav",
                                     "MediaStreamType": "AUDIO", "ParticipantType": None, "StartTimestamp": None,
                                     "Status": "AVAILABLE", "StopTimestamp": None, "StorageType": "S3"}],
                                "SystemEndpoint": {"Address": "+18552531536", "Type": "TELEPHONE_NUMBER"},
                                "TransferCompletedTimestamp": None, "TransferredToEndpoint": None}
        self.put_item_client_error = ClientError({'Error': {'Code': 500, 'Message': 'Error Updating Item'}}, 'PutItem')
        self.get_item_client_error = ClientError({'Error': {'Code': 500, 'Message': 'Error Downloading Item'}},
                                                 'GetItem')
        self.sample_uuid = '1111'
        self.valid_item = {'uuid': {'S': self.sample_uuid}, 'agentId': {'S': 'mbaid1'},
                           'date': {'S': '2019-08-22T21:37:12Z'}, 'disposition': {'S': 'unknown'},
                           'duration': {'S': '00hr 07min 41s'}, 'customerName': {'S': 'NONE'},
                           'customerNameAsEntered': {'S': 'NONE'}, 'description': {'S': 'NONE'},
                           'type': {'S': 'OUTBOUND'}}
        self.valid_item_with_voicemail = {'uuid': {'S': self.sample_uuid}, 'agentId': {'S': 'mbaid1'},
                                          'date': {'S': '2019-08-22T21:37:12Z'}, 'disposition': {'S': 'LEFT_VOICEMAIL'},
                                          'duration': {'S': '00hr 07min 41s'}, 'customerName': {'S': 'NONE'},
                                          'customerNameAsEntered': {'S': 'NONE'}, 'description': {'S': 'NONE'},
                                          'type': {'S': 'OUTBOUND'}}
        self.conversations_url = 'https://contactconversations-qal.api.intuit.com/v1/conversations/universal_id'
        self.headers = {
            'Authorization': f'Intuit_APIKey intuit_apikey=testauth,intuit_apkey_version=1.0:,intuit_userid=test_user',
            'Content-Type': 'application/json', 'intuit_locale': 'en_US', 'intuit_originatingip': '1.1.1.1'}
        self.universal_identifier = 'universal_id'

        self.bad_request_response = Mock(spec=Response)
        self.bad_request_response.status_code = 400

        self.mock_httperror_response = Mock(spec=Response)
        self.mock_httperror_response.status_code = 429
        self.mock_httperror_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        self.mock_success_response = Mock(spec=Response)
        self.mock_success_response.status_code = 200
        self.mock_success_response.raise_for_status.return_value = None
        self.mock_success_response.json.return_value = self.conversations_response_success

    @patch('ctr_record_reader.get_filename')
    @patch('ctr_record_reader.s3_client')
    @patch('ctr_record_reader.db_client')
    def test_handler_filename_is_none(self, mock_db_client, mock_s3_client, mock_get_filename):
        mock_get_filename.return_value = None
        res = ctr_record_reader.handler(self.s3_success_event, None)

        mock_get_filename.assert_called_once_with(
            'connectCtrAmericas2019/08/13/17/intuit-connectCtrAmericasFirehoseS3-default-prd-us-east-1-4-2019-08-13-19-12-49-19f4c4b8-01a6-4dfc-95d5-d6ecb00ea741')

        self.assertTrue(res == None)

    @patch('ctr_record_reader.download_file')
    @patch('ctr_record_reader.get_filename')
    @patch('ctr_record_reader.s3_client')
    @patch('ctr_record_reader.db_client')
    def test_handler_file_not_downloaded(self, mock_db_client, mock_s3_client, mock_get_filename, mock_download_file):
        mock_get_filename.return_value = "file"
        mock_download_file.return_value = False
        res = ctr_record_reader.handler(self.s3_success_event, None)

        mock_get_filename.assert_called_once_with(
            'connectCtrAmericas2019/08/13/17/intuit-connectCtrAmericasFirehoseS3-default-prd-us-east-1-4-2019-08-13-19-12-49-19f4c4b8-01a6-4dfc-95d5-d6ecb00ea741')
        mock_download_file.assert_called_once_with('bucket',
                                                   'connectCtrAmericas2019/08/13/17/intuit-connectCtrAmericasFirehoseS3-default-prd-us-east-1-4-2019-08-13-19-12-49-19f4c4b8-01a6-4dfc-95d5-d6ecb00ea741',
                                                   'file')

        self.assertTrue(res == None)

    @patch('ctr_record_reader.process_json_data')
    @patch('ctr_record_reader.open', create=True)
    @patch('ctr_record_reader.s3_client')
    @patch('ctr_record_reader.db_client')
    def test_process_json_data_no_conversation(self, mock_db_client, mock_s3_client, mock_file_open,
                                               mock_process_json_data):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            mock_file_open.return_value = StringIO(json.dumps(self.valid_json_data))
            mock_process_json_data.return_value = []
            res = ctr_record_reader.handler(self.s3_success_event, None)

            mock_process_json_data.assert_called_once_with(self.valid_json_data)

            self.assertTrue(res == None)

    def test_get_filename_none_parameter(self):
        res = ctr_record_reader.get_filename(None)
        self.assertTrue(res == None)

    @patch('ctr_record_reader.s3_client')
    def test_download_file_client_error(self, mock_s3_client):
        mock_s3_client.download_file.side_effect = self.get_item_client_error
        res = ctr_record_reader.download_file('bucket', 'path', 'filename')

        mock_s3_client.download_file.assert_called_once_with('bucket', 'path', f'/tmp/filename')

        self.assertTrue(res == False)

    def test_process_json_data_empty_json(self):
        res = ctr_record_reader.process_json_data({})
        self.assertTrue(res == False)

        res = ctr_record_reader.process_json_data({'Agent': None})
        self.assertTrue(res == False)

    def test_process_json_data_valid_payload_less_than_10_second_duration(self):
        self.valid_json_data['Agent']['AgentInteractionDuration'] = 9
        res = ctr_record_reader.process_json_data(self.valid_json_data)
        self.assertTrue(res == None)

    @patch('ctr_record_reader.uuid')
    @patch('ctr_record_reader.db_client')
    @patch('ctr_record_reader.process_attributes')
    @patch('ctr_record_reader.get_conversation')
    def test_process_json_data_valid_payload_less_than_80_second_duration(self, mock_get_conversation,
                                                                          mock_process_attributes, mock_db_client,
                                                                          mock_uuid):
        self.valid_json_data['Agent']['AgentInteractionDuration'] = 79
        mock_get_conversation.return_value = self.conversations_response_success
        mock_process_attributes.return_value = self.valid_item_with_voicemail
        mock_uuid.uuid1.return_value = self.sample_uuid
        mock_db_client.put_item.return_value = True

        res = ctr_record_reader.process_json_data(self.valid_json_data)

        mock_get_conversation.assert_called_once_with(self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        item_before_processing = {'uuid': {'S': self.sample_uuid}, 'agentId': {'S': 'stceb5953'},
                                  'date': {'S': '2019-08-13T18:01:18Z'}, 'disposition': {'S': 'LEFT_VOICEMAIL'},
                                  'duration': {'S': '00hr 01min 19s'}, 'customerName': {'S': 'NONE'},
                                  'customerNameAsEntered': {'S': 'NONE'}, 'description': {'S': 'NONE'},
                                  'type': {'S': 'INBOUND'}}
        mock_process_attributes.assert_called_once_with(item_before_processing, self.valid_json_data,
                                                        self.conversations_response_success,
                                                        self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        mock_db_client.put_item.assert_called_once_with(TableName='intuit-expert-contact-history-dev-us-east-1',
                                                        Item=self.valid_item_with_voicemail)

        self.assertTrue(res == self.valid_item_with_voicemail)

    @patch('ctr_record_reader.uuid')
    @patch('ctr_record_reader.db_client')
    @patch('ctr_record_reader.process_attributes')
    @patch('ctr_record_reader.get_conversation')
    def test_process_json_data_valid_payload_valid_conversation(self, mock_get_conversation, mock_process_attributes,
                                                                mock_db_client, mock_uuid):
        mock_get_conversation.return_value = self.conversations_response_success
        mock_process_attributes.return_value = self.valid_item
        mock_uuid.uuid1.return_value = self.sample_uuid
        mock_db_client.put_item.return_value = True

        res = ctr_record_reader.process_json_data(self.valid_json_data)

        mock_get_conversation.assert_called_once_with(self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        item_before_processing = {'uuid': {'S': self.sample_uuid}, 'agentId': {'S': 'stceb5953'},
                                  'date': {'S': '2019-08-13T18:01:18Z'}, 'disposition': {'S': 'unknown'},
                                  'duration': {'S': '00hr 37min 37s'}, 'customerName': {'S': 'NONE'},
                                  'customerNameAsEntered': {'S': 'NONE'}, 'description': {'S': 'NONE'},
                                  'type': {'S': 'INBOUND'}}
        mock_process_attributes.assert_called_once_with(item_before_processing, self.valid_json_data,
                                                        self.conversations_response_success,
                                                        self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        mock_db_client.put_item.assert_called_once_with(TableName='intuit-expert-contact-history-dev-us-east-1',
                                                        Item=self.valid_item)

        self.assertTrue(res == self.valid_item)

    @patch('ctr_record_reader.uuid')
    @patch('ctr_record_reader.get_conversation')
    def test_process_json_data_valid_payload_conversation_return_none(self, mock_get_conversation, mock_uuid):
        mock_get_conversation.return_value = None
        mock_uuid.uuid1.return_value = self.sample_uuid

        res = ctr_record_reader.process_json_data(self.valid_json_data)

        mock_get_conversation.assert_called_once_with(self.valid_json_data['Attributes']['intuUniversalIdentifier'])

        self.assertTrue(res == None)

    @patch('ctr_record_reader.uuid')
    @patch('ctr_record_reader.db_client')
    @patch('ctr_record_reader.process_attributes')
    @patch('ctr_record_reader.get_conversation')
    def test_process_json_data_db_client_raise_clienterror(self, mock_get_conversation, mock_process_attributes,
                                                           mock_db_client, mock_uuid):
        mock_get_conversation.return_value = self.conversations_response_success
        mock_process_attributes.return_value = self.valid_item
        mock_uuid.uuid1.return_value = self.sample_uuid
        mock_db_client.put_item.side_effect = self.put_item_client_error

        res = ctr_record_reader.process_json_data(self.valid_json_data)

        mock_get_conversation.assert_called_once_with(self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        item_before_processing = {'uuid': {'S': self.sample_uuid}, 'agentId': {'S': 'stceb5953'},
                                  'date': {'S': '2019-08-13T18:01:18Z'}, 'disposition': {'S': 'unknown'},
                                  'duration': {'S': '00hr 37min 37s'}, 'customerName': {'S': 'NONE'},
                                  'customerNameAsEntered': {'S': 'NONE'}, 'description': {'S': 'NONE'},
                                  'type': {'S': 'INBOUND'}}
        mock_process_attributes.assert_called_once_with(item_before_processing, self.valid_json_data,
                                                        self.conversations_response_success,
                                                        self.valid_json_data['Attributes']['intuUniversalIdentifier'])
        mock_db_client.put_item.assert_called_once_with(TableName='intuit-expert-contact-history-dev-us-east-1',
                                                        Item=self.valid_item)

        self.assertTrue(res == 'An error occurred (500) when calling the PutItem operation: Error Updating Item')

    @patch('ctr_record_reader.requests')
    def test_get_conversation_status_400(self, mock_requests):
        mock_requests.get.return_value = self.bad_request_response

        res = ctr_record_reader.get_conversation(self.universal_identifier)

        mock_requests.get.assert_called_once_with(self.conversations_url, headers=self.headers)

        self.assertTrue(res == 'NO_CONVERSATION')

    @patch('ctr_record_reader.requests')
    def test_get_conversation_raise_for_status_httperror(self, mock_requests):
        mock_requests.get.return_value = self.mock_httperror_response

        res = ctr_record_reader.get_conversation(self.universal_identifier)

        mock_requests.get.assert_called_once_with(self.conversations_url, headers=self.headers)

        self.assertTrue(res == None)

    @patch('ctr_record_reader.requests')
    def test_get_conversation_throw_exception(self, mock_requests):
        mock_requests.get.side_effect = Exception

        res = ctr_record_reader.get_conversation(self.universal_identifier)

        mock_requests.get.assert_called_once_with(self.conversations_url, headers=self.headers)
        self.assertTrue(res == None)

    @patch('ctr_record_reader.requests')
    def test_get_conversation_success(self, mock_requests):
        mock_requests.get.return_value = self.mock_success_response

        res = ctr_record_reader.get_conversation(self.universal_identifier)

        mock_requests.get.assert_called_once_with(self.conversations_url, headers=self.headers)
        self.mock_success_response.raise_for_status.assert_called_once_with()

        self.assertTrue(res == self.mock_success_response)

    @patch('ctr_record_reader.phonenumbers')
    def test_process_attributes_no_conversation_success(self, mock_phonenumbers):
        mock_phonenumbers.parse.return_value = 'mock number'
        mock_phonenumbers.format_number.return_value = '+14167884774'
        mock_phonenumbers.PhoneNumberFormat.E164 = None

        res = ctr_record_reader.process_attributes(self.valid_item, self.valid_json_data, 'NO_CONVERSATION',
                                                   self.universal_identifier)

        mock_phonenumbers.parse.assert_called_once_with('+14167884774', None)
        mock_phonenumbers.format_number.assert_called_once_with('mock number', None)

        self.assertTrue(res == self.valid_item)

    @patch('ctr_record_reader.phonenumbers')
    def test_process_attributes_with_conversation_success(self, mock_phonenumbers):
        mock_phonenumbers.parse.return_value = 'mock number'
        mock_phonenumbers.format_number.return_value = '+14167884774'
        mock_phonenumbers.PhoneNumberFormat.E164 = None
        self.conversations_response_success['participant']['telephone'] = '6174291336'
        self.mock_success_response.json.return_value = self.conversations_response_success

        res = ctr_record_reader.process_attributes(self.valid_item, self.valid_json_data, self.mock_success_response,
                                                   self.universal_identifier)

        self.assertTrue(res == self.valid_item)


if __name__ == "__main__":
    unittest.main()
