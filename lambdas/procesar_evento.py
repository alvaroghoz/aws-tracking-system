import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('presencia_actual')

S3_BUCKET = 'agh-tracking-2025'  

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        device_mac = body['device_mac']
        zone = body['location']['zone']
        building = body['location'].get('building', 'unknown')
        timestamp = body['detected_at']
        vendor = body.get('vendor', 'unknown')
        rssi = body.get('rssi', -99)

        # 1. Guardar en S3
        s3_key = f"raw/{building}/{zone}/{device_mac}/{timestamp}.json"
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(body)
        )

        # 2. Consultar presencia actual
        response = table.get_item(Key={'device_mac': device_mac})
        item = response.get('Item')

        if item and item['zone'] == zone:
            # Sigue en la misma zona → actualiza solo timestamp
            table.update_item(
                Key={'device_mac': device_mac},
                UpdateExpression="SET last_seen = :ls, rssi = :r",
                ExpressionAttributeValues={
                    ':ls': timestamp,
                    ':r': rssi
                }
            )
        else:
            # Zona nueva o entrada por primera vez
            table.put_item(Item={
                'device_mac': device_mac,
                'zone': zone,
                'building': building,
                'check_in': timestamp,
                'last_seen': timestamp,
                'vendor': vendor,
                'rssi': rssi
            })

    return {
        'statusCode': 200,
        'body': 'Processed successfully'
    }
