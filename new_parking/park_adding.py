import os, glob
import matplotlib.pyplot as plt
import network.detection.cars_detection.car_detection as car_detect
import detection_helper.spots_handling as spot_handle
import json_helper.get_park_settings as j_get
import json_helper.save_park_settings as j_save
import new_parking.park_settings as park_set


def add_park(path_):
    path_to_image=path_+'/*.jpg'
    im_path = ((glob.glob(path_to_image)))[0]
    base = os.path.basename(im_path)
    park_id=os.path.splitext(base)[0]
    path_to_json=path_+'/via_region_data.json'
    image= plt.imread(im_path)
    rows,mask=j_get.load_park_info(path_to_json)
    car_boxes=car_detect.detect_cars(image,mask)
    s_boxes=spot_handle.sort_boxes(car_boxes,rows)
    sorted_points, direction, distances,height,intersects=park_set.define_park_settings(
        s_boxes)
    j_save.save_park_settings(park_id,sorted_points,direction,distances,height,intersects,rows,mask)



add_park('path_to_save_park')