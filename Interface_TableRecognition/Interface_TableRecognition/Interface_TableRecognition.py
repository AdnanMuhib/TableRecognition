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
    return no_of_words, word_Width, word_Height, word_X, word_Y, arr_of_objects, no_of_table

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
        if ((int(table[i]) == int(table_pre[i])) and int(table[i] == 1)):
            # add the rectangle patches to the plot
            # so it can be displayed to the image
            rect = patches.Rectangle((x[i], y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='g',
                                     facecolor='none')
            ax.add_patch(rect)
        elif (int(table[i]) == int(table_pre[i]) and int(table[i]) == 0):
            # add the rectangle patches to the plot
            # so it can be displayed to the image
            rect = patches.Rectangle((x[i], y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='b',
                                     facecolor='none')
            ax.add_patch(rect)
        elif (int(table[i]) != int(table_pre[i])):
            # add the rectangle patches to the plot
            # so it can be displayed to the image
            rect = patches.Rectangle((x[i], y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='r',
                                     facecolor='none')
            ax.add_patch(rect)
    plt.show()
    return

##### weka version
def region_bounder_weka(file, no_of_words, img, word_Width, word_Height, word_x, word_y, arr, file_name):
    wrong_predictions = read_csv_w(file)
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    val = 0
    for i in range(0, no_of_words-1):
        if (wrong_predictions[i] == "+"):
            # add the rectangle patches to the plot
            # so it can be displayed to the image
            arr[i].prediction = not(arr[i].table)
            if(arr[i].prediction == True):
                arr[i].prediction = 1
                rect = patches.Rectangle((word_x[i], word_y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='y',
                                     facecolor='none')
                ax.add_patch(rect)
            elif (arr[i].prediction == False):
                arr[i].prediction = 0
                rect = patches.Rectangle((word_x[i], word_y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='b',
                                     facecolor='none')
                ax.add_patch(rect)
        elif (arr[i].prediction is None):
            arr[i].prediction = arr[i].table
            if (arr[i].table == 1):
                rect = patches.Rectangle((word_x[i], word_y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='y',
                                     facecolor='none')
                ax.add_patch(rect)
            elif (arr[i].table == 0):
                rect = patches.Rectangle((word_x[i], word_y[i]), word_Width[i],
                                     word_Height[i],
                                     linewidth=1, edgecolor='b',
                                     facecolor='none')
                ax.add_patch(rect)
    plt.savefig(file_name + ".png", transparent=True, dpi=300)
    plt.close()
    return arr, wrong_predictions
##########################################3
def region_bounder_weka_via_arr(file, no_of_words, img, word_Width, word_Height, word_x, word_y, arr, file_name):
# for every table drawing the boundry 
    # around
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    for x in range(0, no_of_words):
        # add the rectangle patches to the plot
        # so it can be displayed to the image
        if(arr[x].prediction == 1):
            rect = patches.Rectangle((word_x[x], word_y[x]), word_Width[x],
                                     word_Height[x],
                                     linewidth=1, edgecolor='y',
                                     facecolor='none')
            ax.add_patch(rect)
        elif(arr[x].prediction == 0):
            rect = patches.Rectangle((word_x[x], word_y[x]), word_Width[x],
                                     word_Height[x],
                                     linewidth=1, edgecolor='b',
                                     facecolor='none')
            ax.add_patch(rect)
    plt.savefig(file_name + "_preprocessed.png", transparent=True, dpi=300)
    plt.close()

###################################################
### adnan to write code here
def ground_truth_x(my_sorted_array, wrong_prediction):
    for i in range(len(my_sorted_array)-1):
        if (wrong_prediction[i] == "+"):
            if i==0:
                my_sorted_array[i].neighbour_1 = my_sorted_array[i+1].prediction
                my_sorted_array[i].neighbour_2 = my_sorted_array[i+2].prediction
                val = my_sorted_array[i].neighbour_1 and my_sorted_array[i].neighbour_2
                my_sorted_array[i].prediction = val
            elif(i==len(my_sorted_array)-1):
                my_sorted_array[i].neighbour_1= 0
                my_sorted_array[i].neighbour_2 = my_sorted_array[i-1].prediction
                val = my_sorted_array[i].neighbour_1 and my_sorted_array[i].neighbour_2
                my_sorted_array[i].prediction = val
            else:
                my_sorted_array[i].neighbour_1 = my_sorted_array[i-2].prediction
                my_sorted_array[i].neighbour_2 = my_sorted_array[i-1].prediction
                val = my_sorted_array[i].neighbour_1 and my_sorted_array[i].neighbour_2
                my_sorted_array[i].prediction = val
    return my_sorted_array
'''
def ground_truth_y(my_sorted_array):
    current_index = 0
    x_pos = 0
    y_pos = 0
    y_changed = False
    words_in_row = get_words_in_row(my_sorted_array)  
    last_row_last_element = 0
    for i in range(0, len(words_in_row)):
        for j in range(last_row_last_element, last_row_last_element + words_in_row[i]):
            print "Line ", i, "Word : ", my_sorted_array[j].word, "neighbour 4", my_sorted_array[j + last_row_last_element + words_in_row[i] + 1].word 
        last_row_last_element = words_in_row[i]   
    return

def get_words_in_row(arr):
    words_in_row = []
    y_changed = False
    initial_y = arr[0].y
    count = 0
    j = 0
    for i in range(0, len(arr)):
        if (initial_y < arr[i].y):
            y_changed = True
            initial_y = arr[i].y
            words_in_row.append(count)
            j = j + 1
            count = 0
        elif(initial_y == arr[i].y):
            y_changed = False
            count = count + 1
    return words_in_row
'''
###################################################

# read csv for weka
def read_csv_w(f):
    plus = []
    with open(f, "rU") as inp:
        rd = csv.reader(inp)
        for row in rd:
            plus.append(row[3])
    return plus
# read csv for rapid miner
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
    no_of_words, width, height, x, y, objects, no_of_table = interface(table, img, ocr, "C:\\TR_JUNK",  user + "\\Documents\\TR_JUNK")
    #region_bounder("C:\\TR_JUNK\\output_lab.csv", no_of_words, img, width, height)
    arr, wrong_predictions = region_bounder_weka("D:\\KICS - Research Officer\\CVML\\tablerecognition\\Data\\FixedData\\Test\\ARFF\\336_weka.csv", no_of_words, img, width, height, x, y, objects, "C:\\TR_JUNK\\336")
    new_arr = ground_truth_x(arr, wrong_predictions)
    arr = region_bounder_weka_via_arr(new_arr, no_of_words, img, width, height, x, y, objects, "C:\\TR_JUNK\\336")
    #ground_truth_y(arr)
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    ############################################
################################################
##################END OF FILE###################
################################################

