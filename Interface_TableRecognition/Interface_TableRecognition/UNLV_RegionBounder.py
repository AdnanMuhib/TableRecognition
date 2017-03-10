# xml parser library
import xml.dom.minidom as minidom
# math library
import math
# image processing libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
#-*- coding: utf-8 -*-
import unicodedata
# importing the class of FeatureExtraction
import Class_DataCollector as DC
# importing writing to csv library
import csv
# file handling libraries for batch processing
import os
import re
import fnmatch
import locale
locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_NUMERIC, "C")
################################################
##############Array of Object###################
################################################
arr_of_objects = []

################################################
#################Word Data######################
################################################
# function for reading the xml of words and 
# then storing its values to the array for 
# further processing

def word_to_array(file):
    no_of_words = 0
    total_width = 0
    total_height = 0
    words = []
    word_X = []
    word_Y = []
    word_Width = []
    word_Height = []
    # parse the file using element treee for xml 
    # parser get the root object to move forward
    root = minidom.parse(file)
    # get the number of tables
    no_of_words = len(root.getElementsByTagName('word'))
    #total lenght of document
    for info in root.getElementsByTagName('docinfo'):
        total_width = int(unicodedata.normalize('NFKD', info.getAttribute("width")).encode('ascii', 'ignore'))
        total_height = int(unicodedata.normalize('NFKD',info.getAttribute("height")).encode('ascii', 'ignore'))
    # get the elements by tag name and store it
    # in an array
    for elements in root.getElementsByTagName('word'):
        _words = str(unicodedata.normalize('NFKD', (elements.childNodes[0].data)).encode('ascii', 'ignore'))
        left = int(unicodedata.normalize('NFKD', (elements.getAttribute("left"))).encode('ascii', 'ignore'))
        right = int(unicodedata.normalize('NFKD', (elements.getAttribute("right"))).encode('ascii', 'ignore'))
        top = int(unicodedata.normalize('NFKD', (elements.getAttribute("top"))).encode('ascii', 'ignore'))
        bottom = int(unicodedata.normalize('NFKD', (elements.getAttribute("bottom"))).encode('ascii', 'ignore'))
        words.append(_words)        
        word_X.append(left)
        word_Y.append(abs(total_height - top))
        word_Width.append(abs(left - right))
        word_Height.append(abs(top - bottom))
        
        #for x in range(0, len(X)):
        #    if ((X[x] <= left <= X_1[x]) and (Y[x] <= abs(total_height - top) <= Y_1[x])):
        #        objects_in_table.append(1)
        #    else:
        #        objects_in_table.append(0)         
    y = 0

    for word in words:
        words[y] = word.replace("\n", "")
        y = y + 1
    return no_of_words, total_width, total_height, words, word_X, word_Y, word_Width, word_Height

# there is difference in pixels values along the y axis
# because of raw data to remove that difference you can 
# simply change the value of 20 to the required one
def eliminate_y_diff(arr):
    previous_y=arr[0].y
    for i in range(len(arr)):
        if(i!=len(arr)-1):
            if(abs(arr[i].y-previous_y) < 20):
                arr[i].y=previous_y
        previous_y=arr[i].y
    return arr

################################################
#################Table Data#####################
################################################


# function for reading the xml and then storing 
# its values to the array for further processing

def table_to_array(file):
    no_of_tables = 0
    X = []
    Y = []
    X_1 = []
    Y_1 = []
    Width = []
    Height = []
    # parse the file using element treee for xml 
    # parser get the root object to move forward
    root = minidom.parse(file)
    # get the number of tables
    no_of_tables = len(root.getElementsByTagName('Table'))
    
    # get the elements by tag name and store it
    # in an array
    for elements in root.getElementsByTagName('Table'):
        X.append(int(unicodedata.normalize('NFKD', (elements.getAttribute("x0"))).encode('ascii', 'ignore')))
        Y.append(int(unicodedata.normalize('NFKD', (elements.getAttribute("y0"))).encode('ascii', 'ignore')))
        X_1.append(int(unicodedata.normalize('NFKD', (elements.getAttribute("x1"))).encode('ascii', 'ignore')))
        Y_1.append(int(unicodedata.normalize('NFKD', (elements.getAttribute("y1"))).encode('ascii', 'ignore')))
        Width.append(calc_difference(int(unicodedata.normalize('NFKD', (elements.getAttribute("x0"))).encode('ascii', 'ignore')), 
                                         int(unicodedata.normalize('NFKD', (elements.getAttribute("x1"))).encode('ascii', 'ignore'))))
        Height.append(calc_difference(int(unicodedata.normalize('NFKD', (elements.getAttribute("y0"))).encode('ascii', 'ignore')), 
                                         int(unicodedata.normalize('NFKD', (elements.getAttribute("y1"))).encode('ascii', 'ignore'))))
    return no_of_tables, X, Y, X_1, Y_1, Width, Height

# for calculating the width/height of the table

def calc_difference(x0, x1):
     return (x1 - x0)

# region bounder for bounding the tables in an
# image

def region_bounder_table(img, no_of_tables):
    # for every table drawing the boundry 
    # around
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    for x in range(0, no_of_tables):
        # add the rectangle patches to the plot
        # so it can be displayed to the image
        rect = patches.Rectangle((X[x], Y[x]), Width[x], Height[x],
                                 linewidth=1, edgecolor='r',
                                 facecolor='none')
        ax.add_patch(rect)
    plt.show()

# region bounder for bounding the words in an
# image

def region_bounder_word(img, no_of_words):
    # for every table drawing the boundry 
    # around
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    marker= ['y', 'b', 'r', 'g']
    val = 0
    for x in range(0, no_of_words):
        if (val > 3):
            val = 0
        # add the rectangle patches to the plot
        # so it can be displayed to the image
        rect = patches.Rectangle((word_X[x], word_Y[x]), word_Width[x],
                                 word_Height[x],
                                 linewidth=1, edgecolor=marker[val],
                                 facecolor='none')
        val = val + 1
        ax.add_patch(rect)
    plt.show()

# moving the data from array to struct for
# sorting and other operations

def assigning_values_to_the_struct(no_of_words, word_X, word_Y, word_Width, word_Height, words, X, Y, X_1, Y_1):
    arr_of_objects = []
    for x in range(0, no_of_words):
        arr_of_objects.append(DC.DataCollector(word_X[x], word_Y[x],
                    word_Width[x],
                    word_Height[x],
                    words[x], part_of_table(word_X[x], word_Y[x], X, Y, X_1, Y_1)))
    return arr_of_objects

def part_of_table(x, y, X, Y, X_1, Y_1):
    table = 0
    for i in range(0, len(X)):
        if ((X[i] <= x <= X_1[i]) and (Y[i] <= y <= Y_1[i])):
            table = 1
        else: table = 0
    return table

#sorting the array of objects with respect to y values
def sort_array(new_array_of_objects):
    changed = True
    while changed:
        changed = False
        for i in range(len(new_array_of_objects) - 1):
            if new_array_of_objects[i].y > new_array_of_objects[i+1].y:
                new_array_of_objects[i], new_array_of_objects[i+1] = new_array_of_objects[i+1], new_array_of_objects[i]
                changed = True
    return new_array_of_objects
#sorting the y values sorted array of objects with respect to x values
def sort_array_by_x(new_sorted_array):
    changed = True
    while changed:
        changed = False
        for i in range(len(new_sorted_array) - 1):
            if new_sorted_array[i].y == new_sorted_array[i+1].y:
                if new_sorted_array[i].x > new_sorted_array[i+1].x:
                    new_sorted_array[i], new_sorted_array[i+1] = new_sorted_array[i+1], new_sorted_array[i]
                    changed = True
    return new_sorted_array

# calculating the distance of one object from other
def calculate_dist(my_sorted_array):
    
    # by using the formula distance=sqrt((x2-x1)^2+(y2-y1)^2))
    # x+1 and x-1 distance
    for i in range(len(my_sorted_array)):
        if i==0:
            my_sorted_array[i].x_1_dist = math.ceil( math.sqrt(pow((my_sorted_array[i+1].x-my_sorted_array[i].x),2)+
                                                      pow( (my_sorted_array[i+1].y-my_sorted_array[i].y),2) ) )
            my_sorted_array[i].x_m_1_dist= 0
        elif(i==len(my_sorted_array)-1):
            my_sorted_array[i].x_1_dist= 0
            my_sorted_array[i].x_m_1_dist = math.ceil( math.sqrt(pow((my_sorted_array[i].x-my_sorted_array[i-1].x),2)+
                                                      pow((my_sorted_array[i].y-my_sorted_array[i-1].y),2)) )
        else:
            my_sorted_array[i].x_1_dist= math.ceil( math.sqrt(pow((my_sorted_array[i+1].x-my_sorted_array[i].x),2)+
                                                      pow((my_sorted_array[i+1].y-my_sorted_array[i].y),2)) )
            my_sorted_array[i].x_m_1_dist=math.ceil( math.sqrt(pow((my_sorted_array[i].x-my_sorted_array[i-1].x),2)+
                                                      pow((my_sorted_array[i].y-my_sorted_array[i-1].y),2)) )
    # for y+1 and y-1 distance
    words_in_row = 0
    total_words = 0
    line_index=0
    y_m_1_dist = 0
    row_y_position=my_sorted_array[0].y
    row_x_position=my_sorted_array[0].x
    for i in range ( len(my_sorted_array) ):
        total_words += 1
        if row_y_position == my_sorted_array[i].y:
            words_in_row += 1
            my_sorted_array[i].y_m_1_dist = y_m_1_dist
        else:
            #print("Total Words in the row are : ",words_in_row_counter)
            y_m_1_dist = math.ceil( math.sqrt(pow((my_sorted_array[i].x-row_x_position),2)+
                                                      pow((my_sorted_array[i].y-row_y_position),2)) )
            row_y_position = my_sorted_array[i].y
            row_x_position = my_sorted_array[i].x
            for j in range(line_index,(line_index+words_in_row)):
                my_sorted_array[j].y_1_dist = y_m_1_dist
            line_index=total_words
            my_sorted_array[i].y_m_1_dist = y_m_1_dist
            my_sorted_array[i].y_1_dist = y_m_1_dist
            words_in_row=0
    return my_sorted_array

# copying all the objects value to an array
# for further writing it to the csv file
def objects_to_array(arr):
    return_arr = []
    return_arr.append([])
    return_arr[0].append("word")
    return_arr[0].append("x")
    return_arr[0].append("y")
    return_arr[0].append("x+1 dist")
    return_arr[0].append("x-1 dist")
    return_arr[0].append("y+1 dist")
    return_arr[0].append("y-1 dist")
    return_arr[0].append("width")
    return_arr[0].append("height")
    return_arr[0].append("table")

    index = 1
    for i in range(0, len(arr)):
        return_arr.append([])
        return_arr[index].append(arr[i].word)
        return_arr[index].append(arr[i].x)
        return_arr[index].append(arr[i].y)
        return_arr[index].append(arr[i].x_1_dist)
        return_arr[index].append(arr[i].x_m_1_dist)
        return_arr[index].append(arr[i].y_1_dist)
        return_arr[index].append(arr[i].y_m_1_dist)
        return_arr[index].append(arr[i].width)
        return_arr[index].append(arr[i].height)
        return_arr[index].append(arr[i].table)
        index = index + 1
    return return_arr
# writing the objects and there values to csv
# for training and testing purposes
def write_to_arff(arr):
    return_arr = []  
    index = 0
    # start of the loop
    for i in range(0, len(arr)):
        return_arr.append([])
        return_arr[index].append(arr[i].word)
        return_arr[index].append(arr[i].x)
        return_arr[index].append(arr[i].y)
        return_arr[index].append(arr[i].x_1_dist)
        return_arr[index].append(arr[i].x_m_1_dist)
        return_arr[index].append(arr[i].y_1_dist)
        return_arr[index].append(arr[i].y_m_1_dist)
        return_arr[index].append(arr[i].width)
        return_arr[index].append(arr[i].height)
        return_arr[index].append(arr[i].table)
        index = index + 1
    # end of the loop
    arff.dump("test.arff", return_arr, relation="wordlist",
              names=["word", "x", "y", "x_1_dist", "x_m_1_dist",
                     "y_1_dist", "y_m_1_dist", "width", "height",
                     "table"])
    return
# writing the objects and there values to csv
# for training and testing purposes
def write_to_csv(arr, name_of_file):
    print "writing file : ", name_of_file
    name_of_file = name_of_file + '.csv'
    with open(name_of_file, "wb") as f:
        write = csv.writer(f)
        write.writerows(arr)
    return

# main driver for the file
def main(table, img, ocr, name_of_file):
    # read table xml file and  calculate the
    # line spaces
    no_of_table, X, Y, X_1, Y_1, width, height = table_to_array(table)
    # read the word list xml file and then
    # calculate the distances
    no_of_words, total_width, total_height, words, word_X, word_Y, word_Width, word_Height = word_to_array(ocr)
    # the region bounder for the sake of 
    # display
    #region_bounder_table(img)
    #region_bounder_word(img)
    # assigning the values to the struct object
    arr_of_objects = assigning_values_to_the_struct(no_of_words, word_X, word_Y, word_Width, word_Height, words, X, Y, X_1, Y_1)
    my_sorted_array = sort_array(arr_of_objects)
    my_sorted_array = eliminate_y_diff(my_sorted_array)
    my_sorted_array = sort_array_by_x(my_sorted_array)
    my_sorted_array = calculate_dist(my_sorted_array)
    arr = objects_to_array(my_sorted_array)
    write_to_csv(arr, name_of_file)
    #for x in range(0,len(my_sorted_array)):
     #   print ("x : ", my_sorted_array[x].x,"y : ",
      #         my_sorted_array[x].y,"word : ",
       #        my_sorted_array[x].word)

    #for i in range(len(my_sorted_array)):
     #   print("x_1_dist : " ,  my_sorted_array[i].x_1_dist, 
      #        "word at x_1_dist : ", my_sorted_array[i].word)
       # print("x_m_1_dist: " , my_sorted_array[i].x_m_1_dist,  
        #      "word at x_m_1_dist : ", my_sorted_array[i].word)
        #print("y_1_dist : " ,my_sorted_array[i].y_1_dist,
         #     "word at y_1_dist : ", my_sorted_array[i].word)
        #print("y_m_1_dist : " ,my_sorted_array[i].y_m_1_dist,
         #     "word at y_m_1_dist : ", my_sorted_array[i].word)

    return

# deciding which words are in the table and which 
# are not by looping through all the elements of 
# the word and see if its x and y are equal to that
# of other arrays

def batch_processor():
    dir = raw_input("Please Input the directory")
    extension = "*.png"
    file_list = []
    # accessing all the files and storing it into
    # the file_list
    for r, d, f in os.walk(dir):
        for file in fnmatch.filter(f, extension):
            file_list.append(os.path.join(r, file))
    
    # calling the main function with the files
    for file in file_list:
        img = file
        name_of_file = re.split('.png', file)[0]
        ocr = name_of_file + '_ocr.xml'
        table = name_of_file + '.xml'
        main(table, img, ocr, name_of_file)

    # end of the batch processing
    return

if __name__ == "__main__":
    #for i in range(421, 425):
     #   dir = "F:\\KICS - Research Officer\\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\bulk_data"
      #  table = dir + "\\" + str(i) + ".xml"
       # ocr = dir + "\\" + str(i) + "_ocr.xml"
       # img = dir + "\\" + str(i) + ".png"
       # name = dir + "\\" + str(i) + "_csv"
       # main(table, img, ocr, name)
    #batch_processor()
    main("F:\\KICS - Research Officer\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\bulk_data\\47.xml",
      "F:\\KICS - Research Officer\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\bulk_data\\47.png",
      "F:\\KICS - Research Officer\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\bulk_data\\47_ocr.xml",
      "F:\\KICS - Research Officer\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\bulk_data\\47_csv ")
    
########################################################
####################End of File#########################
########################################################