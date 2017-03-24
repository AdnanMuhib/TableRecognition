#clear()
import os
clear = lambda: os.system('cls')
clear()

#command line arguments
import sys
argumentList = str(sys.argv)
if len(sys.argv) > 0 and str(sys.argv)[0] == '-train':
	train = true
else:
	train = false
#KERAS
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import theano
from PIL import Image
from numpy import *
# SKLEARN
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

# input image dimensions
img_rows, img_cols = 256, 256

# number of channels
img_channels = 1

#%%
#  data

path1 = 'D:\Documents\Visual Studio 2015\Dataset\Images\input_data'    #path of folder of images    
path2 = 'D:\Documents\Visual Studio 2015\Dataset\Images\input_data_resized'  #path of folder to save images     

listing = os.listdir(path1) 
num_samples=size(listing)
#print num_samples

for file in listing:
    im = Image.open(path1 + '\\' + file)   
    img = im.resize((img_rows,img_cols))
    gray = img.convert('L')
                #need to do some more processing here           
    gray.save(path2 +'\\' +  file, "JPEG")

imlist = os.listdir(path2)

im1 = array(Image.open('D:\Documents\Visual Studio 2015\Dataset\Images\input_data_resized' + '\\'+ imlist[0])) # open one image to get size
m,n = im1.shape[0:2] # get the size of the images
imnbr = len(imlist) # get the number of images

# create matrix to store all flattened images
immatrix = array([array(Image.open('D:\Documents\Visual Studio 2015\Dataset\Images\input_data_resized' + '\\' + im2)).flatten()
              for im2 in imlist],'f')
                
label=np.ones((num_samples,),dtype = int)
label[0:11] = 0
label[11:22] = 1
label[22:33] = 2
label[33:44] = 3
label[44:] = 4


data,Label = shuffle(immatrix,label, random_state=2)
train_data = [data,Label]

img=immatrix[3].reshape(img_rows,img_cols)
plt.imshow(img)
plt.imshow(img,cmap='gray')
#print (train_data[0].shape)
#print (train_data[1].shape)

#%%

#batch_size to train
batch_size = 32
# number of output classes
nb_classes = 5
# number of epochs to train
nb_epoch = 20


# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
nb_conv = 5

#%%
(X, y) = (train_data[0],train_data[1])


# STEP 1: split X and y into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)


X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

#print('X_train shape:', X_train.shape)
#print(X_train.shape[0], 'train samples')
#print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

#i = 3
#plt.imshow(X_train[i, 0], interpolation='nearest')
#print("label : ", Y_train[i,:])

#%%

model = Sequential()

model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                        border_mode='valid',
                        input_shape=(1, img_rows, img_cols)))
convout1 = Activation('relu')
model.add(convout1)
model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
convout2 = Activation('relu')
model.add(convout2)
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

# Loading weights
if(train):
	hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch, verbose=1, validation_data=(X_test, Y_test))
else:
	fname = "D:\\weights-Test-CNN.hdf5"
	hist = model.load_weights(fname)
#%%


            
            
#hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, verbose=1, validation_split=0.2)


# visualizing losses and accuracy

#train_loss=hist.history['loss']
#val_loss=hist.history['val_loss']
#train_acc=hist.history['acc']
#val_acc=hist.history['val_acc']
xc=range(nb_epoch)

plt.figure(1,figsize=(7,5))
#plt.plot(xc,train_loss)
#plt.plot(xc,val_loss)
plt.xlabel('num of Epochs')
plt.ylabel('loss')
#plt.title('train_loss vs val_loss')
plt.grid(True)
plt.legend(['train','val'])
#print plt.style.available # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])

plt.figure(2,figsize=(7,5))
#plt.plot(xc,train_acc)
#plt.plot(xc,val_acc)
plt.xlabel('num of Epochs')
plt.ylabel('accuracy')
#plt.title('train_acc vs val_acc')
plt.grid(True)
plt.legend(['train','val'],loc=4)
#print plt.style.available # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])




#%%       

score = model.evaluate(X_test, Y_test, show_accuracy=True, verbose=0)
#print('Test score:', score[0])
#print('Test accuracy:', score[1])
#print(model.predict_classes(X_test[1:5]))
#print(Y_test[1:5])



#%%

# visualizing intermediate layers

#output_layer = model.layers[1].get_output()
#output_fn = theano.function([model.layers[0].get_input()], output_layer)

# the input image

input_image=X_train[0:1,:,:,:]
#print(input_image.shape)

plt.imshow(input_image[0,0,:,:],cmap ='gray')
plt.imshow(input_image[0,0,:,:])


#output_image = output_fn(input_image)
#print(output_image.shape)

# Rearrange dimension so we can plot the result 
#output_image = np.rollaxis(np.rollaxis(output_image, 3, 1), 3, 1)
#print(output_image.shape)


fig=plt.figure(figsize=(8,8))
for i in range(32):
    ax = fig.add_subplot(6, 6, i+1)
    #ax.imshow(output_image[0,:,:,i],interpolation='nearest' ) #to see the first filter
    #ax.imshow(output_image[0,:,:,i],cmap=matplotlib.cm.gray)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.tight_layout()
plt

# Confusion Matrix

from sklearn.metrics import classification_report,confusion_matrix

Y_pred = model.predict(X_test)
#print(Y_pred)
y_pred = np.argmax(Y_pred, axis=1)
#print(y_pred)
  
#                       (or)

#y_pred = model.predict_classes(X_test)
#print(y_pred)

p=model.predict_proba(X_test) # to predict probability

target_names = ['class 0(ASAD)', 'class 1(AYN)', 'class 2(GULRAIZ)', 'class 3(ADEEL)', 'class 4(SHAHID)']
print(classification_report(np.argmax(Y_test,axis=1), y_pred,target_names=target_names))
print(confusion_matrix(np.argmax(Y_test,axis=1), y_pred))

# saving weights

fname = "D:\\weights-Test-CNN.hdf5"
model.save_weights(fname,overwrite=True)



# Loading weights

fname = "D:\\weights-Test-CNN.hdf5"
model.load_weights(fname)



def check_prediction(fileName):
		myLabels = ['Asad','Ayn','Gulraiz','Adeel','Shahid']
		myPath = 'C:\\Users\\Ayn ul hassan\\Desktop\\'
		im = Image.open(fileName)
		img = im.resize((img_rows,img_cols))
		gray = img.convert('L')
		gray.save(myPath + 'myFile.jpg', "JPEG")

		gray = array([array(Image.open(myPath + 'myFile.jpg')).flatten()])
		gray = gray.reshape(gray.shape[0], 1, img_rows, img_cols)
		gray = gray.astype('float32')
		gray /= 255
		return myLabels[model.predict_classes(gray)[0]]

print check_prediction('C:\\Users\\Ayn ul hassan\\Desktop\\1.jpg')