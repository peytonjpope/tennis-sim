import random

class Player:
    
    def __init__(self, name, country, type):
        self.name = name
        self.country = country
        self.age = 18
        self.type = type
        
        match (type):
            case "Power":
                self.serve = random.randint(58, 60)
                self.forehand = 60
                self.backhand = 55
                self.slice = 50
                self.volley = 50
    
                self.clutch = 50
                self.endurance = 55
            case "Touch":
                self.serve = 55
                self.forehand = 55
                self.backhand = 50
                self.slice = 60
                self.volley = 60
    
                self.clutch = 50
                self.endurance = 50
            case "Mind":
                self.serve = 55
                self.forehand = 55
                self.backhand = 50
                self.slice = 50
                self.volley = 50
    
                self.clutch = 60
                self.endurance = 60
        
        self.rating = 0
        self.updateRating()
        
        self.points = 0
        self.energy = 100
        self.rank = 0  # Will be assigned based on points
        
    def updateRating(self):
        self.rating = (self.serve + self.forehand + self.backhand + self.slice + self.volley + self.clutch + self.endurance) / 7
        
    def print_stats(self):
        print("PLAYER INFO")
        print(self.name)
        print(self.country)
        print(f"{self.age} years old")
        print(f"Type: {self.type}")
        print(f"Points: {self.points}")
        print("="*30)
        
        print("RATINGS")
        print(f"Overall: {self.rating}")
        print(f"Serve: {self.serve}")
        print(f"Forehand: {self.forehand}")
        print(f"Backhand: {self.backhand}")
        print(f"Slice: {self.slice}")
        print(f"Volley: {self.volley}")
        print("="*30)
        
        print("INTANGIBLE RATINGS")
        print(f"Clutch: {self.clutch}")
        print(f"Endurance: {self.endurance}")
        print("="*30)
