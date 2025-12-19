class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

    def __str__(self):
        vip_status = "VIP" if self.is_vip else "Регулярный"
        return f"Клиент: {self.name}, Груз: {self.cargo_weight} кг, Статус: {vip_status}"