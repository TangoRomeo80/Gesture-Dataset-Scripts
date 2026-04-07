import os
import csv

def generate_labels_csv(base_path, output_file="labels.csv"):
    rows = []
    # find all gesture folders
    gestures = [
        d for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d))
    ]

    for gesture in gestures:
        gesture_dir = os.path.join(base_path, gesture)
        # loop over each modality inside the gesture
        for modality in os.listdir(gesture_dir):
            mod_dir = os.path.join(gesture_dir, modality)
            videos_path = os.path.join(mod_dir, "videos")
            frames_base = os.path.join(gesture, modality, "frames")
            if not os.path.isdir(videos_path):
                continue

            for file in os.listdir(videos_path):
                if not file.lower().endswith(".mp4"):
                    continue

                video_name = os.path.splitext(file)[0]
                prefix = f"{gesture}_"
                if not video_name.startswith(prefix):
                    print(f"Skipping, unexpected format: {file}")
                    continue

                # Remove the leading "gesture_"
                remainder = video_name[len(prefix):]  
                parts = remainder.split("_")
                # expect parts like ["p01", "bright", "01", "hand", "only"] or ["p01", "bright", "01", "full", "body"]
                if len(parts) < 5:
                    print(f"Skipping, too few parts: {file}")
                    continue

                participant = parts[0].lstrip("p")
                lighting   = parts[1]
                take       = parts[2]
                # modality might also be derivable from parts[3:] but we already know it from folder
                frames_path = os.path.join(frames_base, video_name)

                rows.append([
                    file,           # filename
                    gesture,        # gesture class
                    participant,    # participant ID
                    lighting,       # lighting condition
                    take,           # take number
                    modality,       # hand_only / full_body
                    frames_path,    # path to extracted frames
                ])

    # write out the CSV
    csv_path = os.path.join(base_path, output_file)
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename",
            "gesture",
            "participant",
            "lighting",
            "take",
            "modality",
            "frames_path"
        ])
        writer.writerows(rows)

    print(f"Saved metadata to {csv_path}")

if __name__ == "__main__":
    generate_labels_csv("gesture_dataset")
