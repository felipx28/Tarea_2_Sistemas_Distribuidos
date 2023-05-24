import time
import json
import pika #libreria necesaria para hacer uso de rabbitmq en python
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

        json_data1 = json.dumps(data1)
        json_data2 = json.dumps(data2)
        json_data3 = json.dumps(data3)
        json_data4 = json.dumps(data4)
        json_data5 = json.dumps(data5)

        conn = pika.BlockingConnection(pika.ConnectionParameters('localhost')) #define donde estara el broker, en este caso, en la maquina local

        channel1 = conn.channel() #crea un nuevo canal de comunicacion 
        channel1.queue_declare(queue='temperature') #Declaracion del nombre de la cola
        
        channel2 = conn.channel()
        channel2.queue_declare(queue='pressure')

        channel3 = conn.channel()
        channel3.queue_declare(queue='humidity')

        channel4 = conn.channel()
        channel4.queue_declare(queue='ph')

        channel5 = conn.channel()
        channel5.queue_declare(queue='CO')
        
        start_time = time.time()

        channels = [
            channel1, channel2, channel3, channel4, channel5
        ]

        selectedChannels = secrets.choice(channels)

        if selectedChannels == channel1 :
            channel1.basic_publish(exchange='',
                                routing_key='temperature',
                                body=json_data1)
            print(" [x] Sent %r" % json_data1)
        elif selectedChannels == channel2 :
            channel2.basic_publish(exchange='',
                                routing_key='pressure',
                                body=json_data2)
            print(" [x] Sent %r" % json_data2)
        elif selectedChannels == channel3 :
            channel3.basic_publish(exchange='',
                                routing_key='humidity',
                                body=json_data3)
            print(" [x] Sent %r" % json_data3)
        elif selectedChannels == channel4 :
            channel4.basic_publish(exchange='',
                                routing_key='ph',
                                body=json_data4)
            print(" [x] Sent %r" % json_data4)
        else :
            channel5.basic_publish(exchange='',
                                routing_key='CO',
                                body=json_data5)
            print(" [x] Sent %r" % json_data5)
        
            #se da forma al mensaje que se quiere mandar mediante un intercambio de un string vacio, indicando
            #tambien el nombre de la cola => queue='...', ademas del contenido del mensaje

        
        
        #variable para ayudar a calcular la latencia de los mensajes    
        end_time = time.time()

        #arreglo que contendra todas las latencias para posteriormente exportarlas y graficarlas
        latency = end_time - start_time
        latencies.append(latency)

            #paso final para finalizar nuestra aplicacion
        conn.close()

            # Aquí se realiza la lógica para enviar el json_data a través de la comunicación IoT
            # Puedes adaptar esta parte según el sistema que utilices para enviar los datos

            #print("Datos enviados:", json_data)
        time.sleep(self.delta_t)
        
# Configuración del sistema
n = 10000 # Número de dispositivos IoT
delta_t = 1  # Intervalo de tiempo en segundos entre cada envío de datos

# Creación y ejecución de los dispositivos
devices = []

print('intento nuevo')
for i in range(n):
    device = IoTDevice(device_id=f"{i+1}", delta_t=delta_t)
    devices.append(device)
    device.send_data()
    
with open('datosRabbitMQ.txt', 'w') as file:
    for data in latencies:
        file.write(str(data) + '\n')