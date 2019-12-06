import sys, os
from fastai.vision import *
import cv2, glob
from multiprocessing import Process


class Classifier():
    def __init__(self, img, pkl_input_path, pkl_file_name, return_nc=False):
        self.return_nc = return_nc
        self.raw_img = cv2.resize(img, (80, 80))
        self.pkl_input_path = pkl_input_path
        self.pkl_file_name = pkl_file_name
        # TODO: convert to black and white
        
        self.img = Image(pil2tensor(self.raw_img, dtype=np.float32).div_(255))

        classes = ['black', 'grizzly', 'teddys']

        #self.learn = load_learner('')
        
        self.learn = load_learner(self.pkl_input_path, self.pkl_file_name)

        self.char_map = json.loads(open(os.path.join(self.pkl_input_path, 'map.json')).read())
        self.char_map_rev = {}
        for char in self.char_map: self.char_map_rev[self.char_map[char]] = char


    def classify(self):
        
        self.pred_class, pred_idx, outputs = self.learn.predict(self.img)
        if str(self.pred_class) != 'NC' or self.return_nc or str(self.pred_class) != 'mu': #these are folders which have noise images for exclusion
            #char = self.char_map_rev[str(self.pred_class)]
            char = self.char_map_rev[str(self.pred_class )]
            return char.upper()


    def get_code(self):
        return str(self.pred_class)
