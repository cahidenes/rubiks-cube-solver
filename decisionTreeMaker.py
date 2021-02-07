file = open('in2')
arr = []
for i in range(480):
    arr.append(file.readline().strip())

def top(a, l):
    s = 0
    for i in l:
        s += int(a[i])
    return s

def get(a):
    if a == 0:
        return "U"
    elif a == 1:
        return "U1"
    elif a == 2:
        return "U2"
    elif a == 3:
        return "D"
    elif a == 4:
        return "D1"
    elif a == 5:
        return "D2"
    elif a == 6:
        return "R"
    elif a == 7:
        return "R1"
    elif a == 8:
        return "R2"
    elif a == 9:
        return "L"
    elif a == 10:
        return "L1"
    elif a == 11:
        return "L2"
    elif a == 12:
        return "F"
    elif a == 13:
        return "F1"
    elif a == 14:
        return "F2"
    elif a == 15:
        return "B"
    elif a == 16:
        return "B1"
    elif a == 17:
        return "B2"

def find(nums):

    # print("nums: ", nums)

    if len(nums) == 1:
        print("return cube." + get(nums[0]) + ', "' + get(nums[0])+ '"')
        return

    secilen = -1
    for i in range(480):
        if top(arr[i], nums) == len(nums)//2 or top(arr[i], nums) == len(nums) - len(nums)//2:
            secilen = i
    if secilen == -1:
        for i in range(480):
            if top(arr[i], nums) == len(nums)//2 - 1 or top(arr[i], nums) == len(nums) - len(nums)//2 + 1:
                secilen = i
    if secilen == -1:
        print("haydaaa secilen yokkk")
        exit(0)

    # print("secilen: ", secilen)
    # print(arr[secilen])

    nums0 = []
    nums1 = []
    for i in nums:
        if arr[secilen][i] == '1':
            nums1.append(i)
        else:
            nums0.append(i)
    print("if doTest(cube, %d) == true {" % secilen)
    find(nums1)
    print("} else {")
    find(nums0)
    print("}")

find([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

    