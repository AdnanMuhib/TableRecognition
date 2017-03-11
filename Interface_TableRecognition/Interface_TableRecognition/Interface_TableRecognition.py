# Table recognition user defined classes
import Class_DataCollector as CDC
import UNLV_RegionBounder as TableClass

# for reading csv and drawing bounds
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

# Libraries for Directory creation and
# copy pasting the files
import os

################################################
################################################

# creating the new directory if doesnot exits
def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

# main interface for our project usage
def interface(table, img, ocr, name_of_file, junk):
    # reading the table and storing its compone-
    # nts
    no_of_table, X, Y, X_1, Y_1, width, height = TableClass.table_to_array(table)
    # reading the list of words and storing them
    # in an array
    no_of_words, total_width, total_height, words, word_X, word_Y, word_Width, word_Height = TableClass.word_to_array(ocr)
    # assigning values to struct object and crea-
    # ting an array. this is array is basically
    # an array of objects
    arr_of_objects = TableClass.assigning_values_to_the_struct(no_of_words, word_X, word_Y, word_Width, word_Height, words, X, Y, X_1, Y_1)
    # sorting an array because initially its not
    # in order
    sorted_array_y = TableClass.sort_array(arr_of_objects)
    # there is a difference in different words
    # vertically in a line. So eliminating that
    # difference to sort perfectly
    eliminated_diff = TableClass.eliminate_y_diff(sorted_array_y)
    # after sorting y then we need to sort every
    # x in that specific y
    sorted_array_x = TableClass.sort_array_by_x(eliminated_diff)
    # distance is then calculated between words
    # for training purpose
    dist_calculted_arr = TableClass.calculate_dist(sorted_array_x)
    # now the list of objects are stored in an 
    # array for writing it into csv
    array_of_objects = TableClass.objects_to_array(dist_calculted_arr)
    TableClass.write_to_csv(array_of_objects, name_of_file + "\\INPUT_CSV")
    return no_of_words, word_Width, word_Height

# bounding boxes for correct detection and wro-
# ng detection
def region_bounder(file, no_of_words, img, word_Width, word_Height):
    x, y, table, table_pre = read_csv(file)
    # for every table drawing the boundry 
    # around
    # for every table drawing the boundry 
    # around
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    marker= ['y', 'b', 'r', 'g']
    val = 0
    for i in range(0, no_of_words):
        if (val > 3):
            val = 0
        # add the rectangle patches to the plot
        # so it can be displayed to the image
        rect = patches.Rectangle((x[i], y[i]), word_Width[i],
                                 word_Height[i],
                                 linewidth=1, edgecolor='r',
                                 facecolor='none')
        val = val + 1
        ax.add_patch(rect)
    plt.show()
    return

def read_csv(f):
    x = []
    y = []
    table = []
    table_pre = []
    with open(f, "rU") as inp:
        rd = csv.reader(inp)
        for row in rd:
            x.append(row[0])
            y.append(row[1])
            table.append(row[9])
            table_pre.append(row[12])
    return x, y, table, table_pre

################################################
if __name__ == "__main__":
    ############################################
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    create_directory("C:\\TR_JUNK")
    user = os.path.expanduser("~")
    create_directory(user + "\\Documents\\TR_JUNK")
    img = raw_input("Please Input the Image : ")
    dir = img.split('.png')[0]
    table = dir + ".xml"
    ocr = dir + "_ocr.xml"
    no_of_words, width, height = interface(table, img, ocr, "C:\\TR_JUNK",  user + "\\Documents\\TR_JUNK")
    region_bounder("C:\\TR_JUNK\\output_lab.csv", no_of_words, img, width, height)
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    ############################################
################################################
##################END OF FILE###################
################################################

