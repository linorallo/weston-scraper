import json
def appendToJSON(productsData):
    with open('./data2.json','r+') as db:
        print('DB open')
        db.seek(0)
        parsedDB = json.load(db)
        print(parsedDB)
        for productData in productsData:

            exists = any(savedItem['name'] == productData['name']
                        for savedItem in parsedDB['data'])
            print('exists', exists)
            if not exists:
                parsedDB['data'].append(productData)
                print('+ New Item:', productData['name'])
            else:
                print('= Skipped Item', productData['name'])
        print('Analized')
        db.seek(0)
        db.write(json.dumps(parsedDB))
        print('written')
        db.truncate()
    print('DB closed')

def saveToJSON(data, page):
    f = open('./data-{}.json'.format(page), 'w')
    f.write(json.dumps({"data":data}))
    f.close()