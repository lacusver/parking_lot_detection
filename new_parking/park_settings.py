from shapely.geometry import LineString
import detection_helper.spots_handling as spot_handle


def find_box_side(box,section):
    y1,x1,y2,x2=box
    y1,x1,y2,x2=int(y1),int(x1),int(y2),int(x2)
    sec1,sec2=section
    segm=LineString([sec1,sec2])
    if LineString([(x1,y1),(x1,y2)]).intersects(segm):
        return (x1,y1),(x1,y2)
    elif LineString([(x1,y2),(x2,y2)]).intersects(segm):
        return (x1,y2),(x2,y2)
    elif LineString([(x2,y2),(x2,y1)]).intersects(segm):
        return (x2,y1),(x2,y2)
    elif LineString([(x2,y1),(x1,y1)]).intersects(segm):
        return (x2,y1),(x1,y1)
    return None


def find_inv_side(side, box):
    y1, x1, y2, x2 = box
    y1, x1, y2, x2 = int(y1), int(x1), int(y2), int(x2)
    p1, p2 = side
    if p1[0] == p2[0]:
        if (p1[0] == x1):
            p1 = (x2, y1)
            p2 = (x2, y2)
        else:
            p1 = (x1, y1)
            p2 = (x1, y2)
    elif p1[1] == p2[1]:
        if p1[1] == y1:
            p1 = (x1, y2)
            p2 = (x2, y2)
        else:
            p1 = (x1, y1)
            p2 = (x2, y1)
    return p1, p2


def define_sides(sorted_box):
    intersects_sides=[]
    for i in range(len(sorted_box)):
        if i==len(sorted_box)-1:
            p1=spot_handle.get_mid_point(sorted_box[i - 1])
            p2=spot_handle.get_mid_point(sorted_box[i])
            side=find_box_side(sorted_box[i],(p1,p2))
            inv_side=find_inv_side(side,sorted_box[i])
            intersects_sides.append(inv_side)
        else:
            p1=spot_handle.get_mid_point(sorted_box[i])
            p2=spot_handle.get_mid_point(sorted_box[i + 1])
            side=find_box_side(sorted_box[i],(p1,p2))
            if side is None:
                p1=spot_handle.get_mid_point(sorted_box[i - 1])
                p2=spot_handle.get_mid_point(sorted_box[i])
                side=find_box_side(sorted_box[i],(p1,p2))
                side=find_inv_side(side,sorted_box[i])
            intersects_sides.append(side)
    return intersects_sides


def define_direction(all_sorted_box):
    directions=[]
    for box in all_sorted_box:
        sides=define_sides(box[1:3])
        direction=spot_handle.check_direction(sides[0])
        directions.append(direction)
    return directions


def get_spot_info(boxes, direction):
    start_x = boxes[0][0]
    start_y=boxes[0][1]
    intersects=[]
    distances = []
    heights=[]
    s=len(boxes)
    if direction=='x':
        for i in range(len(boxes)-1):
            if i==len(boxes)-2:
                dist = boxes[i + 1][3] - boxes[i][3]
                h=(int(boxes[i+1][2]),int(boxes[i+1][0]))
                #check height (intersects row)
                distances.append(dist*3.5/4)
                intersects.append(-1)
                #print(type(h))
                heights.append(h)
            else:
                dist=boxes[i+2][1]-start_x
                inter=boxes[i+1][3]-boxes[i+2][1]
                #check height
                h=(int(boxes[i+1][2]),int(boxes[i+1][0]))
                distances.append(dist*3.5/4)
                intersects.append(float(inter))
                heights.append(h)
                start_x=boxes[i+1][3]
    elif direction=='y':
        for i in range(len(boxes)-1):
            if i==len(boxes)-2:
                dist = boxes[i + 1][2] - boxes[i][2]
                h = (int(boxes[i + 1][3]), int(boxes[i + 1][1]))
                # check height (intersects row)
                distances.append(dist * 3.5 / 4)
                intersects.append(-1)
                heights.append(h)
            else:
                dist = boxes[i + 2][0] - start_y
                inter = boxes[i + 1][2] - boxes[i + 2][0]
                # check height
                h = (int(boxes[i + 1][3]), int(boxes[i + 1][1]))
                distances.append(dist * 3.5 / 4)
                intersects.append(float(inter))
                heights.append(h)
                start_y=boxes[i+1][2]

    return distances,heights,intersects


def transform_box(boxes):
    trans_boxes=[boxes[0]]
    for i in range(1,len(boxes)):
        trans_boxes.append(spot_handle.get_mid_point(boxes[i]))
    return trans_boxes


def get_all_spots_info(s_boxes,directions):
    distances = []
    intersects=[]
    heights=[]
    for i in range(len(s_boxes)):
        dist,h,inter = get_spot_info(s_boxes[i], directions[i])
        distances.append(dist)
        intersects.append(inter)
        heights.append(h)
    return distances,heights,intersects


def define_park_settings(s_boxes):
    s_points=[]
    directions=define_direction(s_boxes)
    distances,heights,intersects=get_all_spots_info(s_boxes,directions)
    for i in s_boxes:
        s_points.append(transform_box(i))
    return s_points,directions,distances,heights,intersects



