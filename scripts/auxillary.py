'''
main random meal choice function and its tiny helpers
this is called auxiallary as it is supposed to support the main main.py file
'''
from enum import Enum
import pandas as pd
from pathlib import Path

try:
    import scripts.iodata as iod
    from classes.classes import KosherType
except:
    import iodata as iod
    import classes.classes
    #from ../classes/classes.py import KosherType
    #class_path = Path(__file__).parent / "../classes/"
    #print(class_path)
    #import class_path.classes

class Kosher(str, Enum):
    '''
    DEPRACTED
    still here to make sure nothing depends on this, this will be removed later
    '''
    parve= "parve"
    fleisch = "fleisch"
    milchik = "milchik"

def choose_random(meals, rank: bool = False, times: bool = False, last_made: bool = False, TA=None, k=1):
    '''
    makes a random choice of a meal from a meal DB

    IMPORTANT: this returns too many arguments, either needs to be truncated or used by other functions 
    '''
    use_rank = None
    
    meals_copy = meals.copy()
    
    # filter meals prepared in the past 4 days
    # NOT IMPLEMENTED YET #

    # use a weighted choice, by rank
    if rank == True:
        use_rank = choice["Rank"]
    
    # include or choose only take-away, default is to random from everythin
    if TA == False:
        meals_copy = meals_copy[meals_copy["TA"] == 0]
    elif TA == True:
        meals = meals_copy[meals_copy["TA"] == 1]
    
    is_late = is_too_late_to_cook()
    translate_time = {"short":0, "medium":1, "long": 2}
    if is_late == True:
        meals_copy.replace({"Prep_Time":translate_time,"Cook_Time":translate_time},inplace=True)
        meals_copy = meals_copy[meals_copy["Prep_Time"] < 2]
        meals_copy = meals_copy[meals_copy["Cook_Time"] < 2]

    choice = meals_copy.sample(n=k, weights=use_rank)

    print(choice["Name"].iloc[0])
    
    suggestion = meals.iloc[choice.index[0]].iloc[11]
    if isinstance(suggestion,str):
        print(f'Recipe suggestion: {suggestion}')
    elif isinstance(suggestion,float):
        print("No recipe suggestion exists in the database.")

    return meals, choice["Name"].iloc[0], choice.index[0]

def make_this_meal(meals, choice):
    '''
    Asks user if he will make the meal, if yes meal is logged.
    doesn't return anythin, just changes the state of the meals DB
    '''
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            meals.loc[choice,"times_made"] += 1
            meals.loc[choice,"Timestamp"] = pd.Timestamp.now().date()
            print("meal logged.")
            return True
        elif make_it.lower() == "n":
            print("meal not logged.")
            return False
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")

def is_too_late_to_cook(cutoff: int = 20):
    '''
    Checks actual time and returns if choose_random should skip ideas with long preparation time.
        After 20:00 only short and medium durations will be considered.
    1. Needs cooking duration feature implemnted.
    2. Option: ask user how long does he plan to prepare the meal
    
    IMPORTANT 1: should be relevant to Cook_Time and Prep_Time, so if any of them is above medium then meal shouldn't be suggested.
    IMPORTANT 2: only takes into account that the time is less than 20:00, if you start cooking after midnight this function will fail to work properly.
    '''
    hour = pd.Timestamp.now().hour
    if hour < cutoff:
        return False
    elif hour < 5: # Don't cook in the middle of the night
        return True
    else:
        return True

def reboot_time_timestamps(data="meal_list.csv",logfile="meal.log"):
    '''
    Resets all times made to 0 and removes all time stamps.
    This is currently designed only testing and developing.
    '''
    while True:
        just_checking = input("Are you sure you want to reset *ALL* timestamps and all times_made? (y/n)")
        if just_checking.lower() == "n":
            print("data was not reset")
            return 0
        elif just_checking.lower() == "y":
            data["Timestamp"] = "NaN"
            data["times_made"] = 0
            iod.save_data(data)
            with open(logfile, "w") as f: pass # empties the meal.log file
            print("Data was reset and saved")
            return 0

def filter_kosher(meal_list, kosher: KosherType):
    '''
    Takes loaded meal_list DF and returns the filtered meals according to specified kosher

    meal_list   ::: pandas DataFrame with meals
    kosher      ::: kosher type [parve|milchik|fleisch]
    '''
    return meal_list

if __name__ == "__main__":
    FILENAME = "../data/meal_list.csv"
    PATH = Path(__file__).parent / FILENAME
    data = pd.read_csv(PATH, index_col=0)
    #reboot_time_timestamps(data)

