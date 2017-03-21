# weka training and testing modules
import sys
import traceback
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
import weka.core.serialization as serialization

#############################################################
#############################################################
# main function to call here in this class

def weka_cross_validation(t_model, dataset_dir):
    # start the vm
    #start_jvm()
    # open the test data
    test_data = load_dataset(dataset_dir)
    # open the training model and get the
    # classifier loaded
    t_mod, classifier = load_trained_model(t_model)
    # get the array of prediction via 
    # classifier
    prediction = output_prediction_to_an_array(classifier, test_data)
    # stop the vm
    #stop_jvm()
    return prediction

#############################################################

# start java machine
def start_jvm():
    jvm.start()
    return

# stop java machine
def stop_jvm():
    print("Stopping the JVM")
    jvm.stop()
    return

# for loading of dataset
def load_dataset(dir):
    # opening the loader for Arff Reader
    loader = Loader(classname="weka.core.converters.ArffLoader")
    # creating the pointer to loaded file
    # returing to the user
    pointer_to_dataset = loader.load_file(dir)
    print "DataSet Loaded"
    return pointer_to_dataset

# loading the train model if exists for class-
# ification
def load_trained_model(t_mod):
    # using the serialization library for
    # opening the model
    objects = serialization.read_all(t_mod)
    # and after the using the classifier
    # for actually learn the classifier
    classifier = Classifier(jobject=objects[0])
    print "Model Classified"
    print classifier
    # returning both classifier and objects
    return objects, classifier

# output the trained model to an array
def output_prediction_to_an_array(classifier, test_data):
    test_data.class_is_last()
    prediction = []
    for index, inst in enumerate(test_data):
        pred = classifier.classify_instance(inst)
        dist = classifier.distribution_for_instance(inst)
        prediction.append("+" if pred != inst.get_value(inst.class_index) else '')
    return prediction

#############################################################