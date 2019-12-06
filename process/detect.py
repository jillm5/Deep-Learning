import sys, os
from fastai.vision import *
import cv2, glob
import json, string
import numpy as np
import itertools

class Char():
    def __init__(self, img=None, x=None, y=None, w=None, h=None):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.char = None
        self.code = None


class Detect():
    def __init__(self, img_path, roi_dir, image_name, output_path, resize_img=False, show_progress=True ):
        self.detections = []
        self.img_path = img_path
        self.roi_dir=roi_dir
        self.image_name=image_name
        self.output_path=output_path
        self.resize_img = resize_img
        self.show_progress = show_progress
        

    def is_contour_small(self, c):
        # approximate the contour
        x,y,w,h = cv2.boundingRect(c)
        return w<100 and h<140

    def is_rect_overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if x1 < x2 < (x1+w1) and (x2+w2) < (x1+w1) and y1 < y2 < (y1+h1) and (y2+h2) < (y1+h1):
            return True

    def is_rect_overlap(self, a, b):
        if a[0] < b[0] < (a[0]+a[2]) and (b[0]+b[2]) < (a[0]+a[2]) and a[1] < b[1] < (a[1]+a[3]) and (b[1]+b[3]) < (a[1]+a[3]):
            return True
        return False

    def resize_drawing(self, image):
        # TODO: Move to init
        target_width = 7021
        sf = float(target_width) / float(image.shape[1])
        h = int(sf * image.shape[0])
        return cv2.resize(image, (target_width, h), interpolation=cv2.INTER_AREA)

    def _find_chars(self):
        if not os.path.exists(self.img_path): print ("ERROR: Could not find file at: {}".format(self.img_path))

        image = cv2.imread(self.img_path)
        image_o = cv2.imread(self.img_path)
        if self.resize_img:
            assert image.shape[1] >= image.shape[0], "Image width cannot be smaller than height."
            image = self.resize_drawing(image)
            image_o = self.resize_drawing(image_o)
        
        #convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        #find optimal threshold
        ret,thresh = cv2.threshold(gray, 0, 255,cv2.cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

        # Remove horizontal and vertical lines

        # Defining a kernel length
        kernel_h = np.array(image).shape[1] // 60
        
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_h, 1))

        # Remove horizontal
        detected_h_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, hori_kernel, iterations=2)

        # detect vertical lines
        kernel_v = np.array(image).shape[0] // 40

        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_v))
    
        detected_v_lines= cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)


        cnts_h = cv2.findContours(detected_h_lines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        cnts_h = cnts_h[0] if len(cnts_h) == 2 else cnts_h[1]

        cnts_v = cv2.findContours(detected_v_lines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        cnts_v = cnts_v[0] if len(cnts_v) == 2 else cnts_v[1]

        cnts=np.append(cnts_h, cnts_v)
        
        
        im2 = image.copy()

        for c in cnts:
            try:
                cv2.drawContours(im2, [c], -1, (255,255,255), 2)
            except:
                print(self.img_path)
                continue
    
        # Repair image
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
        result = 255 - cv2.morphologyEx(255 - im2, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
        #convert image to grayscale
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) # the optimal setting for distinguishin I after T in Sensitive
        #smooth_e = cv2.erode(result, kernel, iterations=1) 
        #blur = cv2.GaussianBlur(smooth_e,(3,3),5,0)

        #smooth = cv2.addWeighted(blur,3.5,img,-0.5,0)
        #smooth = cv2.addWeighted(smooth_e,20,image,-5,0)
        
                
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) 

        #find optimal threshold
        ret,thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS )
        

        all_rects=[]
        cnts_f=[]
        
        im2=image.copy()
        
        #apply padding along the width
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if hierarchy[0,i,3] ==-1 :
                x, y, w, h = cv2.boundingRect(cnt)
                
                #if w<100 and h<100:
                all_rects.append((x-1,y-1,w+2,h+2))
                cnts_f.append(cnt)
                im3=cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)  
        
        cv2.imwrite(self.output_path+self.image_name+'detections.png', im3) 
        
        print ("Found {} contours.".format(len(cnts_f)))
        

        # for c in cnts:
        #     if self.is_contour_small(c):
        #         cv2.drawContours(image, [c], -1, (128,255,0), 3)

        # loop over the contours to make rectangles


        overlap_rects = []
        for a, b in itertools.combinations(all_rects, 2):
            if self.is_rect_overlap(a, b):
                overlap_rects.append([b[0],b[1],b[2],b[3]])

        char_rects = []
        for x in all_rects:
            if x not in overlap_rects:
                char_rects.append(x)

        for i, rect in enumerate(char_rects):
            if self.show_progress:
                printProgressBar(i, len(char_rects) -1)
            
            C = Char(x=rect[0], y=rect[1], w=rect[2], h=rect[3])
            img = image_o[np.max([C.y-5,0]):C.y+C.h,C.x:C.x+C.w,:]
            try:
                C.img = cv2.resize(img, (80, 80))
                yield C
            except:
                pass
        
        '''#extract and save each ROI for trainining AI
        im6 = image.copy()
        ROI_number = 0
        for i, cnt in enumerate(cnts_f):
            x, y, w, h = cv2.boundingRect(cnt)
            x_n=x-1
            y_n=y-1
            #cv2.rectangle(im6, (x-1, y-1), (x + w+2, y + h+2), (0, 255, 0), 2)        
            ROI = im6[y_n:y+h+2, x_n:x+w+2]
            try:
                os.mkdir(self.roi_dir+self.image_name+'/')
            except FileExistsError:
                pass
            cv2.imwrite(self.roi_dir+self.image_name+'/'+'ROI_{}.png'.format(ROI_number), ROI)
            ROI_number += 1
        
        #extract and save each context ROI - ROI with padding
        
        im6 = image.copy()
        ROI_number = 0
        for i, cnt in enumerate(cnts_f):
            x, y, w, h = cv2.boundingRect(cnt)
            x_n=x-1
            y_n=y-1
            #cv2.rectangle(im6, (x-1, y-1), (x + w+2, y + h+2), (0, 255, 0), 2)        
            ROI = im6[y_n:y+h+2, x_n:x+w+10]
            cv2.imwrite(self.roi_dir+self.image_name+'/'+'ROI_c_{}.png'.format(ROI_number), ROI)
            ROI_number += 1
'''

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s - %s/%s' % (prefix, bar, percent, suffix, iteration, total), end = '\r')
    if iteration == total: print()
