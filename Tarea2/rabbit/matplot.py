import matplotlib.pyplot as plt 

with open('C:/Users/felip/Desktop/semestre 1-2023/sistemas distribuidos/tarea2/rabbit/datosRabbitMQ.txt', 'r') as File:
    archivo = File.read()
    datos = [float(dato) for dato in archivo.split()]


plt.plot(datos)

plt.ylabel('Tiempo')
plt.xlabel('Mensajes')
plt.title('Gráfico ResponseTime')
plt.show()