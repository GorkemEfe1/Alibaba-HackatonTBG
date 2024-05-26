import os
import json
from glob import glob


# Function to split the JSON content based on frame number
def split_json_by_frame(json_path, output_dir):
    # Load the main JSON file
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    # Extract the base name (without extension) to match the frames
    base_name = os.path.basename(json_path).split(".")[0]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create a lookup for annotations by image ID
    annotations_lookup = {}
    for annotation in data.get("annotations", []):
        image_id = annotation["image_id"]
        if image_id not in annotations_lookup:
            annotations_lookup[image_id] = []
        annotations_lookup[image_id].append(annotation)

    # Iterate over each frame in the images section of the JSON
    for image in data.get("images", []):
        frame_number = image["frame_numer"]
        image_id = image["id"]

        # Create a new JSON object for this frame
        frame_data = {
            "info": data["info"],
            "categories": data["categories"],
            "images": [image],  # Only the image data for this frame
            "annotations": annotations_lookup.get(
                image_id, []
            ),  # Annotations for this frame's image
        }

        # Define the output path for this frame's JSON file
        frame_json_path = os.path.join(
            output_dir, f"{base_name}_frame_{frame_number}.json"
        )

        # Save the frame data to a new JSON file
        with open(frame_json_path, "w") as frame_json_file:
            json.dump(frame_data, frame_json_file, indent=4)

        print(f"Created JSON file for frame {frame_number}: {frame_json_path}")


# Define the path to the directory containing the JSON files
for items in [
    "birddog",
    "bicyclecrunch",
    "curl",
    "fly",
    "legraise",
    "pushup",
    "squat",
    "superman",
]:
    json_dir = f"./v1.0/InfinityAI_InfiniteRep_{items}_v1.0/data"
    output_frames_dir = os.path.join(json_dir, "output_frames")

    # Get a list of all JSON files in the directory
    json_files = glob(os.path.join(json_dir, "*.json"))
    print(output_frames_dir)
    print(json_files)

    # Process each JSON file
    for json_file in json_files:
        # Extract the base name to find the corresponding frames directory
        base_name = os.path.basename(json_file).split(".")[0]
        frames_output_dir = os.path.join(output_frames_dir, base_name)

        # Split the JSON file by frame
        split_json_by_frame(json_file, frames_output_dir)
