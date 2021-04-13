# kd_helper 🍴🍴🍴
- a classic example of automation taking over a job (kitchen assistant rip)!

## how to clone repo:
- skip this part if youre familiar git at all
- go to the command line & run `git clone <https link which can be copied when you hit on code on the main page>`

## how to run 
- `python3 kd_helper.py`
- a text file, `kd_for_the_week.txt`, will be generated that details the kds for the week. 

## dependencies: 
- python3 (obviously lol)
- run `pip3 install xlsx2csv`
- try `pip install xlsx2csv` if you dont have python3

## notes: 
- If individual didnt fill out a meal time or gets a late plate more than 7 times a week (bruh what), they are marked down as available to kd for every meal. Didnt provide a preference, fair game. those that marked down a time should get priority. 
- The names in KD_Count and Meal-Sign-Ups-Spring-2021 need to match up!! Otherwise, mismatching happens & we dont want that @ kitchen assistant.
- To ensure someone doesnt get a KD, just mark down any character in the KD_Count excel file to indicate they shouldnt get a KD.
- Also, if their name is not listed in KD_Count spreadsheet, they will NOT get a KD
- This doesnt automatically update the counts of the # of KD's they've done or havent, so do that on your own time @ Kitchen Assistant. 
- If you feel the selection process is unfair, submit a pr boi 

