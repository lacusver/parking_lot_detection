import json


def load_park_info(path_):
    with open(path_, 'r') as myfile:
        data = json.load(myfile)
    attr = 'shape_attributes'
    x_points = 'all_points_x'
    y_points = 'all_points_y'

    def make_tuple_ls(x, y):
        ls = []
        for i in range(len(x)):
            point = (x[i], y[i])
            ls.append(point)
        return ls

    count = 0
    row_list = []
    mask_list = []
    im_id=next(iter(data))
    value = data[im_id]['regions']
    while str(count) in value:
        if value[str(count)]['region_attributes']['park'] == 'mask':
            x, y = value[str(count)][attr][x_points], value[str(count)][attr][y_points]
            points = make_tuple_ls(x, y)
            mask_list.append(points)
        else:
            x, y = value[str(count)][attr][x_points], value[str(count)][attr][y_points]
            points = make_tuple_ls(x, y)
            row_list.append(points)
        count += 1
    return row_list,mask_list

def get_detail_settings(id):
    path='path_to_data_json'
    key='parking_lot'
    #direction='x'
    with open(path, 'r') as myfile:
        data = json.load(myfile)
    for el in data[key]:
        if el['id']==id:
            sorted_points=el['sorted_points']
            directions=el['directions']
            distances=el['distances']
            heights=el['heights']
            interesects=el['intersects']
            rows=el['rows']
            mask=el['mask']
            return sorted_points,directions,distances,heights,interesects,rows,mask