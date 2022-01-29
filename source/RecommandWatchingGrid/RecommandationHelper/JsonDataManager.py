import json

from source.RecommandWatchingGrid.Resources.HelperClasses.GridChannel import GridChannel

json_data = None
with open("../Resources/Jsons/ResponseGridAPI/channel.json", 'r') as f:
    json_data = json.load(f)

channel_list = []

for data in json_data:
    channel_list.append(GridChannel(data))


print(json_data)

