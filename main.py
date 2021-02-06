import cv2 as cv
import numpy as np
import random
try:
    import clipboard
except:
    pass

DEBUG = False

cam = cv.VideoCapture(0)

eps = 0.00001
W, H = cam.get(cv.CAP_PROP_FRAME_WIDTH), cam.get(cv.CAP_PROP_FRAME_HEIGHT)

firstRead = []
secondRead = []

firstDone = False
secondDone = False

def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def cikar(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def topla(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def carp(a, p):
    return (a*p[0], a*p[1])

def length(p):
    return (p[0]**2 + p[1]**2)**0.5

def area(l):
    alan = 0
    for i in range(0, len(l)):
        alan += l[i][0]*l[i-1][1] - l[i-1][0]*l[i][1]
    return abs(alan/2)

def cdist(color1, color2):
    return ((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)**0.5

def turnHSV(arr):
    tmp = np.zeros((1, len(arr), 3), np.uint8)
    for i in range(len(arr)):
        tmp[0][i] = np.array([arr[i][0], arr[i][1], arr[i][2]])
    tmp = cv.cvtColor(tmp, cv.COLOR_BGR2HSV)
    for i in range(len(arr)):
        arr[i] = [(float(tmp[0][i][0] + 30) % 180), float(tmp[0][i][1]), float(tmp[0][i][2]), i]
    return np.array(arr)

def doldur(kup, face, up):
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
        return (255, 255, 255)
    elif code == 1:
        return (0, 0, 255)
    elif code == 2:
        return (0, 162, 255)
    elif code == 3:
        return (0, 255, 255)
    elif code == 4:
        return (0, 255, 0)
    elif code == 5:
        return (255, 0, 0)
    else:
        error_im = np.zeros(raw.shape, np.uint8)
        error_im = cv.putText(error_im, 'Scanning is not successful :(', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        error_im = cv.putText(error_im, 'Press Enter to exit', (10, 180), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv.imshow('raw', error_im)
        cv.waitKey()
        exit(1)

def kesisim(x1, y1, x2, y2, x3, y3, x4, y4):
    ax = (x3*(y4-y3)/(x4-x3) - x1*(y2-y1)/(x2-x1) + y1 - y3)/((y4-y3)/(x4-x3) - (y2-y1)/(x2-x1))
    ay = (ax-x1)*(y2-y1)/(x2-x1) + y1
    return ax, ay

# beyaz = 0
# kirmizi = 1
# turuncu = 2
# sari = 3
# yesil = 4
# mavi = 5

while True:
    isTrue, raw = cam.read()
    if isTrue == False:
        break

    raw = cv.flip(raw, 1)
    if firstDone:
        raw = cv.circle(raw, (100, 100), 50, (0, 255, 0), -1)
    if secondDone:
        raw = cv.circle(raw, (100, 200), 50, (0, 255, 0), -1)


# ------------------------------ Edge Detection ------------------------------ #
    blur = cv.medianBlur(raw, 7)

    canny = cv.Canny(blur, 50, 150)
    scanning_areas = canny.copy()
    canny_gray = canny.copy()
    canny = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
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
        # canny = cv.line(canny, (885, 200), (675, 342), (0, 255, 0), 3)
        # canny = cv.line(canny, (675, 571), (675, 342), (0, 255, 0), 3)
        # canny = cv.line(canny, (454, 211), (675, 342), (0, 255, 0), 3)

        canny = cv.circle(canny, (675, 342), 30, (0, 0, 255))
        canny = cv.circle(canny, (675, 342), 50, (0, 0, 255))
    else:
        raw = cv.polylines(raw, [pts], True, (0, 255, 0), 3)
        raw = cv.line(raw, (885, 200), (675, 342), (0, 255, 0), 3)
        raw = cv.line(raw, (675, 571), (675, 342), (0, 255, 0), 3)
        raw = cv.line(raw, (454, 211), (675, 342), (0, 255, 0), 3)

    alan = area(pts)
    # print(alan)

    p1 = []
    p2 = []

    points = cv.ellipse2Poly((675, 342), (30, 30), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            if len(p1) == 0 or dist((x, y), p1[-1]) > 30:
                p1.append((x, y))

    points = cv.ellipse2Poly((675, 342), (50, 50), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            if len(p2) == 0 or dist((x, y), p2[-1]) > 30:
                p2.append((x, y))

    full = False
    if len(p1) > 0 and len(p2) > 0 and dist(p1[0], p2[0]) < 22:
        canny = cv.line(canny, p1[0], p2[0], (0, 255, 0), 2)
    if len(p1) > 1 and len(p2) > 1 and dist(p1[1], p2[1]) < 22:
        canny = cv.line(canny, p1[1], p2[1], (0, 255, 0), 2)
    if len(p1) > 2 and len(p2) > 2 and dist(p1[2], p2[2]) < 22:
        canny = cv.line(canny, p1[2], p2[2], (0, 255, 0), 2)
        full = True

    if full:
        x1, y1 = p1[0][0] + eps, p1[0][1] + eps
        x2, y2 = p2[0][0], p2[0][1]
        x3, y3 = p1[1][0] + eps, p1[1][1] + eps
        x4, y4 = p2[1][0], p2[1][1]
        x5, y5 = p1[2][0] + eps, p1[2][1] + eps
        x6, y6 = p2[2][0], p2[2][1]

        # print(x1, y1)
        # print(x2, y2)
        # print(x3, y3)
        # print(x4, y4)

        ax1, ay1 = kesisim(x1, y1, x2, y2, x3, y3, x4, y4)
        ax2, ay2 = kesisim(x3, y3, x4, y4, x5, y5, x6, y6)
        ax3, ay3 = kesisim(x5, y5, x6, y6, x1, y1, x2, y2)

        ax, ay = (ax1 + ax2 + ax3)/3, (ay1 + ay2 + ay3)/3

        if ax > 100000 or ay > 100000:
            continue

        center = int(ax), int(ay)
        if DEBUG and 0 < ax < 1000 and 0 < ay < 1000:
            canny = cv.circle(canny, center, 5, (255, 255, 0), -1)
        
        canny_d = cv.dilate(canny, np.ones((10, 10), np.uint8))

        dx, dy = p2[0][0] - p1[0][0], p2[0][1] - p1[0][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx1, ky1 = ax + dx*200, ay + dy*200
        while 0 < kx1 < W and 0 < ky1 < H:
            if canny_d[int(ky1), int(kx1)].all() == 0:
                break
            kx1 += dx
            ky1 += dy
        kx1 -= 5*dx
        ky1 -= 5*dy

        dx, dy = p2[1][0] - p1[1][0], p2[1][1] - p1[1][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx2, ky2 = ax + dx*200, ay + dy*200
        canny = cv.circle(canny, (int(kx2), int(ky2)), 10, (0, 0, 255))
        while 0 < kx2 < W and 0 < ky2 < H:
            if canny_d[int(ky2), int(kx2)].all() == 0:
                break
            kx2 += dx
            ky2 += dy
        kx2 -= 5*dx
        ky2 -= 5*dy

        dx, dy = p2[2][0] - p1[2][0], p2[2][1] - p1[2][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx3, ky3 = ax + dx*200, ay + dy*200
        while 0 < kx3 < W and 0 < ky3 < H:
            if canny_d[int(ky3), int(kx3)].all() == 0:
                break
            kx3 += dx
            ky3 += dy
        kx3 -= 5*dx
        ky3 -= 5*dy

        k1 = (int(kx1), int(ky1))
        k2 = (int(kx2), int(ky2))
        k3 = (int(kx3), int(ky3))

        if DEBUG:
            canny = cv.circle(canny, k1, 10, (0, 0, 255))
            canny = cv.circle(canny, k2, 10, (0, 0, 255))
            canny = cv.circle(canny, k3, 10, (0, 0, 255))

        kk1 = topla(cikar(k1, center), k2)
        kk2 = topla(cikar(k2, center), k3)
        kk3 = topla(cikar(k3, center), k1)

        kk1 = cikar(kk1, carp(0.13, cikar(kk1, center)))
        kk2 = cikar(kk2, carp(0.13, cikar(kk2, center)))
        kk3 = cikar(kk3, carp(0.13, cikar(kk3, center)))
        kk1 = (int(kk1[0]), int(kk1[1]))
        kk2 = (int(kk2[0]), int(kk2[1]))
        kk3 = (int(kk3[0]), int(kk3[1]))
        
        calculated_area = area([k1, kk1, k2, kk2, k3, kk3])

        error = abs(calculated_area - alan)/alan

        olmadi = False

        if error < 0.1:
            if DEBUG:
                canny = cv.circle(canny, kk1, 10, (0, 0, 255))
                canny = cv.circle(canny, kk2, 10, (0, 0, 255))
                canny = cv.circle(canny, kk3, 10, (0, 0, 255))

                scanning_areas = cv.circle(scanning_areas, k1, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, k2, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, k3, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, kk1, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, kk2, 10, (255, 255, 255))
                scanning_areas = cv.circle(scanning_areas, kk3, 10, (255, 255, 255))

            #* Faces
            read = []
            for faces in range(3):
                if faces == 0:
                    ax1 = cikar(k1, center)
                    ax2 = cikar(k2, center)
                elif faces == 1:
                    ax1 = cikar(k2, center)
                    ax2 = cikar(k3, center)
                else:
                    ax1 = cikar(k3, center)
                    ax2 = cikar(k1, center)
                # ax1 = topla(ax1, carp(0.16, cikar(ax1, center)))
                # ax2 = topla(ax2, carp(0.16, cikar(ax2, center)))
                for i in range(3):
                    for j in range(3):
                        b1 = topla(center, topla(carp( i   /3, ax1), carp( j   /3, ax2)))
                        b2 = topla(center, topla(carp((i+1)/3, ax1), carp( j   /3, ax2)))
                        b3 = topla(center, topla(carp( i   /3, ax1), carp((j+1)/3, ax2)))
                        b4 = topla(center, topla(carp((i+1)/3, ax1), carp((j+1)/3, ax2)))

                        b1 = cikar(b1, carp(0.13*min(i  , j  )/3, cikar(b1, center)))
                        b2 = cikar(b2, carp(0.13*min(i+1, j  )/3, cikar(b2, center)))
                        b3 = cikar(b3, carp(0.13*min(i  , j+1)/3, cikar(b3, center)))
                        b4 = cikar(b4, carp(0.13*min(i+1, j+1)/3, cikar(b4, center)))

                        mask = np.zeros((canny.shape[0], canny.shape[1]), np.uint8)

                        # mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

                        pts = np.array([
                            [b1[0], b1[1]], 
                            [b2[0], b2[1]], 
                            [b4[0], b4[1]],
                            [b3[0], b3[1]]
                            ], np.int32)

                        pts.reshape((-1, 1, 2))
                        # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        mask = cv.fillPoly(mask, [pts], (255, 255, 255))

                        mask = cv.erode(mask, np.ones((35,35), np.uint8) )

                        scanning_areas = cv.bitwise_or(scanning_areas, mask)

                        # edge_check = cv.mean(canny, mask)
                        # if edge_check[0] > 0:
                        #     olmadi = True

                        alan = cv.mean(mask)
                        if alan[0] < 0.005:
                            olmadi = True

                        col = cv.mean(raw, mask)
                        # col_im = np.zeros((1, 1, 3), np.uint8)
                        # col_im[0][0] = [col[0], col[1], col[2]]
                        # col_im = cv.cvtColor(col_im, cv.COLOR_BGR2HSV)
                        # col_im[0][0][2] = 255
                        # col_im = cv.cvtColor(col_im, cv.COLOR_HSV2BGR)
                        # col = col_im[0][0][0], col_im[0][0][1], col_im[0][0][2]
                        if DEBUG:
                            canny = cv.fillPoly(canny, [pts], (int(col[0]), int(col[1]), int(col[2])))

                        read.append((col[0], col[1], col[2]))
            if DEBUG:
                # cv.imshow('canny', canny)
                cv.imshow('scanning_areas', scanning_areas)

            # cv.waitKey()
            # exit(0)

            if olmadi:
                continue

            if not firstRead:
                firstRead = read
                firstDone = True
                if DEBUG:
                    cv.imshow('ilk okuma', canny)
                    cv.imshow('ilk okuma raw', raw)
            else:
                fark = 0
                for i in range(len(read)):
                    for j in range(3):
                        fark += (firstRead[i][j] - read[i][j])**2
                if fark > 270000:
                    secondRead = read
                    secondDone = True
                    reads = firstRead + secondRead
                    if DEBUG:
                        cv.imshow('ikinci okuma', canny)
                        cv.imshow('ikinci okuma raw', raw)
                        print(reads)

                    kumeler = [[], [], [], [], [], []]
                    reads = turnHSV(reads)
                    reads = reads[reads[:,1].argsort()]
                    for i in range(9):
                        kumeler[0].append(int(reads[i][3]))
                    reads = reads[9:]

                    reads = reads[reads[:,0].argsort()]
                    for j in range(1, 6):
                        for i in range(9):
                            kumeler[j].append(int(reads[(j-1)*9 + i][3]))

                    nerede = []
                    for i in range(54):
                        nerede.append(-1)
                    for i in range(6):
                        for j in range(9):
                            nerede[kumeler[i][j]] = i

                    kup = []
                    for i in range(54):
                        kup.append(-1)

                    doldur(kup, nerede[0:9], nerede[13])
                    doldur(kup, nerede[9:18], nerede[22])
                    doldur(kup, nerede[18:27], nerede[4])
                    doldur(kup, nerede[27:36], nerede[40])
                    doldur(kup, nerede[36:45], nerede[49])
                    doldur(kup, nerede[45:54], nerede[31])


                    enson = np.zeros((490 + 30, 650, 3), np.uint8)
                    
                    seperatorThickness = 2
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10
                            py = 10 + 150 + 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[9+i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10 + 150 + 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[18+i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10 + 150 + 10
                            py = 10 + 150 + 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[27+i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10 + 150 + 10 + 150 + 10
                            py = 10 + 150 + 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[36+i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)
                    for i in range(3):
                        for j in range(3):
                            px = 10 + 150 + 10
                            py = 10 + 150 + 10 + 150 + 10
                            enson = cv.rectangle(enson, (px + i*50, py + j*50), (px + (i+1)*50, py + (j+1)*50), getcolor(kup[45+i+j*3]), -1)
                            enson = cv.rectangle(enson, (px, py), (px + 100, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px + 50, py), (px + 150, py + 150), (0, 0, 0), seperatorThickness)
                            enson = cv.rectangle(enson, (px, py + 50), (px + 150, py + 100), (0, 0, 0), seperatorThickness)

                    cube_text = ''
                    c = 0
                    for j in range(3):
                        for i in range(3):
                            cube_text += str(kup[c])
                            c += 1
                        cube_text += '\n'
                    cube_text_1 = ''
                    cube_text_2 = ''
                    cube_text_3 = ''
                    for i in range(4):
                        cube_text_1 += str(kup[c])
                        c += 1
                        cube_text_1 += str(kup[c])
                        c += 1
                        cube_text_1 += str(kup[c])
                        c += 1
                        cube_text_2 += str(kup[c])
                        c += 1
                        cube_text_2 += str(kup[c])
                        c += 1
                        cube_text_2 += str(kup[c])
                        c += 1
                        cube_text_3 += str(kup[c])
                        c += 1
                        cube_text_3 += str(kup[c])
                        c += 1
                        cube_text_3 += str(kup[c])
                        c += 1
                    cube_text += cube_text_1 + '\n' + cube_text_2 + '\n' + cube_text_3 + '\n'
                    for j in range(3):
                        for i in range(3):
                            cube_text += str(kup[c])
                            c += 1
                        cube_text += '\n'
                    cube_text = cube_text.replace('0', 'W')
                    cube_text = cube_text.replace('1', 'R')
                    cube_text = cube_text.replace('2', 'O')
                    cube_text = cube_text.replace('3', 'Y')
                    cube_text = cube_text.replace('4', 'G')
                    cube_text = cube_text.replace('5', 'B')
                    
                    try:
                        clipboard.copy(cube_text)
                        enson = cv.putText(enson, 'Copied to clipboard! Press Enter to exit', (10, 510), cv.FONT_HERSHEY_SIMPLEX, 1, ((255, 255, 255)),)
                    except:
                        enson = cv.putText(enson, 'Press Enter to exit', (10, 510), cv.FONT_HERSHEY_SIMPLEX, 1, ((255, 255, 255)),)
                    

                    cv.imshow('raw', enson)
                    cv.waitKey()

                    exit(0)


        # cv.imshow('canny dilated', canny_d)


        # kose0 = topla((ax, ay), carp(200/length(cikar(p2[0], p1[0])), cikar(p2[0], p1[0])))
        # kose0 = int(kose0[0]), int(kose0[1])
        # canny = cv.circle(canny, kose0, 10, (0, 0, 255))
        
    if DEBUG:
        cv.imshow('canny', canny)
    else:
        cv.imshow('raw', raw)    

    key = cv.waitKey(20)
    if key == ord('q'):
        break