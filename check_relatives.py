from flask import request
from models import Citizen


def checkrelatives(listOfCitizens):
    for citizen in listOfCitizens:
        relatives = citizen['relatives']
        for rltv in relatives:
            found_citizen = Citizen.query.filter_by(citizen_id=rltv).first()
            if found_citizen is None:
                print("not found")
                return 0
            elif citizen['citizen_id'] not in list(map(int, found_citizen.relatives.split())):
                # print(list(map(int, found_citizen.relatives.split())))
                print(rltv)
                return 0
            else:
                continue
    return 1
