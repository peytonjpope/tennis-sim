import player
import random
import math


# Variables
week = 1
year = 2026

ENERGY_PER_MATCH = 5

# Create Player
name = ""
country = ""
type = ""
type_select = 0
name = input("Name: ")
country = input("Country: ")

while (type_select <= 0 or type_select > 3):
    print("\n1. Power\n2. Touch\n3. Mind")
    print("="*30)
    type_select = int(input("Select a type: "))

match (type_select):
    case 1:
        type = "Power"
    case 2:
        type = "Touch"
    case 3:
        type = "Mind"

mc = player.Player(name, country, type)

print("New Career Created!")
mc.print_stats()

# Generate all players 250
# TODO: Generate 250 CPU players here with random names, countries, types
# Store in a list called 'players'
# Assign ranks based on initial ratings

# TODO: Load tournaments from JSON file
# Expected format: [{"name": "US Open", "pts": 2000, "participants": 128, "slam": true, "surface": "hard_outdoor", "week": 35}, ...]
# Store in a list called 'all_tournaments'

# Tutorial

train_options = ['SERVE', 'FOREHAND', 'BACKHAND', 'SLICE', 'VOLLEY', 'CLUTCH', 'ENDURANCE', 'REST']

# Main
# year loop
loop = True
while (loop):
    while (week < 53):
        week_tournaments = [tourney for tourney in all_tournaments if tourney.week == week]
        print(f"WEEK {week} of the {year} season")
        
        print(f"Current Rank: {mc.rank}")
        print(f"Current Energy: {mc.energy}")
        
        print("Tournaments")
        print("="*30)
        n = 1
        for t in week_tournaments:
            print(f"{n}. {t.name} - {t.pts} ({t.surface})")
            n += 1
        
        selection = 0
        while (selection != 1 and selection != 2):
            selection = int(input("(1) Play or (2) Train/Rest?: "))
        
        # Play
        if selection == 1:
            selection = 0
            while (selection <= 0 or selection > len(week_tournaments)):
                selection = int(input("Select Tournament: "))
            
            selected_tournament = week_tournaments[selection - 1]
            
            required_energy = int(math.log2(selected_tournament.participants)) * ENERGY_PER_MATCH
            if mc.energy < required_energy:
                print("Not enough energy")
                selection = 0
            else:
                # TODO: Player will play this tournament
                pass

        # Train/Rest        
        elif selection == 2:
            # Options
            n = 1
            for opt in train_options:
                print(f"{n}. {opt}")
                n += 1
            
            # Pick 2
            pick = 1
            while (pick < 3):
                selection = 0
                while (selection <= 0 or selection > len(train_options)):
                    selection = int(input(f"Select an option ({pick} of 2): "))
                
                selected_option = train_options[selection - 1]
                
                match (selected_option):
                    case "REST":
                        mc.energy += 20
                    case "SERVE":
                        mc.serve += 1
                    case "FOREHAND":
                        mc.forehand += 1
                    case "BACKHAND":
                        mc.backhand += 1
                    case "SLICE":
                        mc.slice += 1
                    case "VOLLEY":
                        mc.volley += 1
                    case "CLUTCH":
                        mc.clutch += 1
                    case "ENDURANCE":
                        mc.endurance += 1
                
                pick += 1
        
        # Sim Tournaments
        for tourney in week_tournaments:
            if tourney == selected_tournament:
                # TODO: watch tournament (player participates)
                pass
            else:
                # TODO: sim tournament (CPU only)
                pass
        
        week += 1


    # End of Season
    # Summary
    print(f"{year} Season Summary")
    # TODO: Display player stats, achievements, etc.

    # Adjust CPU ratings
    # TODO: Define age ranges (young, prime, old)
    for player in players:
        if player.age in young:
            # TODO: increase likely
            pass
        if player.age in prime:
            # TODO: minimal increase
            pass
        if player.age in old:
            # TODO: decrease
            pass
            # TODO: random chance retire
    
    week = 1
    year += 1


def simulate_tournament(tournament, participants):
    
    player_remaining = participants

    while(player_remaining > 1):
        next_round = []
        for i in range(0, len(player_remaining)):
            player1 = player_remaining[i]
            player2 = player_remaining[len(player_remaining -i)]
            winner = simulate_match(tournament, player1, player2)
            next_round.append(winner)



def simulate_match(tournamet, player1, player2):
    
    
    winner = player1
    return winner