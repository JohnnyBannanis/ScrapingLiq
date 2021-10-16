from flask import Flask
import difference
import liq_scrap

url = "https://www.pcfactory.cl/liquidacion?orden=2"

app = Flask(__name__)

@app.route('/')
def dataScraping():
    response = {}
    try:
        response = liq_scrap.scraping(url)
    except Exception as ex:
        print(ex)
    return response

@app.route("/diff")
def newData():
    response = {}
    try:
        response["data"] = list(chunks(difference.diff(), 10))
    except Exception as ex:
        print(ex)
    return response

@app.route("/categories")
def categories():
    response = {}
    try:
        category_names = liq_scrap.scraping(url)
        catego_list = []
        for catego in category_names.keys():
            a = {}
            a["label"] = catego.capitalize()
            a["value"] = catego
            catego_list.append(a)
        response["data"] = catego_list
    except Exception as ex:
        print(ex)
    return response

@app.route("/categories/<key>")
def category(key):
    response = {}
    try:
        scraping = liq_scrap.scraping(url)
        response["data"] = list(chunks(scraping[key], 10))
        print(scraping[key])
        print(response)
    except Exception as ex:
        print(ex)
    return response

def chunks(l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

if __name__ == '__main__':
    #set host and port
    app.run(port=5005)