import base64
import json

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        print("Decoded payload: " + payload.decode('utf-8'))
    return 'Successfully processed {} records.'.format(len(event['Records']))