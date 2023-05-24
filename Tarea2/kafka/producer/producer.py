import time
import json
from kafka import KafkaProducer
import random
import secrets

latencies = []

class IoTDevice:
    def __init__(self, device_id, delta_t):
        self.device_id = device_id
        self.delta_t = delta_t

    def generate_temperature(self):
        # Simulación de generación de datos
        data = {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'temperature': random.randint(0, 100)  # Ejemplo: temperatura
        }
        return data
    
    def generate_pressure(self):
        # Simulación de generación de datos
        data = {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'pressure': random.randint(0,100)
        }
        return data
    
    def generate_humidity(self):
        # Simulación de generación de datos
        data = {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'humidity': random.randint(0, 100),  # Ejemplo: humedad
        }
        return data
    
    def generate_ph(self):
        # Simulación de generación de datos
        data = {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'ph': random.randint(0, 100),  # Ejemplo: humedad
        }
        return data
    
    def generate_co(self):
        # Simulación de generación de datos
        data = {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'CO': random.randint(0, 100),  # Ejemplo: humedad
        }
        return data

    def send_data(self):
        #while True:
        data1 = self.generate_temperature()
        data2 = self.generate_pressure()
        data3 = self.generate_humidity()
        data4 = self.generate_ph()
        data5 = self.generate_co()
    
        json_data1 = json.dumps(data1)#, default=json_util.default).encode('utf-8')
        json_data2 = json.dumps(data2)
        json_data3 = json.dumps(data3)
        json_data4 = json.dumps(data4)
        json_data5 = json.dumps(data5)
        
        servidores_bootstrap = 'kafka:9092'
        
        topic1 = 'temperature'
        topic2 = 'pressure'
        topic3 = 'humidity'
        topic4 = 'ph'
        topic5 = 'CO'
        #generacion de distintos productores

        productor1 = KafkaProducer(bootstrap_servers=[servidores_bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all', retries=5)
        productor2 = KafkaProducer(bootstrap_servers=[servidores_bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all', retries=5)
        productor3 = KafkaProducer(bootstrap_servers=[servidores_bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all', retries=5)
        productor4 = KafkaProducer(bootstrap_servers=[servidores_bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all', retries=5)
        productor5 = KafkaProducer(bootstrap_servers=[servidores_bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all', retries=5)

        productors = [
            productor1, productor2, productor3, productor4, productor5
        ]
        
        start_time = time.time()
        
        #generar arreglo con los topicos para mandarlos de manera aleatoria
        #Send1 = productor1.send(topic1, value=json_data1)
        
        selectedProductor = secrets.choice(productors)

        if selectedProductor == productor1 :
            productor1.send(topic1, value=json_data1)
            productor1.flush()
        elif selectedProductor == productor2 :
            productor2.send(topic2, value=json_data2)
            productor2.flush()
        elif selectedProductor == productor3 :
            productor3.send(topic3, value=json_data3)
            productor3.flush()
        elif selectedProductor == productor4 :
            productor4.send(topic4, value=json_data4)
            productor4.flush()
        else :
            productor5.send(topic5, value=json_data5)
            productor5.flush()
        
        #result = Send1.get() #Espera a que el mensaje sea confirmado 
        
        #variable para ayudar a calcular la latencia de los mensajes    
        end_time = time.time()

        #arreglo que contendra todas las latencias para posteriormente exportarlas y graficarlas
        latency = end_time - start_time
        latencies.append(latency)

        print('La latencia del envio de los mensajes es ' + str(latency))
        
        #time.sleep(3)
        

# Configuración del sistema
n = 10 # Número de dispositivos IoT
delta_t = 0  # Intervalo de tiempo en segundos entre cada envío de datos

# Creación y ejecución de los dispositivos
devices = []

print('intento nuevo')
for i in range(n):
    device = IoTDevice(device_id=f"{i+1}", delta_t=delta_t)
    devices.append(device)
    device.send_data()

with open('datos.txt', 'w') as file:
    for data in latencies:
        file.write(str(data) + '\n')