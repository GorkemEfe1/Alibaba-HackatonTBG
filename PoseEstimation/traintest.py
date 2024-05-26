import os
import shutil
from collections import defaultdict
from sklearn.model_selection import train_test_split

# Directory paths
train_dir = "./train/"
val_dir = "./val/"
trainimages_dir = "./train/images/"
trainlabels_dir = "./train/labels/"
valimages_dir = "./val/images/"
vallabels_dir = "./val/labels/"

# Create train and val directories if not exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(trainimages_dir, exist_ok=True)
os.makedirs(trainlabels_dir, exist_ok=True)
os.makedirs(valimages_dir, exist_ok=True)
os.makedirs(vallabels_dir, exist_ok=True)

# List of images and labels
oldimages = os.listdir("./images/")
oldlabels = os.listdir("./labels/")

# Dictionary to hold segments and their corresponding images and labels
data_dict = defaultdict(list)

# Populate the dictionary with segments
for image in oldimages:
    # Extract class and segment information from the filename
    parts = image.split("_")
    class_segment = "_".join(parts[:2])  # e.g., class1_segment1
    print(class_segment)
    data_dict[class_segment].append(image)

# Split the segments into train and val sets
segments = list(data_dict.keys())
train_segments, val_segments = train_test_split(
    segments, train_size=0.8, random_state=42
)


# Function to move files
def move_files(file_list, src_dir, dst_dir):
    for file in file_list:
        if os.path.exists(os.path.join(src_dir, file)):
            shutil.move(os.path.join(src_dir, file), os.path.join(dst_dir, file))


# Move files to their respective directories
for segment in train_segments:
    images = data_dict[segment]
    labels = [img.replace(".jpg", ".txt") for img in images]
    move_files(images, "./images", trainimages_dir)
    move_files(labels, "./labels", trainlabels_dir)

for segment in val_segments:
    images = data_dict[segment]
    labels = [img.replace(".jpg", ".txt") for img in images]
    move_files(images, "./images", valimages_dir)
    move_files(labels, "./labels", vallabels_dir)

print("Dataset split into train and val sets successfully.")
