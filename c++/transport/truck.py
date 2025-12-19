import vehicle
class Truck:
    def __init__(self, max_weight, color):
        self.max_weight = max_weight
        self.color = color
        self.current_weight = 0
    
    def load_cargo(self, weight):
        if self.current_weight + weight <= self.max_weight:
            self.current_weight += weight
            return True
        return False
    
    def get_available_capacity(self):
        return self.max_weight - self.current_weight