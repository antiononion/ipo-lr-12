import vehicle
class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            return False
        self.vehicles.append(vehicle)
        return True
    
    def list_vehicles(self):
        return self.vehicles
    
    def add_client(self, client):
        if client in self.clients:
            return False
        self.clients.append(client)
        return True
    
    def optimize_cargo_distribution(self):
        # Сортируем клиентов: VIP сначала
        sorted_clients = sorted(self.clients, key=lambda c: (not c.is_vip, -c.cargo_weight))
        
        # Сортируем транспорт по грузоподъемности
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.max_weight, reverse=True)
        
        # Сбрасываем загрузку транспорта
        for vehicle in self.vehicles:
            vehicle.current_weight = 0
        
        used_vehicles = []
        
        for client in sorted_clients:
            client_served = False
            
            # Сначала пробуем загрузить в уже используемый транспорт
            for vehicle in used_vehicles:
                if vehicle.get_available_capacity() >= client.cargo_weight:
                    if vehicle.load_cargo(client.cargo_weight):
                        client_served = True
                        break
            
            # Если не поместилось, ищем новый транспорт
            if not client_served:
                for vehicle in sorted_vehicles:
                    if vehicle not in used_vehicles and vehicle.max_weight >= client.cargo_weight:
                        if vehicle.load_cargo(client.cargo_weight):
                            used_vehicles.append(vehicle)
                            client_served = True
                            break
        
        return used_vehicles