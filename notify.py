import pika
import json


username = 'admin'
password = 'admin'  # Replace with your actual password
credentials = pika.PlainCredentials(username, password)
conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', credentials)
)

channel = conn.channel()

queue = channel.queue_declare('order_notify')
queue_name = queue.method.queue

channel.queue_bind(exchange='orders',
                   routing_key='order.notify',
                   queue=queue_name)
def callback(channel, method, properties, body):
    payload = json.loads(body)
    print("[x] notifying {}".format(payload['user_email']))
    print("[x] Done")
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)


print("* waiting for notifying messages. To exit press CRTL")

channel.start_consuming()