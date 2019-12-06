#import os
#os.environ["CUDA_VISIBLE_DEVICES"]="2"

import cv2
import torch
import os
from process.detect import Detect
from process.classifier import Classifier
from process.generate_text import Generate
import datetime as dt



roi_dir='/mnt/ssd_data/ocr_dev/roi_collection/'
draw_path='/mnt/ssd_data/ocr_dev/random_tiff/'
output_path='/mnt/ssd_data/ocr_dev/output/'
pkl_input_path='/mnt/ssd_data/ocr_dev/for_US/'
pkl_file_name ='export.pkl'

class ProcessIMG:

    def __init__(self, input_path, roi_dir, image_name, output_path, draw_lines=False, draw_detections=False, resize_img=True):
        self.input_path = input_path
        self.roi_dir=roi_dir
        self.image_name=image_name
        self.output_path=output_path
        self.draw_lines = draw_lines
        self.draw_detections = draw_detections
        self.resize_img = resize_img
        self.image_text = None

        if self.resize_img: self.annotated_img = self.resize_drawing(cv2.imread(self.input_path))
        else: self.annotated_img = cv2.imread(self.input_path)

        self.process()

    def resize_drawing(self, image):
        # TODO: Move to init
        target_width = 7021
        sf = float(target_width) / float(image.shape[1])
        h = int(sf * image.shape[0])
        return cv2.resize(image, (target_width, h), interpolation=cv2.INTER_AREA)

    def process(self):
        print ("Detecting contours")
        D = Detect(self.input_path, self.roi_dir, self.image_name, self.output_path, resize_img=self.resize_img)
        detections = D._find_chars()
        chars_found = []

        print("Classifying contours")
        for i, D in enumerate(detections):
            C = Classifier(D.img, pkl_input_path, pkl_file_name)
            char = C.classify()
            if char is not None:
                D.char = char
                chars_found.append(D)

            if self.draw_detections:
                cv2.rectangle(self.annotated_img,(max(D.x -1,0), max(D.y -1, 0)),(D.x + D.w +1, D.y + D.h +1),(255,0,0),1)

        print("Generating text")
        G = Generate(chars_found)
        self.image_text = G.get_text()

        print ("Annotating image")
        font = cv2.FONT_HERSHEY_SIMPLEX
        for C in chars_found:
            cv2.rectangle(self.annotated_img,(C.x, C.y),(C.x + C.w, C.y + C.h),(0,255,0),1)
            cv2.putText(self.annotated_img, C.char, (C.x, C.y), font, .6, (0, 0, 255), 1, cv2.LINE_AA)
        
        if self.draw_lines:
            for group in G.groups:
                for i in range(1,len(group)):
                    x1 = group[i-1].x + (group[i-1].w // 2)
                    y1 = group[i-1].y + (group[i-1].h // 2)

                    x2 = group[i].x + (group[i].w // 2)
                    y2 = group[i].y + (group[i].h // 2)

                    if abs(group[i-1].x - group[i].x) < 5 * group[i].w:
                        cv2.line(self.annotated_img,(x1,y1),(x2,y2),(255,255,0),1)


def main():
    start = dt.datetime.now()
    USE_CUDA = torch.cuda.is_available()

    device = torch.device("cuda" if USE_CUDA else "cpu")
    print("Running OCR Process Image Using " + "Device Name:" + str(device))

    ## Get Id of default device
    #print("DEFAULT GPU DEVICE ID = " + str(torch.cuda.current_device()))

    # Returns the current GPU memory usage by
    # tensors in bytes for a given device
    #print("GPU Memory Usage = " + str(torch.cuda.memory_allocated()))

    # Returns the current GPU memory managed by the
    # caching allocator in bytes for a given device
    #print("GPU Memory by Caching Allocator = " + str(torch.cuda.memory_cached()))

    # Releases all unoccupied cached memory currently held by
    # the caching allocator so that those can be used in other
    # GPU application and visible in nvidia-smi
    torch.cuda.empty_cache()

    # Returns the current GPU memory usage by
    # tensors in bytes for a given device
    #print("GPU Memory usage by Tensors = " + str(torch.cuda.memory_allocated()))

    all_images=[]
    
    for subdir, dirs, files in os.walk(draw_path):
        for file in files:
            if file.startswith(".DS_Store") or file.startswith("models"):
                pass
            else:
                list_of_images=os.path.join(subdir, file)
                all_images.append(list_of_images)
            
    
    for drawing in all_images:
        start = dt.datetime.now()

        input_image_path = drawing
        image_name=os.path.splitext(os.path.basename(drawing))[0]
        output_image_path = output_path+image_name+'_out.png'
        text_output_path = output_path+image_name+'_out.txt'

        print(drawing)
        
        P = ProcessIMG(input_image_path, roi_dir, image_name, output_path, draw_detections=True, draw_lines=False, resize_img=False)
        cv2.imwrite(output_image_path, P.annotated_img)
        
        print(P.image_text)
        
        with open(text_output_path, 'w') as f:
            f.write(P.image_text)
            end = dt.datetime.now()
            duration = end - start
            print("Stored the output:" + str(output_image_path))
            print("Completed OCR Process Image in {}".format(duration))
    end = dt.datetime.now()
    duration = end - start
    
    '''
    P = ProcessIMG(input_image_path, roi_dir, image_name, draw_detections=True, draw_lines=True, resize_img=False)
    cv2.imwrite(output_image_path, P.annotated_img)
    #print(P.image_text)

    with open(text_output_path, 'w') as f:
        f.write(P.image_text)
        end = dt.datetime.now()
        duration = end - start
        print("Stored the output:" + str(output_image_path))
        print("Completed OCR Process Image in {}".format(duration))'''


if __name__ == '__main__':
    main()
