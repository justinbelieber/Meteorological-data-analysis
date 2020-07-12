import json
#json文件输出
names = ['joker', 'jce', 'macy', 'timi']

filename = 'names.json'
with open(filename, 'w') as file_obj:
    json.dump(names, file_obj)
