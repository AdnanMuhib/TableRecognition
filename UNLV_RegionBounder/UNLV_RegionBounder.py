# xml parser library
import xml.dom.minidom as minidom
# image processing libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
#-*- coding: utf-8 -*-
import unicodedata

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
    region_bounder_table(img)
    region_bounder_word(img)
    return


if __name__ == "__main__":
    main("F:\\KICS - Research Officer\\CVML\\unlv\\unlv_xml_gt\\0101_003.xml",
         "F:\\KICS - Research Officer\\CVML\\unlv-table-png\\0101_003.png",
         "F:\\KICS - Research Officer\\CVML\\unlv\\unlv_xml_ocr\\0101_003.xml")
