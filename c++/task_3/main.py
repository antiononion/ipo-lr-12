from transport.vehicle import Vehicle
from transport.truck import Truck
from transport.train import Train
from transport.сlient import Client
from transport.transportcompany import TransportCompany

def main():
    # Создаем компанию
    company = TransportCompany("FastTrans")

    # Создаем транспорт
    truck1 = Truck(10, "Красный")
    truck2 = Truck(8, "Синий")
    train1 = Train(50, 10)

    # Добавляем транспорт в компанию
    company.add_vehicle(truck1)
    company.add_vehicle(truck2)
    company.add_vehicle(train1)

    # Создаем клиентов
    client1 = Client("Иван", 4, vip=True)
    client2 = Client("Мария", 7)
    client3 = Client("Петр", 3)
    client4 = Client("Анна", 6, vip=True)
    client5 = Client("Игорь", 9)

    # Добавляем клиентов
    company.add_client(client1)
    company.add_client(client2)
    company.add_client(client3)
    company.add_client(client4)
    company.add_client(client5)

    # Распределяем грузы
    company.optimize_cargo_distribution()

    # Вывод всех транспортных средств
    for v in company.list_vehicles():
        print(v)

if __name__ == "__main__":
    main()