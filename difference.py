import json
import liq_scrap

url = "https://www.pcfactory.cl/liquidacion"

def diff():
    with open('db.json') as json_file:
        db = json.load(json_file)
    
    response = liq_scrap.scraping(url)

    inPage = []
    inDb = []
    newItems = []
    for category in response.keys():
        inPage.extend(response[category])
    for category in db.keys():
        inDb.extend(db[category])

    for item in inPage:
        if item not in inDb:
            newItems.append(item)

    if (len(inPage)-len(inDb)) != 0 or (len(newItems) < 0):
        with open('db.json', 'w') as outfile:
            json.dump(response, outfile)
    return newItems