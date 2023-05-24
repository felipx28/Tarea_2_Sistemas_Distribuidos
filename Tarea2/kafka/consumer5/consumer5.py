from kafka import KafkaConsumer

servidores_bootstrap = 'kafka:9092'
topic = 'CO'

consumidor = KafkaConsumer(topic, bootstrap_servers=[servidores_bootstrap])

for msg in consumidor:
    print(msg.value)

