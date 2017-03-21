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
import weka.core.jvm as jvm
import traceback
# self defined wrapper of python on 
# weka-python
import Weka_Machine_Learning as WML
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
def region_bounder_weka(wrong_predictions, no_of_words, img, word_Width, word_Height, word_x, word_y, arr, file_name):
    #wrong_predictions = read_csv_w(file)
    img = np.array(Image.open(img))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    val = 0
    if (no_of_words - len(wrong_predictions) == 1):
        length = no_of_words
    else:
        length = no_of_words - 1
    for i in range(0, length):
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
    return arr
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

def write_to_csv(arr, no_of_words, name):
    #print("table : prediction")
    words_in_table = 0
    words_in_table_dected_non_table = 0
    words_in_non_table = 0
    words_in_non_table_detected_table = 0
    for i in range(0, no_of_words):
        #print(arr[i].table, ":" ,arr[i].prediction)
        if (arr[i].table == 1 and arr[i].prediction == 1):
            words_in_table = words_in_table + 1
        elif (arr[i].table == 0 and arr[i].prediction == 0):
            words_in_non_table = words_in_non_table + 1
        elif (arr[i].table == 1 and arr[i].prediction == 0):
            words_in_table_dected_non_table = words_in_table_dected_non_table + 1
        elif (arr[i].table == 0 and arr[i].prediction == 1):
            words_in_non_table_detected_table = words_in_non_table_detected_table + 1
        elif (arr[i].prediction == None):
            if (arr[i].table == 1):
                words_in_table = words_in_table + 1
            elif (arr[i].table == 0):
                words_in_non_table = words_in_non_table + 1
    #print("table : Non Table : wrong Detected Table : wrong Detected Non Table")
    #print(words_in_table, "   ", words_in_non_table, "   ", words_in_non_table_detected_table, "   ", words_in_table_dected_non_table)
    _arr = []
    _arr.append([])
    _arr[0].append("Table")
    _arr[0].append("None Table")
    _arr[0].append("wrong Detected Table")
    _arr[0].append("wrong Detected Non Table")
    _arr.append([])
    _arr[1].append(words_in_table)
    _arr[1].append(words_in_non_table)
    _arr[1].append(words_in_non_table_detected_table)
    _arr[1].append(words_in_table_dected_non_table)
    
    TableClass.write_to_csv(_arr, name)
    return

################################################
def call_the_interface(img, arff, out, name, name_b):
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    dir = img.split('.png')[0]
    user = os.path.expanduser("~")
    table = dir + ".xml"
    ocr = dir + "_ocr.xml"
    no_of_words, width, height, x, y, objects, no_of_table = interface(table, img, ocr, "C:\\TR_JUNK",  user + "\\Documents\\TR_JUNK")
    prediction = WML.weka_cross_validation("F:\\KICS - Research Officer\\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\FixedData\\Train\\Train CSV and ARFF\\WekaModel_y_excluded_included_width.model",
                                           arff)
    #region_bounder("C:\\TR_JUNK\\output_lab.csv", no_of_words, img, width, height)
    arr = region_bounder_weka(prediction, no_of_words, img, width, height, x, y, objects, out)
    write_to_csv(arr, no_of_words, name_b)
    new_arr = ground_truth_x(arr, prediction)
    arr = region_bounder_weka_via_arr(new_arr, no_of_words, img, width, height, x, y, objects, out)
    write_to_csv(new_arr, no_of_words, name)
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    return



###########################################################
def main():
    create_directory("C:\\TR_JUNK")
    user = os.path.expanduser("~")
    create_directory(user + "\\Documents\\TR_JUNK")
    #dir = raw_input("Please Input the main directory having subfolders : ")
    dir = "F:\\KICS - Research Officer\\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\FixedData\\Test"
    after_pre = dir + "\\result after preprocessing\\"
    before_pre = dir + "\\result before preprocessing\\"
    for i in range(326, 327):
        if (i != 330 and i != 332 and i != 336 and i != 341 and i != 343 and i != 344 and i != 345 and i != 351 and i != 352 and i != 357 and i != 360 and i != 363 and i != 370 and i != 371 and i != 377 and i != 379 and i != 380 and i != 383 and i != 387 and i != 390 and i != 393 and i != 394 and i != 398 and i != 404 and i != 410 and i != 412 and i != 423):
            img = dir + "\\bulk_data\\" + str(i) + ".png"
            arff = dir + "\\ARFF\\" + str(i) + "_arf.arff"
            out = "C:\\TR_JUNK\\" + str(i)
            name = after_pre + str(i)
            name_b = before_pre + str(i)
            call_the_interface(img, arff, out, name, name_b)
    return    
#################################################
if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
#################################################
    '''
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
    prediction = WML.weka_cross_validation("F:\\KICS - Research Officer\\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\FixedData\\Train\\Train CSV and ARFF\\WekaModel_y_excluded_included_width.model",
                                           "F:\\KICS - Research Officer\\CVML\\RegionBounder\\New folder\\TableRecognition\\Data\\FixedData\\Test\\ARFF\\331_arf.arff")
    #region_bounder("C:\\TR_JUNK\\output_lab.csv", no_of_words, img, width, height)
    arr = region_bounder_weka(prediction, no_of_words, img, width, height, x, y, objects, "C:\\TR_JUNK\\331")
    new_arr = ground_truth_x(arr, prediction)
    arr = region_bounder_weka_via_arr(new_arr, no_of_words, img, width, height, x, y, objects, "C:\\TR_JUNK\\331")
    #ground_truth_y(arr)
    print ("##############################################")
    print ("This is a testing version of Table Recognition")
    print ("##############################################")
    '''
#################################################
##################END OF FILE####################
################################################

