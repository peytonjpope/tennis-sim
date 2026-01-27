import random

class Player:
    
    def __init__(self, name, country, type):
        self.main_character = False
        
        self.name = name
        self.country = country
        self.age = 18
        self.type = type
        
        # 52 zeroes
        self.point_history = [0] * 52
        
        self.rank_history = [250] * 52
        
        self.rank = 250
        
        self.career_high_rank = 250
        
        self.serve = 0
        self.backhand = 0
        self.forehand = 0
        self.slice = 0
        self.volley = 0

        self.clutch = 0
        self.endurance = 0

        self.serve = 0
        self.forehand = 0
        self.backhand = 0
        self.slice = 0
        self.volley = 0

        self.clutch = 0
        self.endurance = 0

        self.serve = 0
        self.forehand = 0
        self.backhand = 0
        self.slice = 0
        self.volley = 0

        self.clutch = 0
        self.endurance = 0
        
        self.rating = 0
        self.update_rating()
        
        self.points = 0
        self.energy = 100
        
        self.trophies = []
        
    def update_rating(self):
        self.rating = (self.serve + self.forehand + self.backhand + self.slice + self.volley + self.clutch + self.endurance) / 7
        
        self.rating = self.rating.__round__(1)
        
    def print_stats(self):
        print("PLAYER INFO")
        print(f"{self.name}, {self.country}")
        print(f"{self.age} years old")
        print(f"Player Type: {self.type}")
        print(f"ATP Points: {self.points}")
        print("")
        print("RATINGS")
        print(f"Overall: {self.rating}")
        print(f"Serve: {self.serve}")
        print(f"Forehand: {self.forehand}")
        print(f"Backhand: {self.backhand}")
        print(f"Slice: {self.slice}")
        print(f"Volley: {self.volley}")
        print("")
        print(f"Clutch: {self.clutch}")
        print(f"Endurance: {self.endurance}")
        print("="*30)

    def update_points(self):
        self.points = sum(self.point_history[-52:])  # Sum of last 52 weeks