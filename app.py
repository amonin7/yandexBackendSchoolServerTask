import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from checkDate import check_date
from generate_import_namber import generate_random_number
from birthdayMonth import month_of_birthday, current_age
import numpy as np

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Citizen
from check_relatives import checkrelatives

@app.route("/")
def hello():
    return "Hello!"


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        citi = Citizen.query.filter_by(citizen_id=id_).first()
        if citi is None:
            print("\n \t exception \n")
            return "The input data is not correct", 400
        else:
            return jsonify(citi.serialize())
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        citi = Citizen.query.all()
        return jsonify([c.serialize() for c in citi])
    except Exception as e:
        return str(e), 400


@app.route("/imports", methods=['POST'])
def import_data():
    try:
        listOfCitizens = request.get_json()
        listOfCitizens = listOfCitizens["citizens"]
        import_id = generate_random_number()
        for citizen in listOfCitizens:
            citizen_id = citizen['citizen_id']
            if citizen_id < 0:
                return "The citizen_id is not valid", 400

            town = citizen['town']
            flag = False
            for c in town:
                if c.isalpha() or c.isdigit():
                    flag = True
            if not flag or len(town) > 256 or len(town) == 0:
                return "The town string is not valid", 400

            street = citizen['street']
            flag = False
            for c in street:
                if c.isalpha() or c.isdigit():
                    flag = True
            if not flag or len(street) > 256 or len(street) == 0:
                return "The street string is not valid", 400

            building = citizen['building']
            flag = False
            for c in building:
                if c.isalpha() or c.isdigit():
                    flag = True
            if not flag or len(building) > 256 or len(building) == 0:
                return "The building string is not valid", 400

            apartment = citizen['apartment']
            if apartment < 0:
                return "The apartment is not valid", 400

            name = citizen['name']
            if len(name) > 256 or len(name) == 0:
                return "The name string is not valid", 400

            birth_date = citizen['birth_date']
            if check_date(birth_date) == 0:
                return "The date of birth is not valid", 400

            gender = citizen['gender']
            if gender != "male" or gender != "female":
                return "The gender string is not valid", 400

            relatives = ' '.join([str(e) for e in citizen['relatives']])
            citi = Citizen(
                import_id=import_id,
                citizen_id=citizen_id,
                town=town,
                street=street,
                building=building,
                apartment=apartment,
                name=name,
                birth_date=birth_date,
                gender=gender,
                relatives=relatives
            )
            db.session.add(citi)
            db.session.commit()
        if checkrelatives(listOfCitizens) == 0:
            '''
            delete_this = Citizen.query.filter_by(import_id=import_id)
            for citi in delete_this:
                db.session.delete(citi)
            db.session.commit()
            '''
            return "You have a trouble with relatives relationship", 400
        return jsonify({"data": {
            "import_id": import_id
        }}), 201
    except Exception as e:
        print("\n \t exception \n")
        print(str(e))
        return "The input data is not correct", 400


@app.route("/imports/<imports_id>/citizens/<citizen_id>", methods=['PATCH'])
def modify(imports_id, citizen_id):
    try:
        currentCitizen = request.get_json()
        found_citizen = Citizen.query.filter_by(citizen_id=citizen_id, import_id=imports_id).first()
        if found_citizen is None:
            return "There is no such citizen", 400
        else:
            if "town" in currentCitizen.keys():
                found_citizen.town = currentCitizen['town']
                flag = False
                for c in found_citizen.town:
                    if c.isalpha() or c.isdigit():
                        flag = True
                if not flag or len(found_citizen.town) > 256 or len(found_citizen.town) == 0:
                    return "The town string is not valid", 400
            if "street" in currentCitizen.keys():
                found_citizen.street = currentCitizen['street']
                flag = False
                for c in found_citizen.street:
                    if c.isalpha() or c.isdigit():
                        flag = True
                if not flag or len(found_citizen.street) > 256 or len(found_citizen.street) == 0:
                    return "The street string is not valid", 400
            if "building" in currentCitizen.keys():
                found_citizen.building = currentCitizen['building']
                flag = False
                for c in found_citizen.building:
                    if c.isalpha() or c.isdigit():
                        flag = True
                if not flag or len(found_citizen.building) > 256 or len(found_citizen.building) == 0:
                    return "The building string is not valid", 400
            if "apartment" in currentCitizen.keys():
                found_citizen.apartment = currentCitizen['apartment']
                if found_citizen.apartment < 0:
                    return "The apartment is not valid", 400
            if "name" in currentCitizen.keys():
                found_citizen.name = currentCitizen['name']
                if len(found_citizen.name) > 256 or len(found_citizen.name) == 0:
                    return "The name string is not valid", 400
            if "birth_date" in currentCitizen.keys():
                found_citizen.birth_date = currentCitizen['birth_date']
                if check_date(found_citizen.birth_date) == 0:
                    return "The date of birth is not valid", 400
            if "gender" in currentCitizen.keys():
                found_citizen.gender = currentCitizen['gender']
                if found_citizen.gender != "male" or found_citizen.gender != "female":
                    return "The gender string is not valid", 400
            if "relatives" in currentCitizen.keys():
                relatives = currentCitizen['relatives']
                for rltv in relatives:
                    found_other_citizen = Citizen.query.filter_by(citizen_id=rltv).first()
                    other_rltvs = found_other_citizen.relatives
                    other_rltvs = list(map(int, other_rltvs.split()))
                    if int(citizen_id) not in other_rltvs:
                        other_rltvs.append(int(citizen_id))
                    found_other_citizen.relatives = ' '.join([str(e) for e in other_rltvs])
                    db.session.commit()

                old_relatives = list(map(int, found_citizen.relatives.split()))
                for old_rltv in old_relatives:
                    if int(old_rltv) not in relatives:
                        # print("1")
                        found_other_citizen = Citizen.query.filter_by(citizen_id=old_rltv).first()
                        other_rltvs = found_other_citizen.relatives
                        other_rltvs = list(map(int, other_rltvs.split()))
                        if int(citizen_id) in other_rltvs:
                            other_rltvs.remove(int(citizen_id))
                        found_other_citizen.relatives = ' '.join([str(e) for e in other_rltvs])
                        db.session.commit()

                found_citizen.relatives = ' '.join([str(e) for e in currentCitizen['relatives']])

            db.session.commit()
        return jsonify({"data": found_citizen.serialize()}), 200
    except Exception as e:
        return "The input data is not correct \n", 400


@app.route("/imports/<import_id>/citizens", methods=['GET'])
def get_some(import_id):
    try:
        citizens = Citizen.query.filter_by(import_id=import_id)
        return jsonify({"data": [c.serialize() for c in citizens]}), 200
    except Exception as e:
        return str(e), 400


@app.route("/deleteall")
def delete_all():
    try:
        for i in range(6, 7):
            delete_this = Citizen.query.filter_by(citizen_id=i).first()
            db.session.delete(delete_this)
            db.session.commit()
    except Exception as e:
        return str(e), 400


@app.route("/imports/<import_id>/citizens/birthdays", methods=['GET'])
def birthdays(import_id):
    presents = dict()
    try:
        citizens = Citizen.query.filter_by(import_id=import_id)
        for citi in citizens:
            month = month_of_birthday(citi.birth_date)
            if month != 0:
                if month in presents.keys():
                    presents_for_citizen = presents[month]
                else:
                    presents_for_citizen = dict()
                relatives = list(map(int, citi.relatives.split()))
                for rltv in relatives:
                    if rltv in presents.keys():
                        presents_for_citizen[rltv] += 1
                    else:
                        presents_for_citizen[rltv] = 1
                presents[month] = presents_for_citizen
        for i in range(1, 13):
            if i not in presents.keys():
                presents[i] = []
            else:
                presents_list = list()
                for citizen in presents[i].keys():
                    presents_list.append({"citizen_id": citizen, "presents": presents[i][citizen]})
                presents[i] = presents_list
        return jsonify({"data": presents}), 200
    except Exception as e:
        return str(e), 400


@app.route("/imports/<import_id>/towns/stat/percentile/age")
def percentile(import_id):
    try:
        birthdays_list = dict()
        citizens = Citizen.query.filter_by(import_id=import_id)
        for citi in citizens:
            if citi.town in birthdays_list.keys():
                birthdays_list[citi.town].append(current_age(citi.birth_date))
            else:
                birthdays_list[citi.town] = list()
                birthdays_list[citi.town].append(current_age(citi.birth_date))
        answer = list()
        for town in birthdays_list.keys():
            prcntl = np.percentile(birthdays_list[town], [50, 75, 99])
            birthdays_list[town] = list(prcntl)
            for i in range(len(birthdays_list[town])):
                birthdays_list[town][i] = np.round(birthdays_list[town][i], 2)
            answer.append({"town": town,
                           "p50": birthdays_list[town][0],
                           "p75": birthdays_list[town][1],
                           "p99": birthdays_list[town][2]})

        return jsonify({"data": answer}), 200
    except Exception as e:
        return str(e), 400


# if __name__ == '__main__':
app.run(host='0.0.0.0', port=8080)
