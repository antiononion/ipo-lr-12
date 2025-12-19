#Пример работы с класcами
from transport.vehicle import Vehicle
from transport.сlient import Client
def main():
    client1 = Client("Иван", 3)
    client2 = Client("Мария", 4)
    print(client1)
    print(client2)

    veh = Vehicle(23,client1)