
#Fuzzy Control Systems

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

f = open('rules.txt', 'r')
lines = f.readlines()
rules = []
for l in lines:
    li = l.split(" ")
    l = [li[0], li[1], li[2].strip("\n")]
    rules.append(l)
    
'''
print("original rules: ")
for i in rules:
    print(i)
'''
    
def triangle(a, b, c, x):
  v1 = (x-a)/(b-a)
  v2 = (c-x)/(c-b)
  return max(min(v1, v2), 0)
def trapezoid(a, b, c, d, x):
  v1 = (x-a)/(b-a)
  v2 = (d-x)/(d-c)
  return max(min(v1, v2, 1), 0)

def calcFuzzy(l, inp):
  if l[0] == "triangle":
    return triangle(l[1], l[2], l[3], inp)
  else:
    return trapezoid(l[1], l[2], l[3], l[4], inp
                     )
values={'NL':['trapezoid', 0, 0, 31, 61],
        'NM':['triangle', 31, 61, 95],
        'NS':['triangle', 61, 95, 127],
        'ZE':['triangle', 95, 127, 159],
        'PS':['triangle', 127, 159, 191],
        'PM':['triangle', 159, 191, 223],
        'PL':['trapezoid', 191, 223, 255, 255]}

throttle = {'NL': (0, 31, 61), 'NM': (31, 61, 95), 'NS': (61, 95, 127),
            'ZE': (95, 127, 159), 'PS': (127, 159, 191), 'PM': (159, 191, 223),'PL': (191, 223, 255)}

#####################################################

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect = 45)
ax1.set_xlim(0, 260)
ax1.set_ylim(0, 2)

pNL = [[0, 0], [0, 1], [31, 1], [63, 0]]
polygon= plt.Polygon(pNL,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pNM = [[31, 0], [63, 1], [95, 0]]
polygon= plt.Polygon(pNM,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pNS = [[63, 0], [95, 1], [127, 0]]
polygon= plt.Polygon(pNS,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pZE = [[95, 0], [127, 1], [159, 0]]
polygon= plt.Polygon(pZE,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pPS = [[127, 0], [159, 1], [191, 0]]
polygon= plt.Polygon(pPS,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pPM = [[159, 0], [191, 1], [223, 0]]
polygon= plt.Polygon(pPM,  fill=None, edgecolor='r')
ax1.add_patch(polygon)


pPL = [[191, 0], [223, 1], [255, 1], [255, 0]]
polygon= plt.Polygon(pPL,  fill=None, edgecolor='r')
ax1.add_patch(polygon)

x = [31, 63, 95, 127, 159, 191, 223]
y = [1]*7

annotations = ["NL", "NM", "NS", "ZE", "PS", "PM", "PL"]
ax1.scatter(x, y, s=20)

for xi, yi, text in zip(x, y, annotations):
    ax1.annotate(text,
                xy=(xi, yi), xycoords='data',
                xytext=(1.5, 1.5), textcoords='offset points')
#plt.show() 

#####################################################

#sd = int(input("Enter value for speed difference : "))
#acc = int(input("Enter value for acceleration : "))
sd=100
acc=70

speedFuzzyval = 1
accFuzzyval = 1

speedFuzzyList =[]
accFuzzyList =[]

finalFuzzyOp = float('-inf')
opLabel = ''

final = {}

for k in values.keys():
    if sd >= values[k][1] and sd <= values[k][-1]:
        speedFuzzyval = min(speedFuzzyval, calcFuzzy(values[k], sd))
        speedFuzzyList.append(k)

for k in values.keys():
    if acc >= values[k][1] and acc <= values[k][-1]:
        accFuzzyval = min(accFuzzyval, calcFuzzy(values[k], acc))
        accFuzzyList.append(k)
            
for i in rules:
    if i[0] in speedFuzzyList:
        i[0] = speedFuzzyval
    else:
        i[0] = 0
    if i[1] in accFuzzyList:
        i[1] = accFuzzyval
    else:
        i[1] = 0

for i in rules:
    opLabel = i[2]
    i[2] = min(i[0], i[1])
    finalFuzzyOp = max(finalFuzzyOp, i[2])
    final[opLabel] = i[2]

    
print("Fuzzy Speed Value : ", speedFuzzyval)
print("Fuzzy Acceleration Value : ", accFuzzyval)
    
print("Final Fuzzy o/p : ", finalFuzzyOp)

print("final : ", final)


x1 = [0, 260]
y1 = [finalFuzzyOp, finalFuzzyOp]
#plt.show()


line1 = Line2D(x1, y1, color='b')
ax1.add_line(line1) 

hLine = [(0, finalFuzzyOp), (260, finalFuzzyOp)]

def findIntersection(line1, line2):
    # l1 = [(x1, y1), (x2, y2)]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

def find_area(array):
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    return a/2
                  

pnts = []
poly =[]
for i in final.keys():
    if final[i] != 0:
        #print(i, final[i])
        #print(i, values[i])
        if len(values[i])==4:
            line1 = [(values[i][1], 0), (values[i][2], 1)]
            line2 = [(values[i][2], 1), (values[i][3], 0)]
            
            ipPoints1 = findIntersection(line1, hLine )
            ipPoints2 = findIntersection(line2, hLine )
            poly.append([values[i][1], 0])
            poly.append(ipPoints1)
            poly.append(ipPoints2)
            poly.append([values[i][3], 0])
        pnts.append(poly)
        poly = []

print(sorted(pnts, key=lambda x: (x[0])))

for i in pnts:
    polygon= plt.Polygon(i,  fill='pink', edgecolor='r')
    ax1.add_patch(polygon)

plt.show()

for i in pnts:
    print(find_area(i))

'''
Weighted Average Method
		x = ∑ µ(X) . x / ∑ µ(X) 
'''
