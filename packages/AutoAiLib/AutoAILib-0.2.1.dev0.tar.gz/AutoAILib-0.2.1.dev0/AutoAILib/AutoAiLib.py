# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:35:27 2019

@author: matth
"""
import os
import random
import shutil
from img_transform import transform_many
import progressbar
import pandas as pd
from keras import models as m
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2

def check_right(row):
    if row['file'] == row['prediction']:
        return 'Correct'
    else:
        return 'Incorrect'
  
def manual_test(model, testing_dir, labels):
    print("Testing")
    #model should be a path to the model, testing_dir is the directory which contains all your testing images/classes, labels
    #should be a dictionary of the classes, in form (index:class_name).
    
    classes = os.listdir(testing_dir)
    if type(model) == str:
        #If the model is a path, open it
        model = m.load_model(model)
    else:
        #else its an object
        model = model
    #Fetches the classes of the testing directory
    sub_dirs = [os.path.join(testing_dir, x) for x in classes]
    all_files = list()
    predictions = list()
    
    print(labels)
    
    for d in sub_dirs:
        files_in_path = os.listdir(d)
        
        for f in files_in_path:
            img_path = os.path.join(d, f)
            img_name = d.split('\\')[-1] + '/' +  f
            image = cv2.imread(img_path)
            all_files.append(img_name)
            image = cv2.resize(image, (150,150))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            
            pred = model.predict(image)
            choice = np.argmax(pred)
            pred = labels[choice]
            predictions.append(pred)    
        
    
    
    all_files = [i.split('/')[0] for i in all_files]
    results = pd.DataFrame({'file' : all_files, 'prediction' : predictions})
    results['correct/incorrect'] = results.apply(lambda row : check_right(row), axis =1)
    grouping = results.groupby(['file', 'correct/incorrect'], as_index=False).count()
    results = pd.concat([results, grouping], axis = 1)
    os.chdir(os.path.dirname(testing_dir))
    p = os.path.dirname(testing_dir)
    if 'results.csv' in os.listdir(p):
        name = 'results_' + str(len(os.listdir(p)) + 1) + '.csv'
        results.to_csv(os.path.join(p, name), index= False)
    else:
        name =  "results.csv"
        results.to_csv(os.path.join(p, name), index = False)
        
    print("[" + name + '] created')
    return









def compile_data(src, dest, num_imgs_per_class = 0, train_ratio = .7, validation_ratio = .2, test_ratio = .1):
    #Given the original data directory this script creates the
    #directories, transforms images (if provided a number of imgs to generate for each class)
    # and places them in the destination folders.
       
    create_dirs(dest, src)
    
    if num_imgs_per_class:
        
        transform_many(src, num_imgs_per_class)
    
    place_images(dest, src, train=train_ratio, validation = validation_ratio, test = test_ratio)
        



def create_dirs(ROOT_DIR, original_data_dir):
    
    dirs = os.listdir(original_data_dir)
    train_dir= os.path.join(ROOT_DIR, 'train')
    test_dir = os.path.join(ROOT_DIR, 'test')
    validate_dir = os.path.join(ROOT_DIR, 'validation')
    
    if not os.path.isdir(train_dir):
        os.mkdir(train_dir)
    if not os.path.isdir(test_dir):    
        os.mkdir(test_dir)
    if not os.path.isdir(validate_dir):
        os.mkdir(validate_dir)
    
    for fname in dirs:
        p = os.path.join(test_dir, fname)
        if not os.path.isdir(p):
            os.mkdir(p)
            
    for fname in dirs:
        p = os.path.join(train_dir, fname)
        if not os.path.isdir(p):
            os.mkdir(p)
            
    for fname in dirs:
        p = os.path.join(validate_dir, fname)
        if not os.path.isdir(p):
            os.mkdir(p)
    
        
def place_images(ROOT_DIR, original_data_dir, train=.7, validation=.2, test=.1):
    
    dirs = os.listdir(original_data_dir)
    train_dir= os.path.join(ROOT_DIR, 'train')
    test_dir = os.path.join(ROOT_DIR, 'test')
    validate_dir = os.path.join(ROOT_DIR, 'validation')
    bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
    total = 0
    counter = 0
    for dname in dirs:
        
        new_dir = os.path.join(original_data_dir, dname)
        dest_dir = ''
        all_pictures = os.listdir(new_dir)
        total+= len(all_pictures)
        train_limit = int(len(all_pictures) * train)
        validate_limit = int(len(all_pictures) * validation) + train_limit
        
        for i in range(0, train_limit):
            dest_dir = os.path.join(train_dir, dname)          
            fname = random.choice(all_pictures)
            all_pictures.remove(fname)
            src = os.path.join(new_dir, fname)
            dest = os.path.join(dest_dir, fname)
            shutil.copyfile(src, dest)
            bar.update(counter)
            counter+=1
            
           
        for i in range(train_limit, validate_limit):
            dest_dir = os.path.join(validate_dir, dname)
            fname = random.choice(all_pictures)
            all_pictures.remove(fname)
            src = os.path.join(new_dir, fname)
            dest = os.path.join(dest_dir, fname)
            shutil.copyfile(src, dest)
            bar.update(counter)
            counter+=1
        
        for i in range(0, len(all_pictures)):
            dest_dir = os.path.join(test_dir, dname)
            fname = random.choice(all_pictures)
            all_pictures.remove(fname)
            src = os.path.join(new_dir, fname)
            dest = os.path.join(dest_dir, fname)
            shutil.copyfile(src, dest)
            bar.update(counter)
            counter+=1
        
    bar.finish()
    print("\nMoved ", total, ' images.')
     