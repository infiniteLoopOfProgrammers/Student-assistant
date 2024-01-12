import json     
def inputs():
    return 30 , 31 

def fittnessinputs():
    with open('json\help.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)
    courses_co = courses[0]
    fittnessobj={
        "dont_times":courses_co["dontTimes"],  #default baraye not quchani
        "default_wontTime":["08:00","18:00"],
        "has_dormitory" :courses_co["dormitory"],
        "userAvg":float(courses_co["average"]),
        "min_unit":int(courses_co["minUnit"]),
        "max_unit":int(courses_co["maxUnit"]),
        "dont_days":courses_co["dontDays"],
        "Feshorde":int(courses_co["distribution"]),
        "native":courses_co["native"]
        
    }
    return fittnessobj