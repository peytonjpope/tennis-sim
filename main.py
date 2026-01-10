from player import Player
import random
import math
import json
from tournament import Tournament
import names
from datetime import date

# CONSTANTS
COUNTRIES = ["USA", "ESP", "SRB", "FRA", "AUS",
             "ITA", "GER", "GBR", "RUS", "ARG",
             "SUI", "JPN", "CAN", "CRO", "SWE", 
             "AUT", "NED", "BRA", "NOR", "GRE",
             "POL", "CZE", "DEN", "CHN", "MEX"]

ENERGY_PER_SET = 2

TYPES = ['Grass', 'Clay', 'Hard']

TRAIN_OPTIONS = ['Rest', 'Serve', 'Forehand', 'Backhand', 'Slice', 'Volley', 'Clutch', 'Endurance']

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

    full_name = names.get_full_name(gender='male')
    first, last = full_name.split()
    name = f"{first[0]}. {last}"
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
                    player.serve = random.randint(95, 99)      
                    player.forehand = random.randint(78, 90)   
                    player.backhand = random.randint(78, 90)  
                    player.slice = random.randint(85, 96)      
                    player.volley = random.randint(95, 99)    
                    
                    player.clutch = random.randint(88, 96)
                    player.endurance = random.randint(78, 90) 

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
                    player.serve = random.randint(85, 92)      
                    player.forehand = random.randint(70, 81)   
                    player.backhand = random.randint(70, 81)   
                    player.slice = random.randint(78, 88)     
                    player.volley = random.randint(85, 92)     
                    
                    player.clutch = random.randint(78, 88)
                    player.endurance = random.randint(70, 81)  
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

def simulate_tournament(tournament, participants, mc_matches=None, yr="20XX"):
    
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
            
            winner, loser, match_result = simulate_match(tournament, player1, player2, round=round)
            
            # Store MC match if applicable
            if mc_matches is not None and (player1.main_character or player2.main_character):
                mc_matches.append(match_result)
            
            next_round.append(winner)
            loser.point_history[tournament.week - 1] = points_per_round[round]
        
        player_remaining = next_round
        
        round += 1
        
    # Final    
    player1 = player_remaining[0]
    player2 = player_remaining[1]
        
    champ, runner_up, match_result = simulate_match(tournament, player1, player2, final=True)
    
    # Store MC match if applicable
    if mc_matches is not None and (player1.main_character or player2.main_character):
        mc_matches.append(match_result)
    
    # Trophies
    champ.trophies.append(f"{yr} {tournament.name} Champion")
    runner_up.trophies.append(f"{yr} {tournament.name} Finalist")
    
    # Points    
    champ.point_history[tournament.week - 1] = points_per_round[round + 1]
    runner_up.point_history[tournament.week - 1] = points_per_round[round]
    
    return champ


def simulate_match(tournament, p1, p2, round=None, final=False):
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
            final_prob = max(20, min(95, final_prob))
            
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
    
    # Energy deduction for MC
    if p1.main_character == True or p2.main_character == True:
        total_sets = p1_sets_won + p2_sets_won
        energy_deduction = total_sets * ENERGY_PER_SET

        if p1.main_character == True: 
            p1.energy -= energy_deduction
        if p2.main_character == True: 
            p2.energy -= energy_deduction
    
    # Create match result dict
    match_result = {
        'round': round,
        'final': final,
        'p1': p1,
        'p2': p2,
        'winner': winner,
        'loser': loser,
        'p1_scores': p1_scores,
        'p2_scores': p2_scores
    }
    
    return winner, loser, match_result


def update_rankings(players):
    
    # Update point totals
    for p in players:
        p.update_points()
    
    # Sort by points, then rating
    sorted_players = sorted(players, key=lambda p: (-p.points, -p.rating))
    
    # Assign ranks
    for i, p in enumerate(sorted_players, start=1):
        p.rank = i
        if i < p.career_high_rank:
            p.career_high_rank = i
        p.rank_history.append(i)
    
    return sorted_players


def get_tournaments_for_week(week, all_tournaments):
    
    week_tournaments = [t for t in all_tournaments if t.week == week]
    week_tournaments = sorted(week_tournaments, key=lambda obj: obj.pts)
    
    return week_tournaments


def sim_week_tournaments(week_tournaments, players, mc_tournament_selection=None, main_character=None, year="20XX"):
    
    current_players = update_rankings(players)

    # Find and remove MC from pool
    if main_character is not None:
        current_players.remove(main_character)
    
    # Aligns with week_tournaments
    week_tournaments_participants = [[] for _ in week_tournaments]
    
    # Add MC to their chosen tournament
    mc_matches = [] if main_character is not None else None
    
    if mc_tournament_selection is not None:
        week_tournaments_participants[mc_tournament_selection].append(main_character)
    
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
    tournament_results = []
    for i in range(len(week_tournaments)):
        if mc_tournament_selection == i and main_character is not None:
            champion = simulate_tournament(week_tournaments[i], week_tournaments_participants[i], mc_matches, yr=year)
        else:
            champion = simulate_tournament(week_tournaments[i], week_tournaments_participants[i], yr=year)
        
        tournament_results.append({
            'tournament': week_tournaments[i],
            'champion': champion
        })
    
    return tournament_results, mc_matches


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