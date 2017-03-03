# xml parser library
import xml.dom.minidom as minidom
# image processing libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
#-*- coding: utf-8 -*-
import unicodedata
# importing the class of FeatureExtraction
import Class_DataCollector as DC

################################################
##############Array of Object###################
################################################
arr_of_objects = []
# 1 means its part of table 0 means not a part
objects_in_table = []

################################################
#################Word Data######################
################################################
no_of_words = 0
total_width = 0
total_height = 0
words = []
word_X = []
word_Y = []
word_Width = []
word_Height = []

# function for reading the xml of words and 
# then storing its values to the array for 
# further processing

def word_to_array(file):
    global no_of_words
    global total_height
    global total_width
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
        
        for x in range(0, len(X)):
            if ((X[x] < left < X_1[x]) and (Y[x] < abs(total_height - top) < Y_1[x])):
                objects_in_table.append(1)
            else:
                objects_in_table.append(0)         
    y = 0

    for word in words:
        words[y] = word.replace("\n", "")
        y = y + 1

################################################
#################Table Data#####################
################################################
no_of_tables = 0
X = []
Y = []
X_1 = []
Y_1 = []
Width = []
Height = []
word_part_of_table = []

# function for reading the xml and then storing 
# its values to the array for further processing

def table_to_array(file):
    global no_of_tables
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
    return

# for calculating the width/height of the table

def calc_difference(x0, x1):
     return (x1 - x0)

# region bounder for bounding the tables in an
# image

def region_bounder_table(img):
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

def region_bounder_word(img):
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

def assigning_values_to_the_struct():
    for x in range(0, no_of_words):
        arr_of_objects.append(DC.DataCollector(word_X[x], word_Y[x],
                    word_Width[x],
                    word_Height[x],
                    words[x], objects_in_table[x]))
    return

# main driver for the file

def main(table, img, ocr):
    # read table xml file and  calculate the
    # line spaces
    table_to_array(table)
    # read the word list xml file and then
    # calculate the distances
    word_to_array(ocr)
    # the region bounder for the sake of 
    # display
    #region_bounder_table(img)
    #region_bounder_word(img)
    # assigning the values to the struct object
    assigning_values_to_the_struct()
    sorted_array=sort_array(arr_of_objects)
    y_sorted_x=sort_array_by_x(sorted_array)
    for x in range(0,len(y_sorted_x)):
        print(y_sorted_x[x].y,y_sorted_x[x].x)
    return
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
            if new_sorted_array[i].y > new_sorted_array[i+1].y:
                if new_sorted_array[i].x >new_sorted_array[i+1].x:
                    new_sorted_array[i], new_sorted_array[i+1] = new_sorted_array[i+1], new_sorted_array[i]
                    changed = True
    return new_sorted_array
# deciding which words are in the table and which 
# are not by looping through all the elements of 
# the word and see if its x and y are equal to that
# of other arrays

if __name__ == "__main__":
    main("C:\\New Folder\\TableRecognition\\Data\\unlv\\unlv_xml_gt\\0101_003.xml",
         "C:\\New Folder\\TableRecognition\\Data\\unlv-table-png\\0101_003.png",
         "C:\\New Folder\\TableRecognition\\Data\\unlv\\unlv_xml_ocr\\0101_003.xml")
########################################################
####################End of File#########################
########################################################