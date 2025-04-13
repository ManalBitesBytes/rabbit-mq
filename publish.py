import pika
import json
import uuid

username = 'admin'
password = 'admin'  # Replace with your actual password
credentials = pika.PlainCredentials(username, password)
conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', credentials)
)

channel = conn.channel()

channel.exchange_declare(exchange='orders', exchange_type='direct')

order = {
    'id': str(uuid.uuid4()),
    'user_email': 'myemail.com',
    'product': 'Jacket',
    'quantity': 2
}

channel.basic_publish(exchange='orders',
                      routing_key='order.report',
                      body=json.dumps(order)
                      )
print(" [x] Sent report message")

channel.basic_publish(exchange='orders',
                      routing_key='order.notify',
                      body=json.dumps({'user_email': order['user_email']})
                      )
print(" [x] Sent notify message")

conn.close()