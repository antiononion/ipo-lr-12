#Вариант 1
import json
import re
import dearpygui.dearpygui as dpg

from transport.transportcompany import TransportCompany
from transport.сlient import Client
from transport.vehicle import Truck, Train



company = TransportCompany()

# ---------------- ВАЛИДАЦИЯ ----------------

def validate_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-zА-Яа-я]{2,}", name))

def validate_weight(value: str) -> bool:
    try:
        value = float(value)
        return 0 < value <= 10000
    except ValueError:
        return False

# ---------------- УТИЛИТЫ ----------------

def set_status(text: str):
    dpg.set_value("status_text", text)

def show_error(message: str):
    with dpg.window(label="Ошибка", modal=True, no_close=True):
        dpg.add_text(message)
        dpg.add_button(
            label="OK",
            callback=lambda: dpg.delete_item(dpg.last_item())
        )

# ---------------- КЛИЕНТ ----------------

def open_add_client():
    with dpg.window(label="Добавить клиента", modal=True, tag="client_window"):
        dpg.add_input_text(label="Имя клиента", tag="client_name")
        dpg.add_input_text(label="Вес груза", tag="client_weight")
        dpg.add_checkbox(label="VIP", tag="client_vip")

        dpg.add_button(label="Сохранить", callback=save_client)
        dpg.add_same_line()
        dpg.add_button(
            label="Отмена",
            callback=lambda: dpg.delete_item("client_window")
        )

def save_client():
    name = dpg.get_value("client_name")
    weight = dpg.get_value("client_weight")
    vip = dpg.get_value("client_vip")

    if not validate_name(name):
        show_error("Имя должно содержать минимум 2 буквы")
        return

    if not validate_weight(weight):
        show_error("Вес должен быть от 0 до 10000")
        return

    client = Client(name, float(weight), vip)
    company.add_client(client)

    update_clients_table()
    set_status("Клиент добавлен")
    dpg.delete_item("client_window")

# ---------------- ТРАНСПОРТ ----------------

def open_add_vehicle():
    with dpg.window(label="Добавить транспорт", modal=True, tag="vehicle_window"):
        dpg.add_combo(
            ["Truck", "Train"],
            label="Тип транспорта",
            tag="vehicle_type"
        )
        dpg.add_input_text(
            label="Грузоподъемность",
            tag="vehicle_capacity"
        )

        dpg.add_button(label="Сохранить", callback=save_vehicle)
        dpg.add_same_line()
        dpg.add_button(
            label="Отмена",
            callback=lambda: dpg.delete_item("vehicle_window")
        )

def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")
    capacity = dpg.get_value("vehicle_capacity")

    if not validate_weight(capacity):
        show_error("Некорректная грузоподъемность")
        return

    capacity = float(capacity)

    if vehicle_type == "Truck":
        vehicle = Truck(capacity)
    elif vehicle_type == "Train":
        vehicle = Train(capacity)
    else:
        show_error("Тип транспорта не выбран")
        return

    company.add_vehicle(vehicle)
    update_vehicles_table()
    set_status("Транспорт добавлен")
    dpg.delete_item("vehicle_window")

# ---------------- ТАБЛИЦЫ ----------------

def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    for client in company.clients:
        with dpg.table_row(parent="clients_table"):
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.vip else "Нет")

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    for vehicle in company.vehicles:
        with dpg.table_row(parent="vehicles_table"):
            dpg.add_text(vehicle.class.name)
            dpg.add_text(str(vehicle.capacity))
            dpg.add_text(str(vehicle.loaded))

# ---------------- РАСПРЕДЕЛЕНИЕ ----------------

def distribute_cargo():
    company.distribute_cargo()
    set_status("Грузы распределены")
    show_distribution_result()

> Онгон:
def show_distribution_result():
    with dpg.window(label="Результат распределения", modal=True):
        for line in company.results:
            dpg.add_text(line)

# ---------------- ЭКСПОРТ ----------------

def export_results():
    if not company.results:
        show_error("Нет данных для экспорта")
        return

    with open("distribution_results.json", "w", encoding="utf-8") as f:
        json.dump(company.results, f, ensure_ascii=False, indent=2)

    set_status("Результаты сохранены в файл")

# ---------------- GUI ----------------

dpg.create_context()

with dpg.viewport_menu_bar():
    with dpg.menu(label="Файл"):
        dpg.add_menu_item(
            label="Экспорт результата",
            callback=export_results
        )
    with dpg.menu(label="О программе"):
        dpg.add_menu_item(
            label="Информация",
            callback=lambda: show_error(
                "Графическое приложение\nРазработчик: ФИО\nВариант: X"
            )
        )

with dpg.window(label="Управление перевозками", width=1000, height=600):
    with dpg.group(horizontal=True):
        dpg.add_button(label="Добавить клиента", callback=open_add_client)
        dpg.add_button(label="Добавить транспорт", callback=open_add_vehicle)
        dpg.add_button(label="Распределить грузы", callback=distribute_cargo)

    dpg.add_text("Клиенты")
    with dpg.table(header_row=True, tag="clients_table"):
        dpg.add_table_column(label="Имя")
        dpg.add_table_column(label="Вес")
        dpg.add_table_column(label="VIP")

    dpg.add_text("Транспорт")
    with dpg.table(header_row=True, tag="vehicles_table"):
        dpg.add_table_column(label="Тип")
        dpg.add_table_column(label="Грузоподъемность")
        dpg.add_table_column(label="Загружено")

    dpg.add_text("", tag="status_text")

dpg.create_viewport(title="Transport Company GUI", width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
