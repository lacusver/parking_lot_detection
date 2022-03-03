from json_helper import get_park_settings as jout
from network.detection.cars_detection import car_detection as car_detector
from detection_helper import spots_handling as det_h


def check_width(start, sorted_points, distances, intersects, direction, heights):
    h=0
    if direction == 'x':
        for i in range(1, len(sorted_points)):
            if start < sorted_points[i][0]:
                width = distances[i - 1]
                h=heights[i-1]
                #height=sides[0][0][1],sides[0][1][1]
                if intersects[i-1]>0:
                    x0=intersects[i-1]
                else:
                    x0=0
                return width,h,x0
        return distances[-1],heights[-1],0
    elif direction== 'y':
        for i in range(1, len(sorted_points)):
            if start<sorted_points[i][1]:
                width=distances[i-1]
                h=heights[i-1]
                #height=sides[0][1][0],sides[0][1][0]
                if intersects[i-1]>0:
                    y0=intersects[i-1]
                else:
                    y0=0
                return width,h,y0
        return distances[-1],heights[-1],0


def get_boxes_in_row(sorted_car_boxes,sorted_points,direction,distances,heights,intersects):

    empty_spots=[]
    x0, y0 = sorted_points[0]
    xn,yn=sorted_points[-1]

    if direction=='x':
        for i in range(1,len(sorted_car_boxes)):
            width,h,inter_x = check_width(x0,sorted_points,distances,intersects,direction,heights )
            while sorted_car_boxes[i][1]-x0>=width:
                empty_spot=(x0,h[0],x0+width+inter_x,h[1])
                empty_spots.append(empty_spot)
                x0+=width+inter_x
                width,h,inter_x=check_width(x0,sorted_points,distances,intersects,direction,heights)
            x0=sorted_car_boxes[i][3]
        width,h,inter_x=check_width(x0,sorted_points,distances,intersects,direction,heights)
        while xn-x0>=width:
            empty_spot=(x0,h[0],x0+width+inter_x,h[1])
            empty_spots.append(empty_spot)
            x0+=width+inter_x
            width,h,inter_x=check_width(x0,sorted_points,distances,intersects,direction,heights)
    elif direction=='y':
        for i in range(1,len(sorted_car_boxes)):
            width,h,inter_y = check_width(y0,sorted_points,distances,intersects,direction,heights )
            while sorted_car_boxes[i][0]-y0>=width:
                empty_spot=(h[0],y0,h[1],y0+width+inter_y)
                empty_spots.append(empty_spot)
                y0+=width+inter_y
                width,h,inter_y=check_width(y0,sorted_points,distances,intersects,direction,heights)
            y0=sorted_car_boxes[i][2]
        width,h,inter_y=check_width(y0,sorted_points,distances,intersects,direction,heights)
        while yn-y0>=width:
            empty_spot=(h[0],y0,h[1],y0+width+inter_y)
            empty_spots.append(empty_spot)
            y0+=width+inter_y
            width,h,inter_y=check_width(y0,sorted_points,distances,intersects,direction,heights)

    return empty_spots


def detect_empty_spots(image,id):
    empty_spots = []
    sorted_points, directions,distances, heights,intersects, rows, mask = jout.get_detail_settings(id)
    car_boxes = car_detector.detect_cars(image, mask)
    sorted_car_boxes = det_h.sort_boxes(car_boxes, rows)
    for i in range(len(rows)):
        empty_spots.append(get_boxes_in_row(sorted_car_boxes[i],
                                            sorted_points[i],
                                            directions[i],
                                            distances[i],
                                            heights[i],
                                            intersects[i]))
    return empty_spots
