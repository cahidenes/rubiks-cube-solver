import cv2 as cv
import numpy as np
import random

cam = cv.VideoCapture(0)

eps = 0.00001
W, H = cam.get(cv.CAP_PROP_FRAME_WIDTH), cam.get(cv.CAP_PROP_FRAME_HEIGHT)

firstRead = []
secondRead = []

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
        arr[i] = [(float(tmp[0][i][0] + 30) % 180), float(tmp[0][i][1]), float(tmp[0][i][2])]
    return np.array(arr)

while True:
    isTrue, raw = cam.read()
    if isTrue == False:
        break

    raw = cv.flip(raw, 1)

    cv.imshow('raw', raw)

# --------------------------- Hue Saturation Value --------------------------- #

    # hsv = cv.cvtColor(raw, cv.COLOR_BGR2HSV)

    # hue = hsv[:, :, 0]
    # saturation = hsv[:, :, 1]
    # value = hsv[:, :, 2]
    # comp = hsv.copy()

    # value_d = value.copy()
    # value_d[:, :] = 255
    # value_d[value < 250] = 250
    # value_d[value < 200] = 200
    # value_d[value < 150] = 150
    # value_d[value < 100] = 100
    # value_d[value < 50] = 50

    # saturation_d = saturation.copy()
    # saturation_d[:, :] = 225
    # saturation_d[saturation < 200] = 175
    # saturation_d[saturation < 150] = 125
    # saturation_d[saturation < 100] = 75
    # saturation_d[saturation < 50] = 0

    # hue_d = hue.copy()
    # hue_d[:, :] = 0
    # hue_d[hue < 148] = 117
    # hue_d[hue < 91] = 60
    # hue_d[hue < 40] = 25
    # hue_d[hue < 19] = 15
    # hue_d[hue < 10] = 0

    # comp = np.array([hue_d, saturation_d, value_d])
    # comp = np.moveaxis(comp, [0, 1, 2], [2, 0, 1])
    
    # # comp = np.concatenate((hue, saturation, value), axis=1)
    # # print(comp.shape)
    # # comp[:, :] = [hue[:, :], value[:, :], saturation[:, :]]
    # # comp[saturation<100][1] = 0
    # # comp[saturation>=100][1] = 255
    # # for i in comp:
    # #     for j in i:
    # #         if j[2] < 55:
    # #             j[2] = 0
    #         # if j[1] < 100: 
    #         #     j[1] = 0
    #         # else:
    #         #     j[1] = 255
    # comp = cv.cvtColor(comp, cv.COLOR_HSV2BGR)
    # cv.imshow('comp', comp)


# ------------------------------ Edge Detection ------------------------------ #
    raw = cv.medianBlur(raw, 7)

    canny = cv.Canny(raw, 90, 200)
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

    canny = cv.polylines(canny, [pts], True, (0, 255, 0), 3)
    canny = cv.line(canny, (885, 200), (675, 342), (0, 255, 0), 3)
    canny = cv.line(canny, (675, 571), (675, 342), (0, 255, 0), 3)
    canny = cv.line(canny, (454, 211), (675, 342), (0, 255, 0), 3)
    alan = area(pts)
    # print(alan)

    canny = cv.circle(canny, (675, 342), 30, (0, 0, 255))
    canny = cv.circle(canny, (675, 342), 50, (0, 0, 255))

    p1 = []
    p2 = []

    points = cv.ellipse2Poly((675, 342), (30, 30), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            # canny = cv.circle(canny, (x, y), 5, (255, 0, 0))
            if len(p1) == 0 or dist((x, y), p1[-1]) > 10:
                p1.append((x, y))

    points = cv.ellipse2Poly((675, 342), (50, 50), 0, 0, 360, 1)
    for (x, y) in points:
        if canny_gray[y, x] == 255:
            # canny = cv.circle(canny, (x, y), 5, (255, 0, 0))
            if len(p2) == 0 or dist((x, y), p2[-1]) > 10:
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

        # print(x1, y1)
        # print(x2, y2)
        # print(x3, y3)
        # print(x4, y4)

        ax = (x3*(y4-y3)/(x4-x3) - x1*(y2-y1)/(x2-x1) + y1 - y3)/((y4-y3)/(x4-x3) - (y2-y1)/(x2-x1))
        ay = (ax-x1)*(y2-y1)/(x2-x1) + y1

        if ax > 100000 or ay > 100000:
            continue

        center = int(ax), int(ay)
        if 0 < ax < 1000 and 0 < ay < 1000:
            canny = cv.circle(canny, center, 5, (255, 255, 0), -1)
        
        canny_d = cv.dilate(canny, None)
        canny_d = cv.dilate(canny_d, None)
        canny_d = cv.dilate(canny_d, None)
        canny_d = cv.dilate(canny_d, None)
        canny_d = cv.dilate(canny_d, None)

        dx, dy = p2[0][0] - p1[0][0], p2[0][1] - p1[0][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx1, ky1 = p2[0][0], p2[0][1]
        while 0 < kx1 < W and 0 < ky1 < H:
            if canny_d[int(ky1), int(kx1)].all() == 0:
                break
            kx1 += dx
            ky1 += dy
        kx1 -= 5*dx
        ky1 -= 5*dy

        dx, dy = p2[1][0] - p1[1][0], p2[1][1] - p1[1][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx2, ky2 = p2[1][0], p2[1][1]
        while 0 < kx2 < W and 0 < ky2 < H:
            if canny_d[int(ky2), int(kx2)].all() == 0:
                break
            kx2 += dx
            ky2 += dy
        kx2 -= 5*dx
        ky2 -= 5*dy

        dx, dy = p2[2][0] - p1[2][0], p2[2][1] - p1[2][1]
        dx, dy = dx/length((dx, dy)), dy/length((dx, dy))
        kx3, ky3 = p2[2][0], p2[2][1]
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

        canny = cv.circle(canny, k1, 10, (0, 0, 255))
        canny = cv.circle(canny, k2, 10, (0, 0, 255))
        canny = cv.circle(canny, k3, 10, (0, 0, 255))

        kk1 = topla(cikar(k1, center), k2)
        kk2 = topla(cikar(k2, center), k3)
        kk3 = topla(cikar(k3, center), k1)

        kk1 = cikar(kk1, carp(0.16, cikar(kk1, center)))
        kk2 = cikar(kk2, carp(0.16, cikar(kk2, center)))
        kk3 = cikar(kk3, carp(0.16, cikar(kk3, center)))
        kk1 = (int(kk1[0]), int(kk1[1]))
        kk2 = (int(kk2[0]), int(kk2[1]))
        kk3 = (int(kk3[0]), int(kk3[1]))
        
        calculated_area = area([k1, kk1, k2, kk2, k3, kk3])

        error = abs(calculated_area - alan)/alan

        if error < 0.2:
            canny = cv.circle(canny, kk1, 10, (0, 0, 255))
            canny = cv.circle(canny, kk2, 10, (0, 0, 255))
            canny = cv.circle(canny, kk3, 10, (0, 0, 255))

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

                        b1 = cikar(b1, carp(0.16*min(i  , j  )/3, cikar(b1, center)))
                        b2 = cikar(b2, carp(0.16*min(i+1, j  )/3, cikar(b2, center)))
                        b3 = cikar(b3, carp(0.16*min(i  , j+1)/3, cikar(b3, center)))
                        b4 = cikar(b4, carp(0.16*min(i+1, j+1)/3, cikar(b4, center)))

                        mask = np.zeros(canny.shape, np.uint8)

                        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

                        pts = np.array([
                            [b1[0], b1[1]], 
                            [b2[0], b2[1]], 
                            [b4[0], b4[1]],
                            [b3[0], b3[1]]
                            ], np.int32)

                        pts.reshape((-1, 1, 2))
                        # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        mask = cv.fillPoly(mask, [pts], (255, 255, 255))

                        mask = cv.erode(mask, None)
                        mask = cv.erode(mask, None)
                        mask = cv.erode(mask, None)

                        col = cv.mean(raw, mask)
                        # col_im = np.zeros((1, 1, 3), np.uint8)
                        # col_im[0][0] = [col[0], col[1], col[2]]
                        # col_im = cv.cvtColor(col_im, cv.COLOR_BGR2HSV)
                        # col_im[0][0][2] = 255
                        # col_im = cv.cvtColor(col_im, cv.COLOR_HSV2BGR)
                        # col = col_im[0][0][0], col_im[0][0][1], col_im[0][0][2]

                        canny = cv.fillPoly(canny, [pts], (int(col[0]), int(col[1]), int(col[2])))

                        read.append((col[0], col[1], col[2]))
            # cv.imshow('canny', canny)

            # cv.waitKey()
            # exit(0)

            if not firstRead:
                firstRead = read
                cv.imshow('ilk okuma', canny)
                cv.imshow('ilk okuma raw', raw)
            else:
                fark = 0
                for i in range(len(read)):
                    for j in range(3):
                        fark += (firstRead[i][j] - read[i][j])**2
                if fark > 270000:
                    secondRead = read
                    cv.imshow('ikinci okuma', canny)
                    cv.imshow('ikinci okuma raw', raw)
                    print(firstRead + secondRead)
                    reads = firstRead + secondRead

                    kumeler = [[], [], [], [], [], []]
                    reads = turnHSV(reads)
                    reads = reads[reads[:,1].argsort()]
                    print(reads)
                    for i in range(9):
                        kumeler[0].append(reads[i])
                    reads = reads[9:]

                    reads = reads[reads[:,0].argsort()]
                    for j in range(1, 6):
                        for i in range(9):
                            kumeler[j].append(reads[(j-1)*9 + i])

                    enson = np.zeros((600//2, 1500//2, 3), np.uint8)
                    for i in range(6):
                        for j in range(len(kumeler[i])):
                            enson = cv.rectangle(enson, (j*50, i*50), ((j+1)*50, (i+1)*50), (int(kumeler[i][j][0]), int(kumeler[i][j][1]), int(kumeler[i][j][2])), -1)

                    for i in enson:
                        for j in i:
                            j[0] = (j[0] + 150) % 180
                    enson = cv.cvtColor(enson, cv.COLOR_HSV2BGR)
                    cv.imshow('cikti', enson)
                    cv.waitKey()

                    exit(0)


        # cv.imshow('canny dilated', canny_d)


        # kose0 = topla((ax, ay), carp(200/length(cikar(p2[0], p1[0])), cikar(p2[0], p1[0])))
        # kose0 = int(kose0[0]), int(kose0[1])
        # canny = cv.circle(canny, kose0, 10, (0, 0, 255))
        
    cv.imshow('canny', canny)

# --------------------------------- Contours --------------------------------- #

    # hue_white = hue.copy()
    # hue_white[saturation < 50] = 255
    # cv.imshow('hue_white', hue_white)
    # contours, hierarchy = cv.findContours(hue, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # thresh = 100
    # for i in range(len(contours)-1, -1, -1):
    #     if len(contours[i]) < thresh:
    #         contours = np.delete(contours, i)        
            
    # deneme = np.zeros((raw.shape), dtype=np.uint8)
    # cv.drawContours(deneme, contours, -1, (255, 255, 255))
    # cv.drawContours(deneme, contours, -1, (255, 255, 255), 3)
    # cv.imshow('deneme', deneme)

    # # corner = cv.medianBlur(raw, 5)
    # # corner = cv.cvtColor(corner,cv.COLOR_BGR2GRAY)
    # corner = np.float32(deneme)
    # dst = cv.cornerHarris(corner,11,21,0.04)

    # raw[dst>0.02*dst.max()]=[0,0,255]

    #result is dilated for marking the corners, not important
    # dst = cv.dilate(dst, np.ones((5, 5), dtype=np.uint8))
    # Threshold for an optimal value, it may vary depending on the image.
    # dst[dst>0.01*dst.max()]=[0,0,255]
    cv.imshow('raw', raw)
    

    key = cv.waitKey(20)
    if key == ord('q'):
        break