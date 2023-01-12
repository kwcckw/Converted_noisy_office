from glob import glob
import cv2
import os
import io
import random
import zipfile
import requests
import numpy as np

# set random seed for reproducibility
random.seed(10)
cv2.setRNGSeed(10)

# path to the downloaded zip file
noisy_office_zip_path = "NoisyOffice.zip"

with zipfile.ZipFile(noisy_office_zip_path, 'r') as zip_file:
    zip_file.extractall("")
    
# get paths of all clean and noisy images
all_paths_noisy = glob("NoisyOffice/SimulatedNoisyOffice/simulated_noisy_images_grayscale/*")
all_paths_clean = glob("NoisyOffice/SimulatedNoisyOffice/clean_images_grayscale/*")

# randomly sort images
total_images = len(all_paths_noisy)
random_indices = random.sample(range(0, total_images), total_images) 
all_paths_noisy = np.array(all_paths_noisy)
all_paths_noisy = list(all_paths_noisy[random_indices])

# get all name only
noisy_names = [ os.path.basename(cpath) for cpath in all_paths_noisy]
clean_names = [ os.path.basename(cpath) for cpath in all_paths_clean]

# write path for train, validate and test data
write_path_train= "train/train/"
write_path_validate= "validate/validate/"
write_path_test = "test/test/"

# create folders
os.makedirs(write_path_train+"train_noisy")
os.makedirs(write_path_train+"train_cleaned")
os.makedirs(write_path_validate+"validate_noisy")
os.makedirs(write_path_validate+"validate_cleaned")
os.makedirs(write_path_test+"test_noisy")
os.makedirs(write_path_test+"test_cleaned")

# train, validate and test image number
train_number = 144
validate_number = 16
test_number = 56


for i, noisy_name in enumerate(noisy_names):
    # get characters from noisy image for matching purpose
    check_first_7 = noisy_name[:7]
    check_last_3 = noisy_name[-6:]
        
    for j, clean_name in enumerate(clean_names):
        # get characters from clean image for matching purpose
        check_first_7c = clean_name[:7]
        check_last_3c = clean_name[-6:]
    
        # matching noisy and clean image, save them into each folder
        if check_first_7  == check_first_7c and check_last_3 == check_last_3c:
            
            img_noisy = cv2.imread(all_paths_noisy[i])
            img_clean = cv2.imread(all_paths_clean[j])

            if i < train_number:
                write_noisy_path = write_path_train + "train_noisy/"
                write_clean_path = write_path_train + "train_cleaned/"
                
            elif i > train_number and i <= train_number + validate_number:
                write_noisy_path = write_path_validate + "validate_noisy/"
                write_clean_path = write_path_validate + "validate_cleaned/"
            else:
                write_noisy_path = write_path_test + "test_noisy/"
                write_clean_path = write_path_test + "test_cleaned/"

            # save images
            cv2.imwrite(write_noisy_path+noisy_name, img_noisy)
            cv2.imwrite(write_clean_path+noisy_name, img_clean)
             
            
            
            
            
            
            