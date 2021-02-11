import cv2 as cv
import numpy as np
import kociemba

DEBUG = False
eps = 0.00001
firstRead = []
secondRead = []
firstDone = False

cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
W, H = int(cam.get(cv.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
if W != 1280 or H != 720:
    print("WARNING!!! This software was prepared according to 1280x720 camera resolution, but your resolution is %dx%d, this may or may not cause problems" % (W, H))

color_white = (255, 255, 255)
color_yellow = (0, 255, 255)
color_red = (0, 0, 255)
color_orange = (0, 162, 255)
color_green = (0, 255, 0)
color_blue = (255, 0, 0)

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def minus(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def plus(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def times(a, p):
    return (a*p[0], a*p[1])

def length(p):
    return (p[0]**2 + p[1]**2)**0.5

def area(l):
    alan = 0
    for i in range(0, len(l)):
        alan += l[i][0]*l[i-1][1] - l[i-1][0]*l[i][1]
    return abs(alan/2)

def turnHSV(arr):
    tmp = np.zeros((1, len(arr), 3), np.uint8)
    for i in range(len(arr)):
        tmp[0][i] = np.array([arr[i][0], arr[i][1], arr[i][2]])
    tmp = cv.cvtColor(tmp, cv.COLOR_BGR2HSV)
    for i in range(len(arr)):
        arr[i] = [(float(tmp[0][i][0] + 30) % 180), float(tmp[0][i][1]), float(tmp[0][i][2]), i]
    return np.array(arr)

def fill(kup, face, up):
    if face[4] == 0:
        x = 0
        if up == 1:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 4:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 5:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 2:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    elif face[4] == 1:
        x = 36
        if up == 0:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 5:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 4:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 3:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    elif face[4] == 2:
        x = 18
        if up == 0:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 4:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 5:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 3:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    elif face[4] == 3:
        x = 45
        if up == 2:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 4:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 5:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 1:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    elif face[4] == 4:
        x = 27
        if up == 0:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 1:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 2:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 3:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    elif face[4] == 5:
        x = 9
        if up == 0:
            kup[x+0] = face[0]
            kup[x+1] = face[1]
            kup[x+2] = face[2]
            kup[x+3] = face[3]
            kup[x+4] = face[4]
            kup[x+5] = face[5]
            kup[x+6] = face[6]
            kup[x+7] = face[7]
            kup[x+8] = face[8]
        elif up == 2:
            kup[x+0] = face[6]
            kup[x+1] = face[3]
            kup[x+2] = face[0]
            kup[x+3] = face[7]
            kup[x+4] = face[4]
            kup[x+5] = face[1]
            kup[x+6] = face[8]
            kup[x+7] = face[5]
            kup[x+8] = face[2]
        elif up == 1:
            kup[x+0] = face[2]
            kup[x+1] = face[5]
            kup[x+2] = face[8]
            kup[x+3] = face[1]
            kup[x+4] = face[4]
            kup[x+5] = face[7]
            kup[x+6] = face[0]
            kup[x+7] = face[3]
            kup[x+8] = face[6]
        elif up == 3:
            kup[x+0] = face[8]
            kup[x+1] = face[7]
            kup[x+2] = face[6]
            kup[x+3] = face[5]
            kup[x+4] = face[4]
            kup[x+5] = face[3]
            kup[x+6] = face[2]
            kup[x+7] = face[1]
            kup[x+8] = face[0]
        else:
            return False
    else:
        return False

def getcolor(code):
    if code == 0:
        return color_white
    elif code == 1:
        return color_red
    elif code == 2:
        return color_orange
    elif code == 3:
        return color_yellow
    elif code == 4:
        return color_green
    elif code == 5:
        return color_blue
    else:
        error_im = np.zeros(raw.shape, np.uint8)
        error_im = cv.putText(error_im, 'Unexpected error occured :(', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        error_im = cv.putText(error_im, 'Press Enter to exit', (10, 180), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv.imshow("Rubik's Cube Solver", error_im)
        cv.waitKey()
        exit(1)

def intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    ax = (x3*(y4-y3)/(x4-x3) - x1*(y2-y1)/(x2-x1) + y1 - y3)/((y4-y3)/(x4-x3) - (y2-y1)/(x2-x1))
    ay = (ax-x1)*(y2-y1)/(x2-x1) + y1
    return ax, ay

while True:
    isTrue, raw = cam.read()
    if isTrue == False:
        break

    raw = cv.flip(raw, 1)

    if firstDone == False:
        raw = cv.rectangle(raw, (0, H-40), (W, H), (55, 55, 55), -1)
        raw = cv.putText(raw, "Show one corner of the cube to the camera, Q to exit", (10, H-12), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    else:
        raw = cv.circle(raw, (40, H-50), 100, (255, 255, 255), -1)
        raw = cv.line(raw, (40, H-50), (100, H-110), (0, 150, 0), 10)
        raw = cv.line(raw, (10, H-80), (40, H-50), (0, 150, 0), 10)
        raw = cv.rectangle(raw, (0, H-40), (W, H), (55, 55, 55), -1)
        raw = cv.putText(raw, "Now show the opposite corner to the camera, Q to exit", (10, H-12), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    #* canny edge detection
    blur = cv.medianBlur(raw, 7)
    canny = cv.Canny(blur, 50, 150)
    scanning_areas = canny.copy()
    canny_gray = canny.copy()
    canny = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)

    #* Draw cube skeleton
    pts = np.array([
        [665, 115], 
        [885, 200], 
        [855, 428], 
        [675, 571], 
        [490, 434], 
        [454, 211]
        ], np.int32)
    pts.reshape((-1, 1, 2))
    if DEBUG:
        canny = cv.polylines(canny, [pts], True, (0, 255, 0), 3)
        canny = cv.circle(canny, (675, 342), 30, (0, 0, 255))
        canny = cv.circle(canny, (675, 342), 50, (0, 0, 255))
    else:
        raw = cv.polylines(raw, [pts], True, (0, 255, 0), 3)
        raw = cv.line(raw, (885, 200), (675, 342), (0, 255, 0), 3)
        raw = cv.line(raw, (675, 571), (675, 342), (0, 255, 0), 3)
        raw = cv.line(raw, (454, 211), (675, 342), (0, 255, 0), 3)
    cube_area = area(pts)

    #* Draw two circles centered at the corner, find intersection points with edges
    little_circle_points = []
    big_circle_points = []
    points = cv.ellipse2Poly((675, 342), (30, 30), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            if len(little_circle_points) == 0 or distance((x, y), little_circle_points[-1]) > 30:
                little_circle_points.append((x, y))
    points = cv.ellipse2Poly((675, 342), (50, 50), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            if len(big_circle_points) == 0 or distance((x, y), big_circle_points[-1]) > 30:
                big_circle_points.append((x, y))

    all_edges_found = False
    if len(little_circle_points) > 0 and len(big_circle_points) > 0 and distance(little_circle_points[0], big_circle_points[0]) < 22:
        canny = cv.line(canny, little_circle_points[0], big_circle_points[0], (0, 255, 0), 2)
    if len(little_circle_points) > 1 and len(big_circle_points) > 1 and distance(little_circle_points[1], big_circle_points[1]) < 22:
        canny = cv.line(canny, little_circle_points[1], big_circle_points[1], (0, 255, 0), 2)
    if len(little_circle_points) > 2 and len(big_circle_points) > 2 and distance(little_circle_points[2], big_circle_points[2]) < 22:
        canny = cv.line(canny, little_circle_points[2], big_circle_points[2], (0, 255, 0), 2)
        all_edges_found = True

    if all_edges_found:
        #* All found points
        x1, y1 = little_circle_points[0][0] + eps, little_circle_points[0][1] + eps
        x2, y2 = big_circle_points[0][0], big_circle_points[0][1]
        x3, y3 = little_circle_points[1][0] + eps, little_circle_points[1][1] + eps
        x4, y4 = big_circle_points[1][0], big_circle_points[1][1]
        x5, y5 = little_circle_points[2][0] + eps, little_circle_points[2][1] + eps
        x6, y6 = big_circle_points[2][0], big_circle_points[2][1]

        #* Find middle corner
        axis1, center_y1 = intersection(x1, y1, x2, y2, x3, y3, x4, y4)
        axis2, center_y2 = intersection(x3, y3, x4, y4, x5, y5, x6, y6)
        center_x3, center_y3 = intersection(x5, y5, x6, y6, x1, y1, x2, y2)
        center_x, center_y = (axis1 + axis2 + center_x3)/3, (center_y1 + center_y2 + center_y3)/3
        center = int(center_x), int(center_y)
        if center_x > 100000 or center_y > 100000:
            continue
        if DEBUG and 0 < center_x < 1000 and 0 < center_y < 1000:
            canny = cv.circle(canny, center, 5, (255, 255, 0), -1)
        
        #* Find corners near middle corner
        dilated_edges = cv.dilate(canny, np.ones((10, 10), np.uint8))
        dx, dy = big_circle_points[0][0] - little_circle_points[0][0], big_circle_points[0][1] - little_circle_points[0][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        corner1_x, corner1_y = center_x + dx*200, center_y + dy*200
        while 0 < corner1_x < W and 0 < corner1_y < H:
            if dilated_edges[int(corner1_y), int(corner1_x)].all() == 0:
                break
            corner1_x += dx
            corner1_y += dy
        corner1_x -= 5*dx
        corner1_y -= 5*dy

        dx, dy = big_circle_points[1][0] - little_circle_points[1][0], big_circle_points[1][1] - little_circle_points[1][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        corner2_x, corner2_y = center_x + dx*200, center_y + dy*200
        canny = cv.circle(canny, (int(corner2_x), int(corner2_y)), 10, (0, 0, 255))
        while 0 < corner2_x < W and 0 < corner2_y < H:
            if dilated_edges[int(corner2_y), int(corner2_x)].all() == 0:
                break
            corner2_x += dx
            corner2_y += dy
        corner2_x -= 5*dx
        corner2_y -= 5*dy

        dx, dy = big_circle_points[2][0] - little_circle_points[2][0], big_circle_points[2][1] - little_circle_points[2][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        corner3_x, corner3_y = center_x + dx*200, center_y + dy*200
        while 0 < corner3_x < W and 0 < corner3_y < H:
            if dilated_edges[int(corner3_y), int(corner3_x)].all() == 0:
                break
            corner3_x += dx
            corner3_y += dy
        corner3_x -= 5*dx
        corner3_y -= 5*dy

        corner1 = (int(corner1_x), int(corner1_y))
        corner2 = (int(corner2_x), int(corner2_y))
        corner3 = (int(corner3_x), int(corner3_y))

        if DEBUG:
            canny = cv.circle(canny, corner1, 10, (0, 0, 255))
            canny = cv.circle(canny, corner2, 10, (0, 0, 255))
            canny = cv.circle(canny, corner3, 10, (0, 0, 255))

        #* Estimate other corners
        far_corner1 = plus(minus(corner1, center), corner2)
        far_corner2 = plus(minus(corner2, center), corner3)
        far_corner3 = plus(minus(corner3, center), corner1)

        far_corner1 = minus(far_corner1, times(0.13, minus(far_corner1, center)))
        far_corner2 = minus(far_corner2, times(0.13, minus(far_corner2, center)))
        far_corner3 = minus(far_corner3, times(0.13, minus(far_corner3, center)))
        far_corner1 = (int(far_corner1[0]), int(far_corner1[1]))
        far_corner2 = (int(far_corner2[0]), int(far_corner2[1]))
        far_corner3 = (int(far_corner3[0]), int(far_corner3[1]))
        
        #* Check if calculated area and skeleton area matches
        unsuccessful = False
        calculated_area = area([corner1, far_corner1, corner2, far_corner2, corner3, far_corner3])
        error = abs(calculated_area - cube_area)/cube_area
        if error < 0.1:
            if DEBUG:
                canny = cv.circle(canny, far_corner1, 10, (0, 0, 255))
                canny = cv.circle(canny, far_corner2, 10, (0, 0, 255))
                canny = cv.circle(canny, far_corner3, 10, (0, 0, 255))

                scanning_areas = cv.circle(scanning_areas, corner1, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, corner2, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, corner3, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, far_corner1, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, far_corner2, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, far_corner3, 10, (255, 255, 255))

            #* Divide faces and extract colors
            read = []
            for faces in range(3):
                if faces == 0:
                    axis1 = minus(corner1, center)
                    axis2 = minus(corner2, center)
                elif faces == 1:
                    axis1 = minus(corner2, center)
                    axis2 = minus(corner3, center)
                else:
                    axis1 = minus(corner3, center)
                    axis2 = minus(corner1, center)

                for i in range(3):
                    for j in range(3):
                        piece_corner1 = plus(center, plus(times( i   /3, axis1), times( j   /3, axis2)))
                        piece_corner2 = plus(center, plus(times((i+1)/3, axis1), times( j   /3, axis2)))
                        piece_corner3 = plus(center, plus(times( i   /3, axis1), times((j+1)/3, axis2)))
                        piece_corner4 = plus(center, plus(times((i+1)/3, axis1), times((j+1)/3, axis2)))

                        piece_corner1 = minus(piece_corner1, times(0.13*min(i  , j  )/3, minus(piece_corner1, center)))
                        piece_corner2 = minus(piece_corner2, times(0.13*min(i+1, j  )/3, minus(piece_corner2, center)))
                        piece_corner3 = minus(piece_corner3, times(0.13*min(i  , j+1)/3, minus(piece_corner3, center)))
                        piece_corner4 = minus(piece_corner4, times(0.13*min(i+1, j+1)/3, minus(piece_corner4, center)))

                        piece_mask = np.zeros((canny.shape[0], canny.shape[1]), np.uint8)
                        pts = np.array([
                            [piece_corner1[0], piece_corner1[1]], 
                            [piece_corner2[0], piece_corner2[1]], 
                            [piece_corner4[0], piece_corner4[1]],
                            [piece_corner3[0], piece_corner3[1]]
                            ], np.int32)
                        pts.reshape((-1, 1, 2))
                        piece_mask = cv.fillPoly(piece_mask, [pts], (255, 255, 255))
                        piece_mask = cv.erode(piece_mask, np.ones((35,35), np.uint8)) # erode to prevent little misplacements

                        scanning_areas = cv.bitwise_or(scanning_areas, piece_mask)

                        # uncomment for higher accuracy but hard match
                        # edge_check = cv.mean(canny, piece_mask)
                        # if edge_check[0] > 0:
                        #     olmadi = True

                        #* If color picking area is so small, retreat
                        cube_area = cv.mean(piece_mask)
                        if cube_area[0] < 0.005:
                            unsuccessful = True

                        read_color = cv.mean(raw, piece_mask)
                        if DEBUG:
                            canny = cv.fillPoly(canny, [pts], (int(read_color[0]), int(read_color[1]), int(read_color[2])))
                        read.append((read_color[0], read_color[1], read_color[2]))
            if DEBUG:
                cv.imshow('scanning_areas', scanning_areas)

            if unsuccessful:
                continue

            if not firstRead:
                firstRead = read
                firstDone = True
                if DEBUG:
                    cv.imshow('first read', canny)
                    cv.imshow('first read raw', raw)
            else:
                difference = 0
                for i in range(len(read)):
                    for j in range(3):
                        difference += (firstRead[i][j] - read[i][j])**2
                if difference > 270000:
                    secondRead = read
                    reads = firstRead + secondRead
                    if DEBUG:
                        cv.imshow('ikinci okuma', canny)
                        cv.imshow('ikinci okuma raw', raw)
                        print(reads)

                    #* Determine which color which
                    color_groups = [[], [], [], [], [], []]
                    reads = turnHSV(reads)

                    # First 9 least saturated color is white
                    reads = reads[reads[:,1].argsort()]
                    for i in range(9):
                        color_groups[0].append(int(reads[i][3]))
                    reads = reads[9:]

                    # Other colors are determined according to their hue value
                    reads = reads[reads[:,0].argsort()]
                    for j in range(1, 6):
                        for i in range(9):
                            color_groups[j].append(int(reads[(j-1)*9 + i][3]))

                    where = []
                    for i in range(54):
                        where.append(-1)
                    for i in range(6):
                        for j in range(9):
                            where[color_groups[i][j]] = i

                    cube_list = []
                    for i in range(54):
                        cube_list.append(-1)

                    #* Find places of pieces and fill
                    fill(cube_list, where[0:9], where[13])
                    fill(cube_list, where[9:18], where[22])
                    fill(cube_list, where[18:27], where[4])
                    fill(cube_list, where[27:36], where[40])
                    fill(cube_list, where[36:45], where[49])
                    fill(cube_list, where[45:54], where[31])

                    #* Create result image
                    result = np.zeros((H, W, 3), np.uint8)
                    seperatorThickness = 2
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10
                            py = 10 + 150 + 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[9+i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10 + 150 + 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[18+i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10 + 150 + 10
                            py = 10 + 150 + 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[27+i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10 + 150 + 10 + 150 + 10
                            py = 10 + 150 + 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[36+i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10 + 150 + 10 + 150 + 10
                            result = cv.rectangle(result, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(cube_list[45+i+j*3]), -1)
                            result = cv.rectangle(result, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            result = cv.rectangle(result, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)

                    kociemba_input_style = cube_list[0:9] + cube_list[27:36] + cube_list[18:27] + cube_list[45:54] + cube_list[9:18] + cube_list[36:45]
                    kociemba_text = str(kociemba_input_style).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
                    kociemba_text = kociemba_text.replace('0', 'U')
                    kociemba_text = kociemba_text.replace('1', 'B')
                    kociemba_text = kociemba_text.replace('2', 'F')
                    kociemba_text = kociemba_text.replace('3', 'D')
                    kociemba_text = kociemba_text.replace('4', 'R')
                    kociemba_text = kociemba_text.replace('5', 'L')
                    solution = ""
                    try:
                        solution = kociemba.solve(kociemba_text)
                    except:
                        solution = "Sorry, this cube cannot be solved. Try again"
                    
                    result = cv.putText(result, "White on top, Orange in front", (10, 520), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                    result = cv.putText(result, solution, (10, 560), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                    result = cv.putText(result, "R to retry, Q to quit", (10, 600), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

                    dx = (W - 650) // 6
                    dy = 500 // 4

                    if solution[0] != 'S':
                        solution_array = solution.split()
                        for j in range(4):
                            for i in range(6):
                                number = j*6 + i
                                if len(solution_array) <= number:
                                    break
                                center = 650 + i*dx + dx//2, j*dy + dy//2
                                minax = min(dx, dy)
                                color = (0, 0, 0)
                                if solution_array[number][0] == 'U':
                                    color = color_white[0], color_white[1], color_white[2]
                                elif solution_array[number][0] == 'L':
                                    color = color_blue[0], color_blue[1], color_blue[2]
                                elif solution_array[number][0] == 'F':
                                    color = color_orange[0], color_orange[1], color_orange[2]
                                elif solution_array[number][0] == 'R':
                                    color = color_green[0], color_green[1], color_green[2]
                                elif solution_array[number][0] == 'B':
                                    color = color_red[0], color_red[1], color_red[2]
                                elif solution_array[number][0] == 'D':
                                    color = color_yellow[0], color_yellow[1], color_yellow[2]
                                result = cv.rectangle(result, (center[0] - int(minax*0.2), center[1] - int(minax*0.2)), (center[0] + int(minax*0.2), center[1] + int(minax*0.2)), color, -1)
                                if len(solution_array[number]) == 1:
                                    result = cv.ellipse(result, center, (int(minax*0.4), int(minax*0.4)), 0, -90, 0, (0, 255, 0), 3)
                                    result = cv.line(result, (center[0] + int(minax*0.4), center[1]), (center[0] + int(minax*0.4) + int(minax*0.05), center[1] - int(minax*0.05)), (0, 255, 0), 3)
                                    result = cv.line(result, (center[0] + int(minax*0.4), center[1]), (center[0] + int(minax*0.4) - int(minax*0.05), center[1] - int(minax*0.05)), (0, 255, 0), 3)
                                elif solution_array[number][1] == "'":
                                    result = cv.ellipse(result, center, (int(minax*0.4), int(minax*0.4)), 0, -90, -180, (0, 255, 0), 3)
                                    result = cv.line(result, (center[0] - int(minax*0.4), center[1]), (center[0] - int(minax*0.4) + int(minax*0.05), center[1] - int(minax*0.05)), (0, 255, 0), 3)
                                    result = cv.line(result, (center[0] - int(minax*0.4), center[1]), (center[0] - int(minax*0.4) - int(minax*0.05), center[1] - int(minax*0.05)), (0, 255, 0), 3)
                                else:
                                    result = cv.ellipse(result, center, (int(minax*0.4), int(minax*0.4)), 0, -90, 90, (0, 255, 0), 3)
                                    result = cv.line(result, (center[0], center[1] + int(minax*0.4)), (center[0] + int(minax*0.05), center[1] + int(minax*0.4) - int(minax*0.05)), (0, 255, 0), 3)
                                    result = cv.line(result, (center[0], center[1] + int(minax*0.4)), (center[0] + int(minax*0.05), center[1] + int(minax*0.4) + int(minax*0.05)), (0, 255, 0), 3)

                    cv.imshow("Rubik's Cube Solver", result)
                    while True:
                        option = cv.waitKey() & 0xff
                        if option == ord('r') or option == ord('R'):
                            firstDone = False
                            firstRead = []
                            secondRead = []
                            break
                        elif option == ord('q') or option == ord('Q'):
                            exit(0)

    if DEBUG:
        cv.imshow('canny', canny)
    else:
        cv.imshow("Rubik's Cube Solver", raw)    

    key = cv.waitKey(20)
    if key == ord('q') or key == ord('Q'):
        break
