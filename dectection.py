
import os
import tensorflow as tf
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np



path_test = 'test_images/'
# images_path = path_test
images_path = 'uploads/temp_image'
model_path = 'model/VGG_model.h5'
files = []
imgs = []
target_size = (224, 224)
classes_names = ['glioma', 'meningioma', 'notumor', 'pituitary']


def engine(logger):
    return_objs = {
       'result': [],
    }

    model = tf.keras.models.load_model(model_path)

    if not os.listdir(images_path) == []:
     files = [f for f in os.listdir(images_path) if not f.startswith('.') and os.path.isfile(os.path.join(images_path, f))]

     for idx , img in enumerate(files):
        image_pill = image.load_img(os.path.join(images_path, img),color_mode='rgb', target_size=target_size)
        x = image.img_to_array(image_pill)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        logger.info(f"Starting to predict tumor type in image : {img} ")

        prediction = model.predict(x)
        result = np.argmax(prediction)

        logger.info(f"Prediction successfully completed for : {img}")

        result_data = {
           "id" : idx ,
           "file_name" : img ,
           "result" : classes_names[result]
        }

        return_objs['result'].append(result_data)

    else:
       raise FileNotFoundError("Images could not be found during model dectection")

    return return_objs

if __name__ == '__main__':
    try:
       print(engine())
    except Exception as e:
       print('Error : ', str(e))