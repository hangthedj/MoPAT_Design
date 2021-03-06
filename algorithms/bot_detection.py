#Rishi
import numpy as np
import cv2


image = cv2.imread('test.jpg',1)
(h,w,d) = image.shape
# print("width= {}, height = {} , depth = {} ".format(w,h,d))
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def center_finder(lower,upper,hsv):

    img = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((5,5), np.uint8)
    # img_blur=cv2.GaussianBlur(input_y,kernel,1)
    img_erosion = cv2.erode(img, kernel, iterations=3)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
    contours,__ = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("img",img_dilation)
    l=len(contours)
    centers =[]
    for i in range(l):
        center, _ = cv2.minEnclosingCircle(contours[i])
        c=[]
        for x in center:
            c.append(int(x))
        centers.append(c)
    return centers

def points_color(centers,color):
    dic={}
    for p in centers:
        dic[str(p[0]*w+p[1])]=color
    return dic

def arranger(points):
    i=0
    d=np.empty(3)
    for p in points:
        dist = np.square(p-points).sum()
        d[i]=dist
        i=i+1
    s = np.sort(d)
    a = np.where(d==s[1])
    r =points[a[0][0]]
    b = np.where(d==s[2])
    f=points[b[0][0]]
    c = np.where(d==s[0])
    l=points[c[0][0]]
    return f,l,r

def namer(a,b,c,color,w):
    return color[str(a[0]*w+a[1])] + color[str(b[0]*w+b[1])] + color[str(c[0]*w+c[1])]

def identifier(points,w,color):
    dic={}
    for p in points:
        d = np.square(p-points).sum(axis=1)
        s = np.sort(d)
        a = np.where(d==s[1])
        p1=points[a[0][0]]
        b = np.where(d==s[2])
        p2=points[b[0][0]]
        f,l,r=arranger(np.array([p,p1,p2]))
        name= namer(f,l,r,color,w)
        dic[name]=np.array([f,l,r])
    return dic

pt_color={}

lower_r = np.array([140,0,0], dtype = "uint8")
upper_r = np.array([200,255,255], dtype = "uint8")
centers_red = np.array(center_finder(lower_r,upper_r,hsv))
# print(centers_red)
pt_color.update(points_color(centers_red,"r"))

lower_b = np.array([100,0,0], dtype = "uint8")
upper_b = np.array([140,255,255], dtype = "uint8")
centers_blue = np.array(center_finder(lower_b,upper_b,hsv))
# print(centers_blue)
pt_color.update(points_color(centers_blue,"b"))

lower_g = np.array([40,0,0], dtype = "uint8")
upper_g = np.array([100,255,255], dtype = "uint8")
centers_green = np.array(center_finder(lower_g,upper_g,hsv))
# print(centers_green)
pt_color.update(points_color(centers_green,"g"))

# print(pt_color)

all_centers= np.concatenate((centers_blue,centers_red,centers_green))
# print(all_centers)

print(identifier(all_centers,w,pt_color))
