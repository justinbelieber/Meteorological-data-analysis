import json
def transfer_to_json(file):
    filename = '%s_forecast.csv' %file
    fr = open(filename, "r", encoding='utf-8')
    ls = []
    for line in fr:
        line = line.replace("\n", "")
        ls.append(line.split(","))
    fr.close()

    fw = open("%s_forecast.json" %file, "w", encoding='utf-8')
    for i in range(1, len(ls)):
        ls[i] = dict(zip(ls[0], ls[i]))
    b = json.dumps(ls[1:], sort_keys=True, indent=4, ensure_ascii=False)
    print(b)
    fw.write(b)
    fw.close()

def readJson():
    file = 'min.json'
    fr = open(file, 'rb')
    fileJson = json.load(file)
    time = fileJson['date']
    tmin = fileJson['min']

    file = 'max.json'
    fr = open(file, 'rb')
    fileJson = json.load(file)
    tmax = fileJson['max']

    return (time, tmax, tmin)
