import keras
import tensorflow
from keras.models import load_model
import requests
from PIL import Image 
from keras.preprocessing import image
import numpy as np
from keras.applications.imagenet_utils import decode_predictions
from keras import applications
import cv2
from google.colab.patches import cv2_imshow as cv
import requests


def image_view(img_url):
  img_data = requests.get(img_url).content
  with open('image_name.jpg', 'wb') as handler:
      handler.write(img_data)

  # Save image in set directory 
  # Read RGB image 
  img = cv2.imread('image_name.jpg')  
  # Output img with window name as 'image' 
  cv(img)  
  # Maintain output window utill 
  # user presses a key 
  cv2.waitKey(0)         
  # Destroying present windows on screen 
  cv2.destroyAllWindows() 


class Vgg16():
  def __init__(self,url):
    '''
    ------------
    Argument
    ------------
    Vgg16 Keywords
    *url = Image Url or Input Image

    '''    
    self.url = url
    model = applications.VGG16(weights=None)
    model = applications.VGG16(weights='imagenet')
    data = image_view(self.url)
    input_image = image.load_img('image_name.jpg', target_size = (224,224))
    input_image = image.img_to_array(input_image)
    input_image = np.expand_dims(input_image, axis = 0)
    result = model.predict(input_image)
    predicting_class = decode_predictions(result)
    print('----------------Result--------------------')
    print(predicting_class)



class ResNet50():
  def __init__(self,url):
    '''
    ------------
    Argument
    ------------
    ResNet50 Keywords
    *url = Image Url or Input Image

    '''
    self.url = url
    model = applications.ResNet50(weights=None)
    model = applications.ResNet50(weights='imagenet')
    data = image_view(self.url)
    input_image = image.load_img('image_name.jpg', target_size = (224,224))
    input_image = image.img_to_array(input_image)
    input_image = np.expand_dims(input_image, axis = 0)
    result = model.predict(input_image)
    predicting_class = decode_predictions(result)
    print('----------------Result--------------------')
    print(predicting_class)


class MobileNetV2():

  def __init__(self,url):

    '''
    ------------
    Argument
    ------------
    MobileNetV2 Keywords
    *url = Image Url

    '''
    self.url = url
    model = applications.MobileNetV2(weights=None)
    model = applications.MobileNetV2(weights='imagenet')
    data = image_view(self.url)
    test_image = image.load_img('image_name.jpg', target_size = (224,224))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    predicting_class = decode_predictions(result)
    print('----------------Result--------------------')
    print(predicting_class)


