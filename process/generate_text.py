import sys, os
from fastai.vision import *
import cv2, glob
import json, string
import numpy as np
from multiprocessing import Process
import copy
from math import atan2, degrees

class Generate():
    def __init__(self, chars):
        self.chars = chars
        self.groups = []

        # Thresholds
        self.y_thresh = 0.2         # As a proprtion of char height
        self.x_thresh = 3           # As a proprtion of average char width
        self.theta_thresh = 20      # From center to center
        self.space_thresh = 1.5       # As a proprtion of char width

    def get_X_center(self, a):
        return a.x + (a.w // 2)

    def get_Y_center(self, a):
        return a.y + (a.h // 2)

    def get_X_thresh(self, a, b):
        return self.x_thresh * ((a.w + b.w) / 2.0)

    def get_space_thresh(self, a, b):
        return self.space_thresh * ((a.w + b.w) / 2.0)

    def are_joined(self, a, b):
        change_y = float( self.get_Y_center(b) - self.get_Y_center(a) )
        change_x = float( self.get_X_center(b) - self.get_X_center(a) )
        
        if change_x <= 0.0: return False

        theta = degrees(atan2(change_y, change_x))

        # print ("{} -> {}  {}".format(a.char, b.char, theta))
        
        if abs(theta) < self.theta_thresh and abs(change_x) <= self.get_X_thresh(a, b):
            return True
        return False


    def get_text(self):
        # Sort chars by x position
        self.chars.sort(key=lambda x: x.x)

        # Group chars if angle between and distance in X are both not too large
        for char in self.chars:
            found = False
            for group in self.groups:
                if self.are_joined(group[-1], char):
                    group.append(char)
                    found = True
                    break
            if not found: self.groups.append([char])

        # Sort groups by Y value
        self.groups.sort(key=lambda x: x[0].y)

        # Generate string
        text = ''
        for group in self.groups:
            text += group[0].char
            for i in range(1, len(group)):
                if abs(self.get_X_center(group[i]) - self.get_X_center(group[i-1])) > self.get_space_thresh(group[i-1], group[i]):
                    text += " "
                text += group[i].char
            text += "\n"

        return text
