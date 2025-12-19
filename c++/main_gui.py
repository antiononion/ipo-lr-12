#Вариант 1
import json
import os
import re
from typing import List

import dearpygui.dearpygui as dpg

from transport.transportcompany import TransportCompany
from transport.сlient import Client
from transport.vehicle import Truck, Train

company = TransportCompany("MyTransport")
last_distribution: List = []

NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁё\s\-]{2,}$")


def validate_name(name: str) -> bool:
    return bool(NAME_RE.fullmatch(name.strip()))


def validate_weight(w: str) -> bool:
    try:
        v = float(w)
        return 0 < v <= 10000
    except:
        return False

def show_modal_message(title: str, message: str):
    tag = f"modal_{title}"

    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(tag=tag, label=title, modal=True, no_close=False, width=460, height=200):
        dpg.add_text(message)
        dpg.add_spacer(height=10)
        dpg.add_button(label="OK", width=80, callback=lambda *_: dpg.delete_item(tag))


def set_status(msg: str):
    if dpg.does_item_exist("status_text"):
        dpg.set_value("status_text", msg)


def refresh_clients_table():
    body = "clients_table_body"

    if not dpg.does_item_exist(body):
        return

    children = dpg.get_item_children(body, 1)
    if children:
        for ch in children:
            dpg.delete_item(ch)

    for c in company.clients:
        with dpg.table_row(parent=body):
            dpg.add_text(c.name)
            dpg.add_text(str(c.cargo_weight))
            dpg.add_text("Yes" if c.is_vip else "No")


def refresh_vehicles_table():
    body = "vehicles_table_body"

    if not dpg.does_item_exist(body):
        return

    children = dpg.get_item_children(body, 1)
    if children:
        for ch in children:
            dpg.delete_item(ch)

    for v in company.vehicles:
        with dpg.table_row(parent=body):
            dpg.add_text(v.vehicle_id)
            dpg.add_text(type(v).__name__)
            dpg.add_text(str(v.capacity))
            dpg.add_text(str(v.current_load))
            dpg.add_text(str(len(v.clients_list)))


def open_add_client_window():
    tag = "win_add_client"
    if dpg.does_item_exist(tag):
        dpg.show_item(tag)
        return

    with dpg.window(label="Add Client", tag=tag, modal=True, width=400, height=250):

        dpg.add_text("Client Name:")
        dpg.add_input_text(tag="client_name")

        dpg.add_spacer(height=6)
        dpg.add_text("Cargo Weight (kg):")
        dpg.add_input_text(tag="client_weight")

        dpg.add_spacer(height=6)
        dpg.add_checkbox(label="VIP", tag="client_vip")

        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_new_client)
            dpg.add_button(label="Cancel", callback=lambda *_: dpg.delete_item(tag))


def save_new_client():
    name = dpg.get_value("client_name")
    weight = dpg.get_value("client_weight")
    vip = dpg.get_value("client_vip")

    if not validate_name(name):
        show_modal_message("Error", "Invalid name")
        return

    if not validate_weight(weight):
        show_modal_message("Error", "Cargo weight must be between 1 and 10000 kg")
        return

    client = Client(name=name.strip(), cargo_weight=float(weight), is_vip=vip)
    company.add_client(client)

    refresh_clients_table()
    set_status(f"Client '{client.name}' added")

    dpg.delete_item("win_add_client")


def on_vehicle_type_change():
    tp = dpg.get_value("vehicle_type")
    if tp == "Truck":
        dpg.show_item("truck_color")
        dpg.hide_item("train_cars")
    else:
        dpg.hide_item("truck_color")
        dpg.show_item("train_cars")


def open_add_vehicle_window():
    tag = "win_add_vehicle"

    if dpg.does_item_exist(tag):
        dpg.show_item(tag)
        return

    with dpg.window(label="Add Transport", tag=tag, modal=True, width=400, height=260):

        dpg.add_text("Transport Type:")
        dpg.add_combo(["Truck", "Train"], default_value="Truck",
                      tag="vehicle_type", callback=lambda *_: on_vehicle_type_change())

        dpg.add_spacer(height=6)
        dpg.add_text("Load Capacity (t):")
        dpg.add_input_float(tag="vehicle_capacity", default_value=1.0, min_value=0.1)

        dpg.add_text("Color (Truck):")
        dpg.add_input_text(tag="truck_color", default_value="white")

        dpg.add_text("Number of Cars (Train):")
        dpg.add_input_int(tag="train_cars", default_value=1)

        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_new_vehicle)
            dpg.add_button(label="Cancel", callback=lambda *_: dpg.delete_item(tag))

    on_vehicle_type_change()


def save_new_vehicle():
    tp = dpg.get_value("vehicle_type")
    cap = dpg.get_value("vehicle_capacity")

    if cap <= 0:
        show_modal_message("Error", "Load capacity must be > 0")
        return

    if tp == "Truck":
        color = dpg.get_value("truck_color")
        vehicle = Truck(capacity=cap, color=color)
    else:
        cars = dpg.get_value("train_cars")
        vehicle = Train(capacity=cap, number_of_cars=cars)

    company.add_vehicle(vehicle)

    refresh_vehicles_table()
    set_status("Transport added")

    dpg.delete_item("win_add_vehicle")

def delete_selected_clients():
    if not company.clients:
        show_modal_message("Error", "No clients")
        return

    names = [c.name for c in company.clients]

    with dpg.window(label="Delete Client", modal=True, tag="del_client_win", width=320, height=150):
        dpg.add_text("Select Client:")
        dpg.add_combo(names, default_value=names[0], tag="del_client_choice")

        dpg.add_button(label="Delete", callback=confirm_delete_client)
        dpg.add_button(label="Cancel", callback=lambda *_: dpg.delete_item("del_client_win"))


def confirm_delete_client():
    sel = dpg.get_value("del_client_choice")
    company.clients = [c for c in company.clients if c.name != sel]
    refresh_clients_table()
    set_status(f"Client '{sel}' deleted")
    dpg.delete_item("del_client_win")

def delete_selected_vehicle():
    if not company.vehicles:
        show_modal_message("Error", "No transport")
        return

    ids = [v.vehicle_id for v in company.vehicles]

    with dpg.window(label="Delete Transport", modal=True, tag="del_vehicle_win", width=320, height=150):
        dpg.add_text("Select Transport ID:")
        dpg.add_combo(ids, default_value=ids[0], tag="del_vehicle_choice")

        dpg.add_button(label="Delete", callback=confirm_delete_vehicle)
        dpg.add_button(label="Cancel", callback=lambda *_: dpg.delete_item("del_vehicle_win"))


def confirm_delete_vehicle():
    sel = dpg.get_value("del_vehicle_choice")
    company.vehicles = [v for v in company.vehicles if v.vehicle_id != sel]
    refresh_vehicles_table()
    set_status(f"Transport '{sel}' deleted")
    dpg.delete_item("del_vehicle_win")


def perform_distribution():
    global last_distribution

    if not company.clients:
        show_modal_message("Error", "No clients")
        return

    if not company.vehicles:
        show_modal_message("Error", "No transport")
        return

    last_distribution = company.optimize_cargo_distribution()
    refresh_vehicles_table()

    text = ""
    for v in last_distribution:
        text += f"{type(v).__name__} {v.vehicle_id} ({v.current_load}/{v.capacity})\n"
        for c in v.clients_list:
            text += f"  - {c.name}: {c.cargo_weight} kg {'(VIP)' if c.is_vip else ''}\n"
        text += "\n"

    with dpg.window(label="Distribution Result", modal=True, tag="dist_window", width=500, height=400):
        dpg.add_input_text(default_value=text, multiline=True, readonly=True, width=470, height=330)
        dpg.add_button(label="Close", callback=lambda *_: dpg.delete_item("dist_window"))


def export_distribution_to_json():
    if not last_distribution:
        show_modal_message("Error", "No distribution data")
        return

    data = []

    for v in last_distribution:
        data.append({
            "id": v.vehicle_id,
            "type": type(v).__name__,
            "capacity": v.capacity,
            "current_load": v.current_load,
            "clients": [
                {"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip}
                for c in v.clients_list
            ]
        })

    with open("distribution.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    show_modal_message("Done", "distribution.json saved")


def build_gui():
    dpg.create_context()

    dpg.create_viewport(title="LR 12 — GUI", width=1100, height=700)

    with dpg.window(tag="main_window", label="LR 12 — Transport Company", width=1100, height=700):

        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Export JSON", callback=export_distribution_to_json)
            with dpg.menu(label="About Program"):
                dpg.add_menu_item(label="Info",
                                  callback=lambda *_: show_modal_message(
                                      "About Program",
                                      "LR 12\nVariant X\nDeveloper: Your Name"
                                  ))

        dpg.add_spacer(height=6)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Add Client", width=160, callback=open_add_client_window)
            dpg.add_button(label="Delete Client", width=160, callback=delete_selected_clients)
            dpg.add_button(label="Add Transport", width=160, callback=open_add_vehicle_window)
            dpg.add_button(label="Delete Transport", width=160, callback=delete_selected_vehicle)
            dpg.add_button(label="Distribute Cargo", width=200, callback=perform_distribution)

        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):

            with dpg.child_window(width=500, height=480):
                dpg.add_text("Clients")
                dpg.add_separator()
                with dpg.table(tag="clients_table", header_row=True,
                               resizable=True, policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Weight (kg)")
                    dpg.add_table_column(label="VIP")
                    dpg.add_table_row(tag="clients_table_body")

            with dpg.child_window(width=580, height=480):
                dpg.add_text("Transport")
                dpg.add_separator()
                with dpg.table(tag="vehicles_table", header_row=True,
                               resizable=True, policy=dpg.mvTable_SizingStretchProp):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Type")
                    dpg.add_table_column(label="Capacity")
                    dpg.add_table_column(label="Loaded")
                    dpg.add_table_column(label="Clients")
                    dpg.add_table_row(tag="vehicles_table_body")

        dpg.add_spacer(height=12)
        dpg.add_text("", tag="status_text")
        set_status("Ready")

    dpg.setup_dearpygui()

    refresh_clients_table()
    refresh_vehicles_table()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":

    build_gui()