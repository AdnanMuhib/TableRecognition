# importing the main library for getting the X's, Y's, 
# Width's, Height and same things for table also
import UNLV_RegionBounder

# class for feature extraction, the basic concept is     
# creating a matrix and then calculating the distances
# from each of the other object of matrix............
# basically this class is acting like a struct method

class DataCollector:                                
    x_1_dist = None
    x_m_1_dist = None
    y_1_dist = None
    y_m_1_dist = None
    # mention which of the neighbour is which one
    neighbour_1 = None
    neighbour_2 = None
    neighbour_3 = None
    neighbour_4 = None
    # dont worry about this one, it stores what was 
    # predicted
    prediction = None

    def __init__(self, x, y, width,
                 height, word, table):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = word
        self.table = table
        return
    
    def set_table_predicted(predicted):
        prediction = predicted
        return

    def set_x_1_dist(x):
        x_1_dist = x
        return

    def set_x_m_1_dist(x):
        x_m_1_dist = x
        return

    def set_y_1_dist(x):
        y_1_dist = x
        return

    def set_y_m_1_dist(x):
        y_m_1_dist = x
        return

    def set_neighbour_1(x):
        neighbour_1 = x
        return

    def set_neighbour_2(x):
        neighbour_2 = x
        return

    def set_neighbour_3(x):
        neighbour_3 = x
        return

    def set_neighbour_4(x):
        neighbour_4 = x
        return
########################################################
####################End of File#########################
########################################################