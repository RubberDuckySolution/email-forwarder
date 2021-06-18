import json

from pprint import pprint as pp
from email_handler import EmailHandler

def lambda_handler(event, context):  
    for record in event['Records']:
        try:
            pp(record['Sns']['Message'])

            email_content = json.loads(record['Sns']['Message'])['content']
            email_handler = EmailHandler(email_content)
            email_handler.handle_mail()
        except Exception as e:
            print(f'Error forwarding email: {e}')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Execution Successful!')
    }
