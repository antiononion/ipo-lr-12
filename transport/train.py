import vehicle
class Train:
    def __init__(self, max_weight, number_of_cars):
        self.max_weight = max_weight
        self.number_of_cars = number_of_cars
        self.current_weight = 0
    
    def load_cargo(self, weight):
        if self.current_weight + weight <= self.max_weight:
            self.current_weight += weight
            return True
        return False
    
    def get_available_capacity(self):
        return self.max_weight - self.current_weight