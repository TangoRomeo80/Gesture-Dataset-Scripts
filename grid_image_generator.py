import os
import matplotlib.pyplot as plt
from PIL import Image

# --- Configuration ---
root_dir = "./gesture_dataset"
view_mode = "full_body"  # or "full_body"
gesture_classes = ['come_here',
                    'fist',
                    'go',
                    'ok_sign',
                    'thumbs_up']  # choose up to 13
target_frames = ['frame_001.png', 'frame_015.png', 'frame_030.png']
n_frames_per_row = 6  # 3 bright + 3 dim

# --- Grid settings ---
n_rows = len(gesture_classes)
n_cols = n_frames_per_row
figsize = (n_cols * 2.2, n_rows * 2.8)

fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

image_counter = 1

for i, gesture in enumerate(gesture_classes):
    frames_root = os.path.join(root_dir, gesture, view_mode, "frames")
    subfolders = sorted(os.listdir(frames_root))

    bright_folder = next((f for f in subfolders if "bright" in f), None)
    dim_folder = next((f for f in subfolders if "dim" in f), None)

    selected_images = []

    for folder in [bright_folder, dim_folder]:
        if folder:
            for frame_name in target_frames:
                frame_path = os.path.join(frames_root, folder, frame_name)
                if os.path.exists(frame_path):
                    selected_images.append(frame_path)
                else:
                    selected_images.append(None)  # Placeholder for missing frame

    # Plot the selected frames (bright first, then dim)
    for j, img_path in enumerate(selected_images):
        ax = axes[i, j] if n_rows > 1 else axes[j]

        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            ax.imshow(img)
        else:
            ax.text(0.5, 0.5, "Missing", ha='center', va='center', fontsize=8)
            ax.set_facecolor('lightgray')

        ax.axis('off')

        # Label image number below
        ax.set_title("")
        ax.text(0.5, -0.05, f"({image_counter})", transform=ax.transAxes,
                ha='center', va='top', fontsize=9)
        image_counter += 1

        # Add gesture label on left
        if j == 0:
            ax.set_ylabel(gesture.replace("_", " "), fontsize=10, rotation=0, labelpad=40, va='center')

# Adjust layout
plt.subplots_adjust(wspace=0.3, hspace=0.6)
plt.tight_layout()
plt.savefig("gesture_grid_bright_dim_full_body.png", dpi=200)
plt.show()
