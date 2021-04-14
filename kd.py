from xlsx2csv import Xlsx2csv
from pprint import pprint
import random

# CONSTANTS 
KD_COUNT = "KD_Count"
MEAL_SIGN_UPS = "Meal-Sign-Ups-Spring-2021"
KDS = "KDs" 

NEW_MEMBERS = ["AANJAN", "ANKITH", "TONY", "PRAX", "LUKE", "MATEO", "SANDRO"]

# meal time mapped to people
meal_time_to_people = {
    "MONDAY_LUNCH": [],
    "MONDAY_DINNER": [],
    "TUESDAY_LUNCH": [],
    "TUESDAY_DINNER": [],
    "WEDNESDAY_LUNCH": [],
    "WEDNESDAY_DINNER": [],
    "THURSDAY_LUNCH": [],
    "THURSDAY_DINNER": [],
    "FRIDAY_LUNCH": [],
    "SUNDAY_DINNER": []
}

kdtime_to_victim = {
    "MONDAY_LUNCH": {11: "EMPTY", 12: "EMPTY"},
    "MONDAY_DINNER": {5: "EMPTY", 6: "EMPTY"},
    "TUESDAY_LUNCH": {11: "EMPTY", 12: "EMPTY"},
    "TUESDAY_DINNER": {5: "EMPTY", 6: "EMPTY"},
    "WEDNESDAY_LUNCH": {11: "EMPTY", 12: "EMPTY"},
    "WEDNESDAY_DINNER": {5: "EMPTY", 6: "EMPTY"},
    "THURSDAY_LUNCH": {11: "EMPTY", 12: "EMPTY"},
    "THURSDAY_DINNER": {5: "EMPTY", 6: "EMPTY"},
    "FRIDAY_LUNCH": {11: "EMPTY", 12: "EMPTY"},
    "SUNDAY_DINNER": {6: "EMPTY"}
}

meals_list = [
    "MONDAY_LUNCH",
    "MONDAY_DINNER",
    "TUESDAY_LUNCH",
    "TUESDAY_DINNER",
    "WEDNESDAY_LUNCH",
    "WEDNESDAY_DINNER",
    "THURSDAY_LUNCH",
    "THURSDAY_DINNER",
    "FRIDAY_LUNCH",
    "SUNDAY_DINNER"
]


# maps kd count to a list of all the people with that number of kds done
kd_count_to_name = {}
# list of people who can do KD's - no pledges and no grad bros 
list_of_names = []

# Need to do pip install xlxsx2csv or pip3 install xlxsx2csv
# NO need to pass in extension for file name here 
def convert_to_csv(fileName):
    Xlsx2csv(fileName +".xlsx", outputencoding="utf-8").convert(fileName + ".csv")
    print("Succesfully exported {}.xlsx to {}.csv .....".format(fileName, fileName))

convert_to_csv(KD_COUNT)
convert_to_csv(MEAL_SIGN_UPS)
convert_to_csv(KDS)


# This will only add to meal_time_to_people if they are eligible to do a kd 
def add_to_meal_time_to_people(name_to_add, index):
    if (name_to_add in list_of_names):
        if (index == 2 and name_to_add not in meal_time_to_people["MONDAY_LUNCH"]):
            meal_time_to_people["MONDAY_LUNCH"].append(name_to_add)
        elif (index == 3 and name_to_add not in meal_time_to_people["MONDAY_DINNER"]):
            meal_time_to_people["MONDAY_DINNER"].append(name_to_add)
        elif (index == 4 and name_to_add not in meal_time_to_people["TUESDAY_LUNCH"]):
            meal_time_to_people["TUESDAY_LUNCH"].append(name_to_add)
        elif (index == 5 and name_to_add not in meal_time_to_people["TUESDAY_DINNER"]):
            meal_time_to_people["TUESDAY_DINNER"].append(name_to_add)
        elif (index == 6 and name_to_add not in meal_time_to_people["WEDNESDAY_LUNCH"]):
            meal_time_to_people["WEDNESDAY_LUNCH"].append(name_to_add)
        elif (index == 7 and name_to_add not in meal_time_to_people["WEDNESDAY_DINNER"]):
            meal_time_to_people["WEDNESDAY_DINNER"].append(name_to_add)
        elif (index == 8 and name_to_add not in meal_time_to_people["THURSDAY_LUNCH"]):
            meal_time_to_people["THURSDAY_LUNCH"].append(name_to_add)
        elif (index == 9 and name_to_add not in meal_time_to_people["THURSDAY_DINNER"]):
            meal_time_to_people["THURSDAY_DINNER"].append(name_to_add)
        elif (index == 10 and name_to_add not in meal_time_to_people["FRIDAY_LUNCH"]):
            meal_time_to_people["FRIDAY_LUNCH"].append(name_to_add)
        elif (index == 11 and name_to_add not in meal_time_to_people["SUNDAY_DINNER"]):
            meal_time_to_people["SUNDAY_DINNER"].append(name_to_add)

def map_names_to_kdcount():
    file_kd_count = open("KD_Count.csv", "r")
    kd_count_header = file_kd_count.readline()
    
    # index 0: name 
    # index 1: num of Kds
    # index 2: dont give kd
    kd_count_info = file_kd_count.readlines()
    
    # logic for populating kd_count_info
    for line in kd_count_info:
        line = line.split(",")
        if (line[0] != '' and line[0] != ''):
            giveKD = (line[2] == '') # this means that if you add anythinng to the dont give kd line, it wont give them a kd
            if (giveKD):
                name = line[0].strip().upper()
                list_of_names.append(name)
                kdCount = int(line[1].strip())

                if (kdCount in kd_count_to_name.keys()):
                    kd_count_to_name[kdCount].append(name)
                else:
                    kd_count_to_name[kdCount] = [name]


def assign_people_to_meal_time():
    file_meal_sign_ups = open("Meal-Sign-Ups-Spring-2021.csv", "r")
    meal_sign_ups_header = file_meal_sign_ups.readline()
    meal_sign_ups_info = file_meal_sign_ups.readlines()

    for line in meal_sign_ups_info:
        line = line.split(",")
        if (line[0] != '' and line[1] != ''):
            name = line[1].upper().strip()

            latePlateCounterForPerson = 0
            noFill = 0

            for index in range(2,12):
                mealTime = line[index].strip()
                
                if (mealTime == "11" or mealTime == "12" or mealTime == "5" or mealTime == "6") and mealTime != '':
                    add_to_meal_time_to_people(name, index)
                elif (line[index] == "Late"):
                    latePlateCounterForPerson += 1
                else:
                    noFill +=1


            # if they didnt fill out a meal time or get a late plate more than 5 times, assigns them to every possibility
            if (noFill > 3 or latePlateCounterForPerson > 7):
                for index in range(2,12):
                    # handles grad bro logic in add_to_meal_time_to_people
                    add_to_meal_time_to_people(name, index)


def kd_selector():

    numPeople = 0
    victims = []
    minimumNumOfKD = min(k for k, v in kd_count_to_name.items())
    print(minimumNumOfKD)
    
    # victim selection
    while numPeople < 19:
        toAdd = kd_count_to_name[minimumNumOfKD]
        for member in toAdd:
            if (numPeople < 19): 
                victims.append(member)
                numPeople += 1
            else:
                break

        del kd_count_to_name[minimumNumOfKD] # deleting min key 
        minimumNumOfKD = min(k for k, v in kd_count_to_name.items())

    print(victims)
    
    # pick random indices here to replace w pledges 
    # of kds to be taken care by new members
    # EDIT LOGIC HERE TO ADJUST NEW MEMBER FREQUENCIES 
    new_member_kd_per_week = 7 

    for num in range(new_member_kd_per_week + 1):
        lucky_index = random.randrange(0, 19,1)
        unlucky_new_mem_index = random.randrange(0, len(NEW_MEMBERS),1)
        victims[lucky_index] = NEW_MEMBERS[unlucky_new_mem_index]

    victims_wout_placement = []

    print(victims)

    for victim in victims:
        meal_found = False
        for meal in meal_time_to_people:
            
            if victim in meal_time_to_people[meal]:
                for whichTime in kdtime_to_victim[meal]:
                    if kdtime_to_victim[meal][whichTime] == "EMPTY" and meal_found == False:
                        kdtime_to_victim[meal][whichTime] = victim
                        meal_found = True
                
            if meal_found == False:
                continue # keep looking for meals 
            else:
                break # look at next victim
        
        if meal_found == False:
            victims_wout_placement.append(victim)
    
    numLeft = len(victims_wout_placement)
    victimIndexer = 0

    if numLeft != 0:
        while (numLeft != 0):

            for meal in kdtime_to_victim: 
                for time in kdtime_to_victim[meal]:
                    if numLeft == 0:
                        return

                    if kdtime_to_victim[meal][time] == "EMPTY":
                        kdtime_to_victim[meal][time] = victims_wout_placement[victimIndexer]
                        victimIndexer += 1
                        numLeft -= 1
         

def write_txt(): 
    outputFile = open("kd_for_the_week.txt","w")


    for meal in meals_list:
        for time in kdtime_to_victim[meal]:
            outputFile.write("{}, {}, : {}\n".format(meal, time, kdtime_to_victim[meal][time]))

    outputFile.close()


