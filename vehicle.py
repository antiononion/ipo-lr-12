import uuid

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []
    
    def load_cargo(self, client):
        if not hasattr(client, 'cargo_weight'):
            return False
        
        if self.current_load + client.cargo_weight <= self.capacity:
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
            return True
        return False
    
    def __str__(self):
        return f"ID: {self.vehicle_id}, Грузоподъемность: {self.capacity}т, Загружено: {self.current_load}т"