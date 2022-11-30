import json
#Create a JSON Object

def createJSON(PATH):

    json_obj = []
    json_obj.append({
        'date_created': '01-01-2015',
        'name': '01-01-2015.mp4',
        })
    #Write the object to file.
    with open('example.json','w') as jsonFile:
        json.dump(json_obj, jsonFile, indent=4)
        return jsonFile

def updateJSON(target):
    with open(target) as file:
        d = json.load(file)
        newData = {'name': 'Jeffrey Bezos', 'date': '02-04-2069'}
        d.append(newData)

    with open(target, 'w') as file:
        json.dump(d, file, indent=4)


file = createJSON('test.jpg')
updateJSON('example.json')