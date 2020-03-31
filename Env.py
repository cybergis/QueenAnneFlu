import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import itertools, math, os, random, scipy

class House: #house is class
    def __init__(self, row_number):
        self.houseID = row_number
        self.houseX = None
        self.houseY = None
        self.houseMemberCount = None

class School: # school is class
    def __init__(self, row_number):
        self.schoolID = row_number
        self.schoolX = None
        self.schoolY = None

class Work: # work is class
    def __init__(self, row_number):
        self.workID = row_number
        self.workX = None
        self.workY = None

# import *.csv file 
# each school has id and x, y coordinates
def settingSchools(data_path): 
    schoolData = pd.read_csv(os.path.join(data_path, "schools_points.csv"))
    schoolData['schoolID']=list(range(0,len(schoolData),1))

    schoolList = [School(i) for i in range(len(schoolData))]
    print("...setting schools...")
    for i in range(len(schoolList)):
        row_school = schoolData.iloc[i]
        school = schoolList[i]
        school.schoolID = row_school['schoolID']
        school.schoolX = row_school['X']
        school.schoolY = row_school['Y']
    return(schoolList)

# import *.csv file 
# each workplace has id and x, y coordinates
def settingWorks(data_path):
    workData = pd.read_csv(os.path.join(data_path, 'works_points.csv'))
    workData['workID']=list(range(0,len(workData),1))
    
    workList = [Work(i) for i in range(len(workData))]
    print("...setting workplaces...")
    for i in range(len(workList)):
        row_work = workData.iloc[i]
        work = workList[i]
        work.workID = row_work['workID']
        work.workX = row_work['X']
        work.workY = row_work['Y']
    return(workList)

#i mport *.csv file 
# each households has id and x, y coordinates
def settingHouseholds(data_path, schoolList, workList, houses = None):
    if houses is None:
        houseData = pd.read_csv(os.path.join(data_path, 'houses_points.csv'))
    else:
        houseData = houses
    houseData['houseID']=list(range(0,len(houseData)))
    houseList = [House(i) for i in range(len(houseData))]
    # the number of household members is also from the ACS data
    print("...setting households...")
    for i in tqdm(range(len(houseList))):
        row_house = houseData.iloc[i]
        house = houseList[i]
        house.houseID = row_house['houseID']
        house.houseX = row_house['X']
        house.houseY = row_house['Y']
        house.houseMemberCount = random.choices([1,2,3,4,5,6],weights=[0.263,0.292,0.189,0.128,0.064,0.064],k=1)
    
    # findingNearest School & Workplace
    print("...calculating distances to schools and workplaces...")
    for i in tqdm(range(len(houseList))):
        house = houseList[i]
        houseX = house.houseX
        houseY = house.houseY
        
        schoolDists = [ math.pow(houseX-school.schoolX, 2)+math.pow(houseY-school.schoolY,2) for school in schoolList ]
        schoolID = schoolDists.index(min(schoolDists))
        house.schoolID = schoolID
        house.schoolX = schoolList[schoolID].schoolX
        house.schoolY = schoolList[schoolID].schoolY
        workDists = [ math.pow(houseX-work.workX,2)+math.pow(houseY-work.workY,2) for work in workList ]
        workID = workDists.index(min(workDists))
        house.workID = workID
        house.workX = workList[workID].workX
        house.workY = workList[workID].workY
    return(houseList)


# initial infections occur at the beginning of simulation
# the number of initial infections is measured by the number of people * the introduction rates
def initialInfection(peopleList, introRate):
    susceptibleUIDs = [peopleList[i].uid for i in range(len(peopleList)) 
                          if peopleList[i].S==True]
    exposedPeople = int(len(peopleList)*introRate)
    selectedUIDs=random.sample(susceptibleUIDs,exposedPeople)
    
    for i in range(len(selectedUIDs)):
        uid = selectedUIDs[i]
        for j in range(len(peopleList)):
            person = peopleList[j]

            if person.uid == uid:
                person.E = True
        
    return(peopleList)





