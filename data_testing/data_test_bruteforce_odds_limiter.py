from get_data import dataset_to_dictionary, fetch_data, single_match
from get_values import football_values
import time
start_time = time.time()
"""
print(relevant_data)
print(match_list)
print(row)
"""


def HTG_compare(match):
    hometeam = int(match_list[match]['HTHG'])
    awayteam = int(match_list[match]['HTAG'])

    if hometeam > awayteam:
        if (hometeam - awayteam) == 1:
            return (football_values[0]), "H"
            
        elif (hometeam - awayteam) == 2:
            return (football_values[0] * 1.2), "H"
            
        elif (hometeam - awayteam) == 3:
            return (football_values[0] * 1.5), "H"
            
        else:
            return (football_values[0] * 2), "H"       
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) == 1:
            return -(football_values[0]), "A"
            
        elif (awayteam - hometeam) == 2:
            return -(football_values[0] * 1.2), "A"
            
        elif (awayteam - hometeam) == 3:
            return -(football_values[0] * 1.5), "A"
            
        else:
            return -(football_values[0] * 2), "A"

    elif hometeam == awayteam:
        return 0, "D"
    
    else:
        print("Error")

def S_compare(match):
    hometeam = int(match_list[match]['HS'])
    awayteam =int(match_list[match]['AS'])

    if hometeam > awayteam:
        return football_values[1], "H"
    
    elif hometeam == awayteam:
        return 0, "D"
    
    else:
        return -(football_values[1]), "A"

def ST_compare(match):
    hometeam = int(match_list[match]['HST'])
    awayteam = int(match_list[match]['AST'])

    if hometeam > awayteam:
        return football_values[2], "H"
    
    elif hometeam == awayteam:
        return 0, "D"
    
    else:
        return -(football_values[2]), "A"

def Y_compare(match):
    hometeam = int(match_list[match]['HY'])
    awayteam = int(match_list[match]['AY'])

    if hometeam > awayteam:
        return -football_values[3], "A"
    
    elif hometeam == awayteam:
        return 0, "D"
    
    else:
        return football_values[3], "H"


def R_compare(match):
    hometeam = int(match_list[match]['HR'])
    awayteam = int(match_list[match]['AR'])

    if hometeam > awayteam:
        return -(football_values[4]), "A"
    
    elif hometeam == awayteam:
        return 0, "D"
    
    else:
        return football_values[4], "H"


def winning_team(team_score):
    if team_score > 0:
        return "H"
    elif team_score < 0:
        return "A"
    else:
        return "D"

def check_predictions(match, results):
    if results == match_list[match]['FTR']:
        return 1
    else:
        return 0
"""
def betting(match, results, points):
    money_bet = 100
    if points > 1.1 or points < -1.1:
        
        if results == match_list[match]['FTR']:
            
            if results == "H":
                return money_bet * match_list[match]['B365H'] - 100, 1, 1
            
            elif results == 'D':
                return money_bet * match_list[match]['B365D'] - 100, 1, 1
            
            else:
                return money_bet * match_list[match]['B365A'] - 100, 1, 1
        else:
            return -100, 1, 0
    else: 
        return 0, 0, 0
"""
def betting(match, results, points, val):
    money_bet = 100
    if results == "H":
        if match_list[match]['B365H'] > (val/10):
            if results == match_list[match]['FTR']:
                return money_bet * match_list[match]['B365H'] - 100, 1, 1
            else:
                return -100, 1, 0
        else:
            return 0, 0, 0
    
    elif results == 'D':
        if match_list[match]['B365D'] > (val/10):
            if results == match_list[match]['FTR']:
                return money_bet * match_list[match]['B365D'] - 100, 1, 1
            else:
                return -100, 1, 0
        else:
            return 0, 0, 0
    
    else:
        if match_list[match]['B365A'] > (val/10):
            if results == match_list[match]['FTR']:
                return money_bet * match_list[match]['B365A'] - 100, 1, 1
            else:
                return -100, 1, 0
        else:
            return 0, 0, 0


file_list = ["imported_data/E0_2005.csv", "imported_data/E0_2006.csv", "imported_data/E0_2007.csv", "imported_data/E0_2008.csv", "imported_data/E0_2009.csv", "imported_data/E0_2010.csv", "imported_data/E0_2011.csv", "imported_data/E0_2012.csv", "imported_data/E0_2013.csv", "imported_data/E0_2014.csv", "imported_data/football_data.csv"]

if __name__ == "__main__":
    for x in range(10, 50):   
        money_earned = 0
        predictions_correct = 0
        matches_bet = 0
        matches_bet_correct = 0
        for file in file_list:
            relevant_data = fetch_data(file) # Hämtar data

            match_list = dataset_to_dictionary(relevant_data) # Konverterar datan till dictionary
            # match_list[index för matchens rad][target-data]

            row = single_match(0, file)
            
            for y in match_list:
                results = HTG_compare(y)[0]
                function_return_id = HTG_compare(y)[1]
                
                results += ST_compare(y)[0]
                function_return_id += ST_compare(y)[1]
                
                results += S_compare(y)[0]
                function_return_id += S_compare(y)[1]
                
                results += Y_compare(y)[0]
                function_return_id += Y_compare(y)[1]
                
                results += R_compare(y)[0]
                function_return_id += R_compare(y)[1]
                
                match_predictions = winning_team(results)
                predictions_correct += check_predictions(y, match_predictions)
                money_earned += betting(y, match_predictions, results, x)[0]
                matches_bet += betting(y, match_predictions, results, x)[1]
                matches_bet_correct += betting(y, match_predictions, results, x)[2]

        print("--- Program predicted results in ", round(((predictions_correct / 4180) * 100)), "%", "of matches ---")
        print("--- Program betted correctly in ", round(((matches_bet_correct / matches_bet) * 100)), "%", "of matches ---")
        print("---", money_earned, " kr earned ---")
        print("---", (money_earned/matches_bet), " kr earned on average per match ---")
        print("--- Program bet on ", matches_bet, " matches ---")
        print("--- %s seconds ---" % (time.time() - start_time))
        print("--- Odds limiter value was:", x/10 , "---")



