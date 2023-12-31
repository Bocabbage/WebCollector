import pika

if __name__ == "__main__":
    credentials = pika.PlainCredentials(username="mikanani", password="mikanani_test")
    parameters = pika.ConnectionParameters("localhost", port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    # Queue def
    channel.queue_declare(queue="mikanani_dispatch_test", durable=True)
    
    # Exchange def
    channel.exchange_declare("mikanani-direct-ex", "direct", durable=True)
    
    # Exchange-Queue bind
    routing_key = "mikanani-subanime-download"
    channel.queue_bind(queue="mikanani_dispatch_test", exchange="mikanani-direct-ex", routing_key=routing_key)