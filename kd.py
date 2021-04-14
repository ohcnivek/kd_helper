from xlsx2csv import Xlsx2csv
from pprint import pprint
import random

# CONSTANTS: The values of KD_COUNT, MEAL_SIGN_UPS, NEW_KD_SHEET should only change when the excel sheet names change. 
KD_COUNT = "KD_Count"
MEAL_SIGN_UPS = "Meal-Sign-Ups-Spring-2021"
NEW_KD_SHEET = "KDs_for_the_week"
NEW_MEMBERS = ["AANJAN", "ANKITH", "TONY", "PRAX", "LUKE", "MATEO", "SANDRO"]
TOTAL_KDS_PER_WEEK = 19

# Kitchen Assistant should change these values as they see fit: 
DIDNT_FILL_OUT_FORM_MAX_COUNT = 3 # If they didnt fill out a time for this many meals, they will be marked as "available" to KD for every meal. Those who marked the times they are eating will get priority. 
NUMBER_OF_LATE_PLATES_PER_WEEK_MAX_COUNT = 7 # If they get a late plate this many number of times, they will be marked as "available" to KD for every meal. 
NEW_MEMBERS_COVER_THIS_AMOUNT_OF_KDS = 7 #Number of KDs you want covered by New Members. 

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

kd_count_to_name = {}
list_of_names = [] # NOTE: THIS LIST WILL NOT INCLUDE NEW MEMBERS & GRAD BROS. LOGIC FOR HANDLING NEW MEMBER'S IS IN KD_SELECTOR


def convert_to_csv(fileName):
    Xlsx2csv(fileName +".xlsx", outputencoding="utf-8").convert(fileName + ".csv")
    print("Succesfully exported {}.xlsx to {}.csv .....".format(fileName, fileName))

convert_to_csv(KD_COUNT)
convert_to_csv(MEAL_SIGN_UPS)


def add_to_meal_time_to_people(name_to_add, index):
    if (name_to_add in list_of_names): #VALIDATING THAT THEY ARE AVAILABLE TO DO A KD AKA NOT A GRADUATING BROTHER/NEW MEMBER
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
    file_kd_count = open(KD_COUNT + ".csv", "r")
    file_kd_count.readline()
    kd_count_info = file_kd_count.readlines()
    
    # POPULATING kd_count_info
    for line in kd_count_info:
        line = line.split(",")
        name = line[0]
        if (name != ''):
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
    file_meal_sign_ups = open( MEAL_SIGN_UPS + ".csv", "r")
    file_meal_sign_ups.readline()
    meal_sign_ups_info = file_meal_sign_ups.readlines()

    for line in meal_sign_ups_info:
        line = line.split(",")
        submission_time = line[0]
        name = line[1]
        if (submission_time!= '' and name != ''):
            name = line[1].upper().strip()
            latePlateCounterForPerson = 0
            noFill = 0

            for index in range(2,12): # 2-12 because these are the indexes that contain meal times/ info about attendance
                mealTime = line[index].strip()
                if (mealTime == "11" or mealTime == "12" or mealTime == "5" or mealTime == "6"):
                    add_to_meal_time_to_people(name, index)
                elif (line[index] == "Late"):
                    latePlateCounterForPerson += 1
                else:
                    noFill +=1


            if (noFill > DIDNT_FILL_OUT_FORM_MAX_COUNT or latePlateCounterForPerson > NUMBER_OF_LATE_PLATES_PER_WEEK_MAX_COUNT):
                for index in range(2,12):
                    add_to_meal_time_to_people(name, index)


def kd_selector():
    numPeople = 0
    victims = []
    minimumNumOfKD = min(k for k, v in kd_count_to_name.items())

    # victim selection
    while numPeople < TOTAL_KDS_PER_WEEK:
        toAdd = kd_count_to_name[minimumNumOfKD]
        for member in toAdd:
            if (numPeople < TOTAL_KDS_PER_WEEK): 
                victims.append(member)
                numPeople += 1
            else:
                break

        del kd_count_to_name[minimumNumOfKD] # deleting min key 
        minimumNumOfKD = min(k for k, v in kd_count_to_name.items())
    

    for num in range(NEW_MEMBERS_COVER_THIS_AMOUNT_OF_KDS + 1):
        lucky_brother_index = random.randrange(0, len(victims), 1)
        unlucky_new_mem_index = random.randrange(0, len(NEW_MEMBERS),1) #ENSURES THAT A NEW MEMBER ISNT CHOSEN TWICE
        victims[lucky_brother_index] = NEW_MEMBERS[unlucky_new_mem_index]
 


    victims_wout_placement = []

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
    outputFile = open(NEW_KD_SHEET + ".txt","w")
    for meal in meals_list:
        for time in kdtime_to_victim[meal]:
            outputFile.write("{}, {}, : {}\n".format(meal, time, kdtime_to_victim[meal][time]))

    outputFile.close()


