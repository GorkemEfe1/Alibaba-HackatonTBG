import os
import json
from glob import glob
import csv

ec = 0
check = 0
os.makedirs("./csv", exist_ok=True)

# Keypoint labels
keypoint_labels = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

# Initialize lists to store keypoints for each category
pushup_keypoints = []
squat_keypoints = []


# Function to normalize values
def normalize(value, max_value):
    end = value / max_value
    if end > 1:
        return 1
    elif end < 0:
        return 0
    return end


# Function to process each JSON file and extract keypoints
def conv_txt(json_path, ix, items, nn):
    global ec
    global check
    # Load the main JSON file
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    annotations = data["annotations"]
    images = data["images"]
    image_info = {img["id"]: img for img in images}

    try:
        for annotation in annotations:
            image_id = annotation["image_id"]
            image = image_info[image_id]
            img_width = image["width"]
            img_height = image["height"]

            category_id = annotation["category_id"]
            if category_id != 0:
                continue

            keypoints = annotation["keypoints"]

            keypoints_normalized = []
            for i in range(0, len(keypoints), 3):
                x = normalize(keypoints[i], img_width)
                y = normalize(keypoints[i + 1], img_height)
                keypoints_normalized.extend([x, y])

            # Add the normalized keypoints to the respective list
            if items == "pushup":
                pushup_keypoints.append(keypoints_normalized)
            elif items == "squat":
                squat_keypoints.append(keypoints_normalized)

    except Exception as e:
        print(f"Error processing file {json_path}: {e}")
        check = ec
        ec += 1

    if check < ec:
        print(ec)


# Define the path to the directory containing the JSON files
for ix, items in enumerate(["pushup", "squat"]):
    json_dir = f"./v1.0/InfinityAI_InfiniteRep_{items}_v1.0/data/output_frames/*/*.json"
    jsons = glob(json_dir)
    for json_path in jsons:
        nn = json_path.split("\\")[-1].split(".")[0]
        conv_txt(json_path, ix, items, nn)


# Write keypoints to CSV files
def write_keypoints_to_csv(filename, keypoints):
    header = []
    for label in keypoint_labels:
        header.extend([f"{label}_x", f"{label}_y"])

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write header
        writer.writerows(keypoints)  # Write keypoints


write_keypoints_to_csv("./csv/pushup_keypoints.csv", pushup_keypoints)
write_keypoints_to_csv("./csv/squat_keypoints.csv", squat_keypoints)
