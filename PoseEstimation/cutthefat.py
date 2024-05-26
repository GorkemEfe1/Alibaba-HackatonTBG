import os


def process_folder(folder_path):
    images_folder = os.path.join(folder_path, "images")
    labels_folder = os.path.join(folder_path, "labels")

    # Ensure both images and labels folders exist
    if not os.path.exists(images_folder) or not os.path.exists(labels_folder):
        print(f"Error: Images or labels folder missing in {folder_path}")
        return

    image_files = sorted(os.listdir(images_folder))
    label_files = sorted(os.listdir(labels_folder))

    # Ensure there are the same number of image and label files
    if len(image_files) != len(label_files):
        print("Error: Number of image files does not match number of label files.")
        return

    # Process every 10th image
    for i in range(0, len(image_files)):
        image_file = image_files[i]
        label_file = label_files[i]

        # Construct full paths
        image_path = os.path.join(images_folder, image_file)
        label_path = os.path.join(labels_folder, label_file)
        # Delete non-10th images and corresponding labels
        if i % 10 != 9:
            os.remove(image_path)
            os.remove(label_path)


# Process train folder
train_folder = "./data/train"
process_folder(train_folder)

# Process val folder
val_folder = "./data/val"
process_folder(val_folder)
