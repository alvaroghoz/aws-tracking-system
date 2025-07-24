import boto3
import json
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = 'presencia_actual'
BUCKET_NAME = 'agh-tracking-2025'

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()

    items = response.get('Items', [])
    resumen = []

    for item in items:
        try:
            device_mac = item['device_mac']
            zone = item['zone']
            check_in = datetime.fromisoformat(item['check_in'])
            last_seen = datetime.fromisoformat(item['last_seen'])
            duration = (last_seen - check_in).total_seconds() / 60  # minutos

            resumen.append({
                'device_mac': device_mac,
                'zone': zone,
                'duration_minutes': round(duration, 2),
                'vendor': item.get('vendor', ''),
                'last_seen': item['last_seen']
            })
        except Exception as e:
            print(f"Error procesando item {item}: {e}")

    # Guardar en S3
    fecha_hoy = datetime.utcnow().date().isoformat()
    key = f"reports/{fecha_hoy}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(resumen, indent=2, default=str),
        ContentType='application/json'
    )

    print(f"Reporte generado con {len(resumen)} registros y guardado en {key}")

    return {
        'statusCode': 200,
        'body': f"Reporte diario generado con éxito ({len(resumen)} registros)"
    }
