import csv,json

def getHeaders():
    headers = ['SKU', 'NAME', 'PRODUCT DESCRIPTION']
    with open('./data-44.json','r+') as dataFile:
        jsonData = json.load(dataFile)
        parsedData =[]
        for jsonItem in  jsonData['data']:
            parsedData+=jsonItem
        for item in parsedData:
            for key in item['specs'].keys():
                if key not in headers:
                    headers.append(key)
    return [header.replace(':','') for header in headers]

def transformData():
    fileName = input('File name: ')
    f = open('./transformed_data/{}.csv'.format(fileName),'w')
    writer = csv.writer(f)
    headers = getHeaders()
    writer.writerow(headers)
    with open('./data-11.json','r+') as dataFile:
        jsonData = json.load(dataFile)
        print(len(jsonData['data']))
        parsedData =[]
        for jsonItem in  jsonData['data']:
            parsedData+=jsonItem
        for item in parsedData:
            line = [""]*len(headers)
            line[0] = item['specs']['MODEL NUMBER']
            line[1] = item['name'].replace(',','')

            for spec in headers[2:]:
                specsParsed = [
                    itemName.replace(':', '')
                    for itemName in item['specs'].keys()
                ]
                if spec in specsParsed:
                    idx = headers.index(spec)
                    try:
                        line[idx] = item['specs'][spec.replace(':','')]
                    except KeyError:
                        line[idx]=item['specs'][spec+':']
            writer.writerow(line)
            #if line[0] == '905-0246':
            #    break


def transformDataV2():
    fileName = input('File name: ')
    f = open('./transformed_data/{}.csv'.format(fileName), 'w')
    writer = csv.writer(f)
    headers = getHeaders()
    writer.writerow(headers)
    with open('./data-11.json', 'r+') as dataFile:
        jsonData = json.load(dataFile)
        print(len(jsonData['data']))
        parsedData = []
        for jsonItem in jsonData['data']:
            parsedData += jsonItem
        for item in parsedData:
            productDescription = '<ul>'
            for spec in headers[2:]:
                specsParsed = [
                    itemName.replace(':', '')
                    for itemName in item['specs'].keys()
                ]

                if spec in specsParsed:
                    li = '<li> {}: '.format(spec)
                    try:
                        li += item['specs'][spec.replace(':','')] + '</li>'
                    except KeyError:
                        li += item['specs'][spec + ':'] + '</li>'
                    productDescription += li
            productDescription += '</ul>'

            line = [""] * len(headers)
            line[0] = item['specs']['MODEL NUMBER']
            line[1] = item['name'].replace(',', '')
            line[2] = productDescription

            writer.writerow(line)
            #if line[0] == '905-0246':
            #    break


def transformDataV3():
    fileName = input('File name: ')
    f = open('./transformed_data/{}.csv'.format(fileName), 'w')
    writer = csv.writer(f)
    headers = getHeaders()
    writer.writerow(headers)
    with open('./data-44.json', 'r+') as dataFile:
        jsonData = json.load(dataFile)
        print(len(jsonData['data']))
        parsedData = []
        for jsonItem in jsonData['data']:
            parsedData += jsonItem
        for item in parsedData:
            productDescription = ''
            for spec in headers[2:]:
                specsParsed = [
                    itemName.replace(':', '')
                    for itemName in item['specs'].keys()
                ]

                if spec in specsParsed:
                    li = '{}: '.format(spec)
                    try:
                        li += item['specs'][spec.replace(':', '')] + '\n'
                    except KeyError:
                        li += item['specs'][spec + ':'] + '\n'
                    productDescription += li

            line = [""] * len(headers)
            line[0] = item['specs']['MODEL NUMBER']
            line[1] = item['name'].replace(',', '')
            line[2] = productDescription
            

            writer.writerow(line)
            #if line[0] == '905-0246':
            #    break


transformDataV3()