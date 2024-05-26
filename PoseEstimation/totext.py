import os
import json
from glob import glob
import shutil

ec = 0
check = 0
os.makedirs("./images", exist_ok=True)
os.makedirs("./labels", exist_ok=True)


# Function to split the JSON content based on frame number
def conv_txt(json_path, ix, items, nn):
    global ec
    global check
    # Load the main JSON file
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    annotations = data["annotations"]
    images = data["images"]
    image_info = {img["id"]: img for img in images}

    def normalize(value, max_value):
        end = value / max_value
        if end > 1:
            return 1
        elif end < 0:
            return 0
        return end

    txt_dir = "./labels/"
    img_dir = "./images/"
    txt_filename = os.path.join(txt_dir, f"{items}_{nn}.txt")
    img_filename = os.path.join(img_dir, f"{items}_{nn}.jpg")
    try:
        for annotation in annotations:

            image_id = annotation["image_id"]
            image = image_info[image_id]
            img_width = image["width"]
            img_height = image["height"]

            category_id = annotation["category_id"]
            if category_id != 0:
                continue
            bbox = annotation["bbox"]  # [x, y, width, heigh*t]
            keypoints = annotation["keypoints"]

            x_center = normalize(bbox[0] + bbox[2] / 2, img_width)
            y_center = normalize(bbox[1] + bbox[3] / 2, img_height)
            width = normalize(bbox[2], img_width)
            height = normalize(bbox[3], img_height)

            keypoints_normalized = []
            for i in range(0, len(keypoints), 3):
                keypoints_normalized.extend(
                    [
                        (
                            normalize(keypoints[i], img_width),
                            normalize(keypoints[i + 1], img_height),
                        )
                    ]
                )
            print(keypoints_normalized)

        # shutil.copyfile(json_path.replace(".json", ".jpg"), img_filename)

    except:
        check = ec
        ec += 1

    if check < ec:
        print(ec)


# Extract the base name (without extension) to match the frames


# Define the path to the directory containing the JSON files
for ix, items in enumerate(
    [
        "pushup",  # 100
        "squat",  # 101
    ]
):
    json_dir = f"./v1.0/InfinityAI_InfiniteRep_{items}_v1.0/data/output_frames/*/*.json"
    jsons = glob(json_dir)
    for json_path in jsons:
        nn = json_path.split("\\")[-1].split(".")[0]
        conv_txt(json_path, ix, items, nn)
