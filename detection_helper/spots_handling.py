import math
from shapely.geometry import Point,LineString
from shapely.geometry.polygon import Polygon


def find_start_point(points):
    p1, p2 = points
    x1, y1 = p1
    x2, y2 = p2

    x_m = (x1 + x2) / 2
    y_m = (y1 + y2) / 2
    return x_m, y_m


def find_close_point(point,cars):
    all_distances=[]
    ind=0
    for p in cars:
        distance=get_distance(point,get_mid_point(p))
        all_distances.append((distance,p,ind))
        ind+=1
    min_dis=min(all_distances)
   # print(min_dis)
    return min_dis[1],min_dis[2]


def get_distance(point1,point2):
    dist=math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)
    return dist


def get_mid_point(box):
    y1, x1, y2, x2 = box
    mid_p=((x1 +x2)/2 ,(y1 + y2)/2 )
    return mid_p


def get_mid_boxes(car_boxes):
    car_mid_points=[]
    for box in car_boxes:
        mid_p=get_mid_point(box)
        car_mid_points.append((mid_p,box))
    return car_mid_points


def check_point_in_polygon(row_list, point):
    ind_r = 0
    for row in row_list:
        polygon = Polygon(row)
        p = Point(point)
        if polygon.contains(p):
            return ind_r, point
        ind_r += 1
    return None


def get_box_in_row(car_boxes,rows):
    car_mid_points=get_mid_boxes(car_boxes)
    row_points = []
    for point in car_mid_points:
        res = check_point_in_polygon(rows, point[0])
        if res is not None:
            print(point[1])
            row_points.append((res, point[1]))
    box_in_row = {}
    for point in row_points:
        val_p = [point[1]]
        #     print(val_p)
        if point[0][0] in box_in_row:
            value = box_in_row.get(point[0][0])
            #         print("value ",value)
            value.append(point[1])
            #         print(value)
            box_in_row[point[0][0]] = value
        else:
            box_in_row[point[0][0]] = val_p
    return box_in_row


def sort_in_row(box_in_row,row):
    start_point = find_start_point(row[:2])
    car_set = box_in_row.copy()
    s_cars = [start_point]
    #s_cars = []
    for i in range(len(box_in_row)):
        close_car, ind = find_close_point(start_point, car_set)
        s_cars.append(close_car)
        car_set.pop(ind)
        start_point = get_mid_point(close_car)
    return s_cars


def sort_boxes(car_boxes,rows):
    sorted_box=[]
    box_in_row=get_box_in_row(car_boxes,rows)
    a=len(rows)
    for i in range(len(rows)):
        if i in box_in_row:
            sorted_box.append(sort_in_row(box_in_row[i],
                                      rows[i]))
        else:
            sorted_box.append([])
    return sorted_box

def check_direction(side):
    p1,p2=side
    if p1[0]==p2[0]:
        return 'x'
    elif p1[1]==p2[1]:
        return 'y'
    else:
        return None