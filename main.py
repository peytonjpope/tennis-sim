from player import Player
import random
import math
import json
from tournament import Tournament
import names

# CONSTANTS
COUNTRIES = ["USA", "ESP", "SRB", "FRA", "AUS",
             "ITA", "GER", "GBR", "RUS", "ARG",
             "SUI", "JPN", "CAN", "CRO", "SWE", 
             "AUT", "NED", "BRA", "NOR", "GRE",
             "POL", "CZE", "DEN", "CHN", "MEX"]

ENERGY_PER_SET = 2

TYPES = ['Grass', 'Clay', 'Hard']

TRAIN_OPTIONS = ['SERVE', 'FOREHAND', 'BACKHAND', 'SLICE', 'VOLLEY', 'CLUTCH', 'ENDURANCE', 'REST']

# Tournament Weeks
AO_WEEK = 3
FO_WEEK = 22
WIM_WEEK = 27
USO_WEEK = 35
FINALS_WEEK = 46

ATP_FINALS_POINTS_PER_ROUND = [
    200,   # QF (Quarterfinals) - 4 losers
    500,   # SF (Semifinals) - 2 losers  
    1000,  # Final - 1 loser
    1500   # Winner
]

# Points awarded per round
POINTS_PER_ROUND_GS = [
    10,    # R128
    45,    # R64
    90,    # R32
    180,   # R16
    360,   # QF
    720,   # SF
    1200,  # Final
    2000   # Winner
]

POINTS_PER_ROUND_1000 = [
    10,    # R64
    45,    # R32
    90,    # R16
    180,   # QF
    360,   # SF
    600,   # Final
    1000   # Winner
]

POINTS_PER_ROUND_500 = [
    20,    # R32
    45,    # R16
    90,    # QF
    180,   # SF
    300,   # Final
    500    # Winner
]

POINTS_PER_ROUND_250 = [
    10,    # R32
    20,    # R16
    45,    # QF
    90,    # SF
    150,   # Final
    250    # Winner
]

# Functions ----------------------------------

def generate_random_player(age = None):

    name = names.get_full_name(gender='male') 
    country = random.choice(COUNTRIES)
    type = random.choice(["Grass", "Clay", "Hard", "Hard"])
    
    player = Player(name, country, type)
    
    if age is not None:
        player.age = age
    else:
        player.age = random.randint(18, 36)
    
    level = random.choices(
        ["Elite", "High", "Medium", "Low"], 
        weights=[10, 25, 45, 20]
    )[0]

    match level:
        case "Elite":  # Top 10-25 players (rating ~90-96)
            match (type):
                case "Grass":
                    player.serve = random.randint(92, 99)
                    player.forehand = random.randint(80, 92)
                    player.backhand = random.randint(80, 92)
                    player.slice = random.randint(82, 94)
                    player.volley = random.randint(92, 99)
        
                    player.clutch = random.randint(88, 96)
                    player.endurance = random.randint(80, 92)
                case "Clay":
                    player.serve = random.randint(78, 90)
                    player.forehand = random.randint(92, 99)
                    player.backhand = random.randint(92, 99)
                    player.slice = random.randint(82, 92)
                    player.volley = random.randint(72, 85)
        
                    player.clutch = random.randint(88, 96)
                    player.endurance = random.randint(92, 99)
                case "Hard":
                    player.serve = random.randint(86, 94)
                    player.forehand = random.randint(86, 94)
                    player.backhand = random.randint(86, 94)
                    player.slice = random.randint(80, 90)
                    player.volley = random.randint(78, 88)
        
                    player.clutch = random.randint(92, 99)
                    player.endurance = random.randint(92, 99)
        
        case "High":  # Top 50 players (rating ~80-88)
            match (type):
                case "Grass":
                    player.serve = random.randint(82, 90)
                    player.forehand = random.randint(72, 83)
                    player.backhand = random.randint(72, 83)
                    player.slice = random.randint(75, 86)
                    player.volley = random.randint(82, 90)
        
                    player.clutch = random.randint(78, 88)
                    player.endurance = random.randint(72, 83)
                case "Clay":
                    player.serve = random.randint(70, 82)
                    player.forehand = random.randint(82, 90)
                    player.backhand = random.randint(82, 90)
                    player.slice = random.randint(73, 84)
                    player.volley = random.randint(65, 78)
        
                    player.clutch = random.randint(78, 88)
                    player.endurance = random.randint(82, 90)
                case "Hard":
                    player.serve = random.randint(76, 86)
                    player.forehand = random.randint(76, 86)
                    player.backhand = random.randint(76, 86)
                    player.slice = random.randint(70, 82)
                    player.volley = random.randint(68, 80)
        
                    player.clutch = random.randint(82, 90)
                    player.endurance = random.randint(82, 90)
        
        case "Medium":  # Solid players (rating 65-78)
            match (type):
                case "Grass":
                    player.serve = random.randint(72, 82)
                    player.forehand = random.randint(60, 72)
                    player.backhand = random.randint(58, 70)
                    player.slice = random.randint(62, 75)
                    player.volley = random.randint(70, 82)
        
                    player.clutch = random.randint(62, 75)
                    player.endurance = random.randint(60, 72)
                case "Clay":
                    player.serve = random.randint(58, 72)
                    player.forehand = random.randint(70, 82)
                    player.backhand = random.randint(70, 82)
                    player.slice = random.randint(60, 73)
                    player.volley = random.randint(55, 68)
        
                    player.clutch = random.randint(62, 75)
                    player.endurance = random.randint(72, 82)
                case "Hard":
                    player.serve = random.randint(65, 75)
                    player.forehand = random.randint(65, 75)
                    player.backhand = random.randint(65, 75)
                    player.slice = random.randint(60, 72)
                    player.volley = random.randint(60, 72)
        
                    player.clutch = random.randint(68, 78)
                    player.endurance = random.randint(68, 78)
        
        case "Low":  # Journey players (rating 50-65)
            match (type):
                case "Grass":
                    player.serve = random.randint(58, 68)
                    player.forehand = random.randint(48, 60)
                    player.backhand = random.randint(48, 60)
                    player.slice = random.randint(50, 62)
                    player.volley = random.randint(56, 66)
        
                    player.clutch = random.randint(50, 62)
                    player.endurance = random.randint(48, 60)
                case "Clay":
                    player.serve = random.randint(48, 60)
                    player.forehand = random.randint(58, 68)
                    player.backhand = random.randint(58, 68)
                    player.slice = random.randint(50, 62)
                    player.volley = random.randint(45, 58)
        
                    player.clutch = random.randint(50, 62)
                    player.endurance = random.randint(58, 68)
                case "Hard":
                    player.serve = random.randint(52, 62)
                    player.forehand = random.randint(52, 62)
                    player.backhand = random.randint(52, 62)
                    player.slice = random.randint(50, 60)
                    player.volley = random.randint(50, 60)
        
                    player.clutch = random.randint(54, 64)
                    player.endurance = random.randint(54, 64)
        
    player.update_rating()
    
    return player

def simulate_tournament(tournament, participants):
    
    # Seed players based on points
    player_remaining = sorted(participants, key=lambda p: p.points)
    
    match tournament.pts:
        case 2000:  # Grand Slam
            points_per_round = POINTS_PER_ROUND_GS
        case 1000:  # Masters 1000
            points_per_round = POINTS_PER_ROUND_1000
        case 500:   # ATP 500
            points_per_round = POINTS_PER_ROUND_500
        case 250:   # ATP 250
            points_per_round = POINTS_PER_ROUND_250
        case 1500:  # ATP Finals
            points_per_round = ATP_FINALS_POINTS_PER_ROUND
     
    round = 0
    
    # Simulate Rounds
    while(len(player_remaining) > 2):
        
        next_round = []
        
        for i in range(0, int(len(player_remaining) / 2)):
            player1 = player_remaining[i]
            player2 = player_remaining[len(player_remaining) - 1 - i]
            
            winner, loser = simulate_match(tournament, player1, player2)
            
            next_round.append(winner)
            loser.point_history[tournament.week] = points_per_round[round]
        
        player_remaining = next_round
        
        round += 1
        
    # Final    
    player1 = player_remaining[0]
    player2 = player_remaining[1]
        
    champ, runner_up = simulate_match(tournament, player1, player2, final=True)
    
    # Trophies
    champ.trophies.append(f"{year} {tournament.name} Champion")
    runner_up.trophies.append(f"{year} {tournament.name} Finalist")
    
    # Points    
    champ.point_history[tournament.week] = points_per_round[round + 1]
    runner_up.point_history[tournament.week] = points_per_round[round]


def simulate_match(tournament, p1, p2, final=False):
    if tournament.slam: 
        best_of = 5
    else: 
        best_of = 3
    
    surface = tournament.surface
    country = tournament.country
    
    p1_games_won = 0
    p2_games_won = 0
    
    p1_sets_won = 0
    p2_sets_won = 0
    
    # Final Score
    p1_scores = []
    p2_scores = []
    
    # Calculate base probabilities (doesn't change during match)
    # P1 serving
    p1_server_rating = (
        p1.serve + 
        (p1.forehand + p1.backhand + p1.slice) / 2 + 
        p1.volley / 4
    )
    p2_returner_rating = (
        (p2.forehand + p2.backhand + p2.slice) / 2 + 
        p2.volley / 4
    )
    total = p1_server_rating + p2_returner_rating
    p1_serve_base = (p1_server_rating / total) * 100 + 15
    
    # P1 match bonuses
    if p1.country == country:
        p1_serve_base += 2
    if p1.type == surface:
        p1_serve_base += 3
    if p2.type == surface:
        p1_serve_base -= 3
    
    # P2 serving
    p2_server_rating = (
        p2.serve + 
        (p2.forehand + p2.backhand + p2.slice) / 2 + 
        p2.volley / 4
    )
    p1_returner_rating = (
        (p1.forehand + p1.backhand + p1.slice) / 2 + 
        p1.volley / 4
    )
    total = p2_server_rating + p1_returner_rating
    p2_serve_base = (p2_server_rating / total) * 100 + 15
    
    # P2 match bonuses
    if p2.country == country:
        p2_serve_base += 2
    if p2.type == surface:
        p2_serve_base += 3
    if p1.type == surface:
        p2_serve_base -= 3
    
    # Determine first server
    coin_flip = random.randint(0, 1)
    if coin_flip == 0: 
        server = p1
        returner = p2
    else: 
        server = p2
        returner = p1
    
    # Match loop
    while p1_sets_won < (best_of / 2 + 0.5) and p2_sets_won < (best_of / 2 + 0.5):
        
        # Set loop
        while (p1_games_won < 6 and p2_games_won < 6) or (abs(p1_games_won - p2_games_won) < 2):
            
            # Tiebreak at 6-6
            if p1_games_won == 6 and p2_games_won == 6:
                # Tiebreak - use server vs server base
                if server == p1:
                    tb_base = p1_serve_base
                else:
                    tb_base = p2_serve_base
                
                # Clutch bonus (higher in tiebreak)
                clutch_diff = server.clutch - returner.clutch
                tb_adjustments = clutch_diff * 0.5
                
                tb_prob = tb_base + tb_adjustments
                tb_prob = max(30, min(95, tb_prob))
                
                if random.randint(1, 100) <= tb_prob:
                    # Server won tiebreak
                    if server == p1:
                        p1_games_won = 7
                    else:
                        p2_games_won = 7
                else:
                    # Returner won tiebreak
                    if server == p1:
                        p2_games_won = 7
                    else:
                        p1_games_won = 7
                
                break  # Exit game loop, tiebreak ends set
            
            # Regular game simulation
            # Get base probability
            if server == p1:
                base_prob = p1_serve_base
            else:
                base_prob = p2_serve_base
            
            adjustments = 0
            
            # Fatigue (based on completed sets)
            sets_completed = p1_sets_won + p2_sets_won
            p1_fatigue = ((100 - p1.endurance) / 10) * sets_completed
            p2_fatigue = ((100 - p2.endurance) / 10) * sets_completed
            
            if server == p1:
                adjustments -= p1_fatigue
                adjustments += p2_fatigue
            else:
                adjustments -= p2_fatigue
                adjustments += p1_fatigue
            
            # Clutch adjustments
            clutch_diff = server.clutch - returner.clutch
            
            # Close games (5-4 or later)
            if p1_games_won + p2_games_won >= 9:
                adjustments += clutch_diff * 0.2
            
            # Final set
            if p1_sets_won + p2_sets_won >= best_of - 1:
                adjustments += clutch_diff * 0.2
            
            # Calculate final probability
            final_prob = base_prob + adjustments
            final_prob = max(30, min(95, final_prob))
            
            # Simulate game
            if random.randint(1, 100) <= final_prob:
                # Server won
                if server == p1:
                    p1_games_won += 1
                else:
                    p2_games_won += 1
            else:
                # Returner won (break!)
                if server == p1:
                    p2_games_won += 1
                else:
                    p1_games_won += 1
            
            # Switch server (continues throughout match)
            if server == p1:
                server = p2
                returner = p1
            else:
                server = p1
                returner = p2
        
        # Set complete - determine winner
        if p1_games_won > p2_games_won:
            p1_sets_won += 1
        else:
            p2_sets_won += 1
        
        # Record and reset games
        p1_scores.append(p1_games_won)
        p2_scores.append(p2_games_won)
        
        p1_games_won = 0
        p2_games_won = 0
    
    # Match complete - determine winner
    if p1_sets_won > p2_sets_won:
        winner = p1
        loser = p2
    else:
        winner = p2
        loser = p1
    
    # Display results if MC involved or final
    if p1.main_character == True or p2.main_character == True or final == True:
        if winner == p1:
            print(f"{tournament.name} Final: {p1.rank} {p1.name} d. {p2.rank} {p2.name}")
            print(*p1_scores, sep=" | ")
            print(*p2_scores, sep=" | ")
        else:
            print(f"{tournament.name}: {p2.rank} {p2.name} d. {p1.rank} {p1.name}")
            print(*p2_scores, sep=" | ")
            print(*p1_scores, sep=" | ")
        print("="*30)
    
    # Energy deduction for MC
    if p1.main_character == True or p2.main_character == True:
        input("Press Enter to continue...")
        
        total_sets = p1_sets_won + p2_sets_won
        energy_deduction = total_sets * ENERGY_PER_SET

        if p1.main_character == True: 
            p1.energy -= energy_deduction
        if p2.main_character == True: 
            p2.energy -= energy_deduction
    
    return winner, loser


def update_rankings(players):
    
    # Update point totals
    for p in players:
        p.update_points()
    
    # Sort by points, then rating
    sorted_players = sorted(players, key=lambda p: (-p.points, -p.rating))
    
    # Assign ranks
    for i, p in enumerate(sorted_players, start=1):
        p.rank = i
    
    return sorted_players

def print_rankings(players, num_players=15):
    
    players = update_rankings(players)
    
    # Top 15
    players = players[0:num_players]
    
    n=1
    for p in players:
        print(f"{n}. {p.name} ({p.country}) -- {p.points}, {p.rating} rating") 
        n += 1
        
def get_tournaments_for_week(week, all_tournaments):
    
    week_tournaments = [t for t in all_tournaments if t.week == week]
    week_tournaments = sorted(week_tournaments, key=lambda obj: obj.pts)
    
    return week_tournaments


def sim_week_tournaments(week_tournaments, players, mc_tournament=None, main_character=None):
    
    current_players = update_rankings(players)
    
    # Remove MC from pool and add to their tournament
    if mc_tournament:
        current_players.remove(main_character)
        mc_tournament_index = week_tournaments.index(mc_tournament)
    
    # Aligns with week_tournaments
    week_tournaments_participants = [[] for _ in week_tournaments]
    
    # Add MC to their chosen tournament
    if mc_tournament:
        week_tournaments_participants[mc_tournament_index].append(main_character)
    
    # Slam or Masters (1000+ points)
    if week_tournaments[0].pts >= 1000:
        # Top players fill the big tournament
        for p in current_players[0:week_tournaments[0].participants]:
            week_tournaments_participants[0].append(p)
    
    # ATP 500 or 250
    else: 
        for p in current_players:
            # Probability to enter based on rank (LESS likely as rank improves)      
            if p.rank <= 20:
                probability = 35
            elif p.rank <= 50:
                probability = 75
            elif p.rank <= 100:
                probability = 80
            else:
                probability = 99
            
            if random.randint(1, 100) <= probability:
                # Find tournaments with available spots
                available_tournaments = []
                for i in range(len(week_tournaments)):
                    if len(week_tournaments_participants[i]) < week_tournaments[i].participants:
                        available_tournaments.append(i)
                
                # If any tournament has space, assign randomly
                if available_tournaments:
                    tournament_index = random.choice(available_tournaments)
                    week_tournaments_participants[tournament_index].append(p)
                        
    # Simulate Tournaments
    for i in range(len(week_tournaments)):
        simulate_tournament(week_tournaments[i], week_tournaments_participants[i])
        
def year_end_results(players):
    players = update_rankings(players)
    
    for p in players:
        if p.main_character == True:
            
            print(f"Your final rank was {p.rank} with {p.points} points\n")
            continue
    
    # Year-end #1
    print(f"{players[0].name} finished the year as World No. 1\n")
    players[0].trophies.append(f"{year} Year-End World No. 1")
    
    print_rankings(players, 10)
    
    # Slam & Finals Winners
    for p in players:
        if p.point_history[AO_WEEK] >= 2000:
            print(f"{p.name} won the Australian Open")
            break
    for p in players:
        if p.point_history[FO_WEEK] >= 2000:
            print(f"{p.name} won the French Open")
            break
    for p in players:
        if p.point_history[WIM_WEEK] >= 2000:
            print(f"{p.name} won Wimbledon")
            break
    for p in players:
        if p.point_history[USO_WEEK] >= 2000:
            print(f"{p.name} won the US Open")
            break
    for p in players:
        if p.point_history[FINALS_WEEK] >= 1500:
            print(f"\n{p.name} won the ATP Finals")
            break
    
    print("="*30)

def year_end_changes(players):    

    players = update_rankings(players)

    retired_players = 0
    
    for p in players:            
        change_in_overall = 0
        retirement_chance = 0
        
        # Retirement Chance
        # Age factor
        if p.age >= 30:
            retirement_chance += (p.age - 29) * 10
        
        # Rank factor
        if p.rank > 225:
            retirement_chance += (p.rank - 224) 
        
        if retirement_chance > random.randint(1, 100):
            # Retire Player
            players.remove(p)    
            retired_players += 1
            continue
        
        # Change in overall rating
        p.age += 1
        # Age Effects
        if p.age >= 34:
            change_in_overall += random.randint(-7, -2)
            p.endurance += random.randint(-5, 0)
        elif p.age >= 30:
            change_in_overall += random.randint(-2, 0)
            p.endurance += random.randint(-3, 0)
        elif p.age >= 26:
            change_in_overall += random.randint(-3, 2)
        elif p.age >= 22:
            change_in_overall += random.randint(-1, 3)
        else:
            change_in_overall += random.randint(1, 4)
            
        # Rank Effects
        if p.rank <= 25:
            change_in_overall += random.randint(0, 1)
        elif p.rank <= 100:
            change_in_overall += random.randint(-1, 1)
            
        # Deep Run Effects 
        for performance in p.point_history:
            if performance >= 600: # SF or better at GS, F or better at Masters
                change_in_overall += random.randint(0, 1)
        
        # Apply change
        # Max 100 rating
        if change_in_overall + p.rating >= 100:
            change_in_overall = 100 - p.rating
        
        stat_change = change_in_overall / 6
        
        p.serve += random.uniform(0, stat_change * 2)
        p.forehand += random.uniform(0, stat_change * 2)
        p.backhand += random.uniform(0, stat_change * 2)
        p.slice += random.uniform(0, stat_change * 2)
        p.volley += random.uniform(0, stat_change * 2)
        # Clutch Unchanged
        p.endurance += random.uniform(0, stat_change * 2)
        
        p.update_rating()
        

    # Generate new young players to replace retirees
    for i in range(retired_players):
        new_player = generate_random_player(age = random.randint(18, 22))
        players.append(new_player)
        
    return players


# New Game ----------------------------------

# Generate random players
players = []

for i in range(250):
    cpu = generate_random_player()
    players.append(cpu)

# Load tournaments from JSON
with open('tournaments.json', 'r') as f:
    tournament_data = json.load(f)

all_tournaments = []
for t in tournament_data:
    tourney = Tournament(t['name'], t['pts'], t['participants'], 
                         t['slam'], t['surface'], t['week'], t['country'])
    all_tournaments.append(tourney)

# Sim Past Years
for year in range(2020, 2026):
    for week in range(1, 53):
        week_tournaments = get_tournaments_for_week(week, all_tournaments)
        
        if len(week_tournaments) > 0:
            sim_week_tournaments(week_tournaments, players)
            
        players = update_rankings(players)
    
    # Summary
    print(f"{year} Season Summary")
    year_end_results(players)
    
    # Year end adjustments
    players = year_end_changes(players)
    


# Create Main Player
name = ""
country = ""
type = ""
type_select = 0
name = input("Name (first and last): ")
country = input("Country (3-letter abbreviation, ex. USA): ")

while (type_select <= 0 or type_select > 3):

    print(f"1. Grass -  Serve, volley, slice focused")
    print(f"2. Clay  -  Strong groundstrokes and endurance")
    print(f"3. Hard  -  Balanced all-around, strong mentality")
    
    
    print("="*30)
    type_select = int(input("Select a type (1-3): "))

match (type_select):
    case 1:
        type = "Grass"
    case 2:
        type = "Clay"
    case 3:
        type = "Hard"

mc = Player(name, country, type)

mc.main_character = True

print("New Career Created!")
mc.print_stats()

# Tutorial


# Main
# year loop
week = 1
year = 2026
loop = True
while (loop):
    while (week < 53):
        
        players = update_rankings(players)
        
        week_tournaments = get_tournaments_for_week(week, all_tournaments)
        
        if len(week_tournaments) == 0:
            week += 1
            continue
        
        print(f"WEEK {week} of the {year} season")
        
        print_rankings(players)
        
        # print(f"Current Rank: {mc.rank}")
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
                
                # Energy Check
                required_energy = int(math.log2(selected_tournament.participants)) * ENERGY_PER_SET * 3  # Estimate for 3-set matches
                if mc.energy < required_energy:
                    print("Not enough energy")
                    selection = 0
                    
                # Eligibility Check
                if selected_tournament.pts >= 1000:  # Slam or Masters
                    if mc.rank > selected_tournament.participants:
                        print("Not eligible for this tournament")
                        selection = 0
                
                    
            # Enter Tournament


        # Train/Rest        
        elif selection == 2:
            # Options
            n = 1
            for opt in TRAIN_OPTIONS:
                print(f"{n}. {opt}")
                n += 1
            

            selection = 0
            while (selection <= 0 or selection > len(TRAIN_OPTIONS)):
                selection = int(input(f"Select an option: "))
            
            selected_option = TRAIN_OPTIONS[selection - 1]
            
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
                
        # Sim Tournaments
        sim_week_tournaments(week_tournaments, players, mc_tournament=selected_tournament, main_character=mc)
        
        week += 1


    # End of Season
    # Summary
    print(f"{year} Season Summary")
    year_end_results(players)
    
    # Year end adjustments (retirements, rating changes, new players)
    players = year_end_changes(players)
    
    # Happy New Year
    week = 1
    year += 1

