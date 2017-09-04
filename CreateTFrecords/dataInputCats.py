from PIL import Image  #pip install pillow
import numpy as np
import skimage.io as io #pip install scikit_image
import tensorflow as tf #pip install tensorflow
import os
import sys

#Path to our working directory
dir_path = os.getcwd()

#Path to subdirectory with images; finds extensions jpeg and such
relevant_path = os.path.join(dir_path,"cats")
included_extensions = ('.jpg', '.jpeg', '.bmp', '.png', '.gif')
file_names = [fn for fn in os.listdir(relevant_path)
              if fn.endswith(included_extensions)]
file_paths = [os.path.join(relevant_path,fn) for fn in file_names]


####################################################
### WRITE TO TENSORFLOW FORMAT
####################################################

#come back later to this
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# The filename to be written to
tfrecords_filename = 'pascal_voc_segmentation.tfrecords'

# Predefined function by tensorflow, to obtain standard formatted data
writer = tf.python_io.TFRecordWriter(tfrecords_filename)

# Let's collect the real images to later on compare
# to the reconstructed ones
original_images = []

for img_path in file_paths:

    #Open the image
    img = np.array(Image.open(img_path))
    
    # The reason to store image sizes was demonstrated
    # in the previous example -- we have to know sizes
    # of images to later read raw serialized string,
    # convert to 1d array and convert to respective
    # shape that image used to have.
    height = img.shape[0]
    width = img.shape[1]
    
    # Put in the original images into array
    # Just for future check for correctness
    original_images.append(img)
    
    img_raw = img.tostring()
    
    example = tf.train.Example(features=tf.train.Features(feature={
        'height': _int64_feature(height),
        'width': _int64_feature(width),
        'image_raw': _bytes_feature(img_raw)}))
    
    writer.write(example.SerializeToString())

writer.close()

########################################################
####### TRANSFORM BACK
########################################################

reconstructed_images = []

record_iterator = tf.python_io.tf_record_iterator(path=tfrecords_filename)

for string_record in record_iterator:
    
    example = tf.train.Example()
    example.ParseFromString(string_record)
    
    height = int(example.features.feature['height']
                                 .int64_list
                                 .value[0])
    
    width = int(example.features.feature['width']
                                .int64_list
                                .value[0])
    
    img_string = (example.features.feature['image_raw']
                                  .bytes_list
                                  .value[0])
        
    img_1d = np.fromstring(img_string, dtype=np.uint8)
    reconstructed_img = img_1d.reshape((height, width, -1))
    
    reconstructed_images.append(reconstructed_img)


###########################################################
########## SEE IF THEY ARE EQUAL
###########################################################

for original, reconstructed in zip(original_images,
                                             reconstructed_images):
    
    img_pair_to_compare = (original, reconstructed)
    print(np.allclose(*img_pair_to_compare))

sys.stdout.flush()


############## TO GO FURTHER, WE NEED IMAGES OF THE SAME SIZE


##cat_img = io.imread('cat.jpg')
##
##io.imshow(cat_img)
##io.show()
##
### Let's convert the picture into string representation
### using the ndarray.tostring() function 
##cat_string = cat_img.tostring()
##
### Now let's convert the string back to the image
### Important: the dtype should be specified
### otherwise the reconstruction will be errorness
### Reconstruction is 1d, so we need sizes of image
### to fully reconstruct it.
##reconstructed_cat_1d = np.fromstring(cat_string, dtype=np.uint8)
##
### Here we reshape the 1d representation
### This is the why we need to store the sizes of image
### along with its serialized representation.
##reconstructed_cat_img = reconstructed_cat_1d.reshape(cat_img.shape)
##
### Let's check if we got everything right and compare
### reconstructed array to the original one.
##np.allclose(cat_img, reconstructed_cat_img)
