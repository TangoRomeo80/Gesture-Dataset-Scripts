# import os
# import matplotlib.pyplot as plt
# from PIL import Image

# # --- Configuration ---
# root_dir = "./Root"
# view_mode = "full_body"  # or "full_body"
# gesture_classes = ['come_here',
#                     'fist',
#                     'go',
#                     'ok_sign',
#                     'thumbs_up']  # choose up to 13
# target_frames = ['frame_001.png', 'frame_015.png', 'frame_030.png']
# n_frames_per_row = 6  # 3 bright + 3 dim

# # --- Grid settings ---
# n_rows = len(gesture_classes)
# n_cols = n_frames_per_row
# figsize = (n_cols * 2.2, n_rows * 2.8)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

# image_counter = 1

# for i, gesture in enumerate(gesture_classes):
#     frames_root = os.path.join(root_dir, gesture, view_mode, "frames")
#     subfolders = sorted(os.listdir(frames_root))

#     bright_folder = next((f for f in subfolders if "bright" in f), None)
#     dim_folder = next((f for f in subfolders if "dim" in f), None)

#     selected_images = []

#     for folder in [bright_folder, dim_folder]:
#         if folder:
#             for frame_name in target_frames:
#                 frame_path = os.path.join(frames_root, folder, frame_name)
#                 if os.path.exists(frame_path):
#                     selected_images.append(frame_path)
#                 else:
#                     selected_images.append(None)  # Placeholder for missing frame

#     # Plot the selected frames (bright first, then dim)
#     for j, img_path in enumerate(selected_images):
#         ax = axes[i, j] if n_rows > 1 else axes[j]

#         if img_path and os.path.exists(img_path):
#             img = Image.open(img_path)
#             ax.imshow(img)
#         else:
#             ax.text(0.5, 0.5, "Missing", ha='center', va='center', fontsize=8)
#             ax.set_facecolor('lightgray')

#         ax.axis('off')

#         # Label image number below
#         ax.set_title("")
#         ax.text(0.5, -0.05, f"({image_counter})", transform=ax.transAxes,
#                 ha='center', va='top', fontsize=9)
#         image_counter += 1

#         # Add gesture label on left
#         if j == 0:
#             ax.set_ylabel(gesture.replace("_", " "), fontsize=10, rotation=0, labelpad=40, va='center')

# # Adjust layout
# plt.subplots_adjust(wspace=0.3, hspace=0.6)
# plt.tight_layout()
# plt.savefig("gesture_grid_bright_dim_full_body.png", dpi=200)
# plt.show()

import os
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

# --- Configuration ---
root_dir = "./Root"
view_mode = "hand_only"  # "full_body" or "hand_only"

gesture_classes = [
    "come_here",
    "fist",
    "go",
    "ok_sign",
    "thumbs_up"
]

target_frames = ["frame_001.png", "frame_015.png", "frame_030.png"]

# Bright 3 frames + dim 3 frames = 6 columns
conditions = ["bright", "dim"]
n_cols = len(conditions) * len(target_frames)
n_rows = len(gesture_classes)

# Larger physical figure size
# This matters because LaTeX will shrink the whole figure.
fig_width = n_cols * 2.6
fig_height = n_rows * 2.4

fig, axes = plt.subplots(
    n_rows,
    n_cols,
    figsize=(fig_width, fig_height),
    constrained_layout=False
)

# Handle single-row case safely
if n_rows == 1:
    axes = [axes]

image_counter = 1

for i, gesture in enumerate(gesture_classes):
    frames_root = os.path.join(root_dir, gesture, view_mode, "frames")

    if not os.path.exists(frames_root):
        print(f"Missing folder: {frames_root}")
        continue

    subfolders = sorted(os.listdir(frames_root))

    bright_folder = next((f for f in subfolders if "bright" in f.lower()), None)
    dim_folder = next((f for f in subfolders if "dim" in f.lower()), None)

    selected_images = []

    for folder in [bright_folder, dim_folder]:
        if folder:
            for frame_name in target_frames:
                frame_path = os.path.join(frames_root, folder, frame_name)
                selected_images.append(frame_path if os.path.exists(frame_path) else None)
        else:
            selected_images.extend([None] * len(target_frames))

    for j, img_path in enumerate(selected_images):
        ax = axes[i][j] if n_rows > 1 else axes[j]

        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            img = ImageOps.exif_transpose(img)
            ax.imshow(img)
        else:
            ax.text(
                0.5, 0.5, "Missing",
                ha="center",
                va="center",
                fontsize=13,
                fontweight="bold"
            )
            ax.set_facecolor("lightgray")

        ax.axis("off")

        # Put image number INSIDE the image with a white box
        ax.text(
            0.04,
            0.92,
            f"({image_counter})",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=14,
            fontweight="bold",
            color="black",
            bbox=dict(
                facecolor="white",
                edgecolor="black",
                boxstyle="round,pad=0.25",
                alpha=0.90
            )
        )

        image_counter += 1

        # Row label on the left side
        if j == 0:
            ax.text(
                -0.18,
                0.5,
                gesture.replace("_", " ").title(),
                transform=ax.transAxes,
                ha="right",
                va="center",
                fontsize=15,
                fontweight="bold",
                rotation=0
            )

        # Column headers only on top row
        if i == 0:
            if j < len(target_frames):
                header = f"Bright\n{target_frames[j].replace('.png', '')}"
            else:
                idx = j - len(target_frames)
                header = f"Dim\n{target_frames[idx].replace('.png', '')}"

            ax.set_title(
                header,
                fontsize=14,
                fontweight="bold",
                pad=10
            )

# Layout tuning
plt.subplots_adjust(
    left=0.14,
    right=0.99,
    top=0.92,
    bottom=0.03,
    wspace=0.04,
    hspace=0.16
)

output_base = f"gesture_grid_{view_mode}_clear"

plt.savefig(f"{output_base}.png", dpi=500, bbox_inches="tight", pad_inches=0.05)
plt.savefig(f"{output_base}.pdf", bbox_inches="tight", pad_inches=0.05)

plt.show()