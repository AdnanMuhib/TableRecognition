# importing the main library for getting the X's, Y's, 
# Width's, Height and same things for table also
import UNLV_RegionBounder

# class for feature extraction, the basic concept is 
# creating a matrix and then calculating the distances
# from each of the other object of matrix............
# basically this class is acting like a struct method
class FeatureExtraction:
    def __init__(self, x, y, width, height, word, table):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = word
        self.table = table
        return

