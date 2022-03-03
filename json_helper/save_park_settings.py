import json


def save_park_settings(name,sorted_points,directions,distances,heights,intersects,row_list,mask_list):
    path = 'path_to_data_json'
    #data['parking_lot'] = []
    with open(path, 'r') as myfile:
        data = json.load(myfile)
    data['parking_lot'].append({
        'id': name,
        'sorted_points': sorted_points,
        'directions': directions,
        'distances': distances,
        'heights':heights,
        'intersects':intersects,
        'rows': row_list,
        'mask': mask_list})
    with open('D:/smart_park/data/data.json', 'w') as outfile:
        json.dump(data, outfile)