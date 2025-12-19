from transport.vehicle import Vehicle
from transport.truck import Truck
from transport.train import Train
from transport.сlient import Client
from transport.transportcompany import TransportCompany

def print_menu():
    print("\n==== Меню ====")
    print("1. Добавить транспортное средство")
    print("2. Добавить клиента")
    print("3. Распределить грузы")
    print("4. Показать список транспортных средств")
    print("5. Показать список клиентов")
    print("0. Выход")
    print("================")

def main():
    company = TransportCompany("FastTrans")
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        if choice == '1':
            print("Выберите тип транспорта:")
            print("1. Грузовик")
            print("2. Поезд")
            t_type = input("Введите номер: ")
            capacity = float(input("Введите грузоподъемность (в тоннах): "))
            if t_type == '1':
                color = input("Введите цвет грузовика: ")
                vehicle = Truck(capacity, color)
            elif t_type == '2':
                num_cars = int(input("Введите количество вагонов: "))
                vehicle = Train(capacity, num_cars)
            else:
                print("Некорректный выбор.")
                continue
            company.add_vehicle(vehicle)
            print("Транспортное средство добавлено.")
        elif choice == '2':
            name = input("Введите имя клиента: ")
            cargo_weight = float(input("Введите вес груза клиента (в тоннах): "))
            vip_input = input("Это VIP-клиент? (да/нет): ").strip().lower()
            vip = True if vip_input == 'да' else False
            client = Client(name, cargo_weight, vip)
            company.add_client(client)
            print("Клиент добавлен.")
        elif choice == '3':
            print("Начинается распределение грузов...")
            company.optimize_cargo_distribution()
        elif choice == '4':
            print("\nСписок транспортных средств:")
            for v in company.list_vehicles():
                print(v)
        elif choice == '5':
            print("\nСписок клиентов:")
            for c in company.clients:
                print(c)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()