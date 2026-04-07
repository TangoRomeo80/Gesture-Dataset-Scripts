import os
import subprocess

def extract_frames_with_ffmpeg(base_path, fps=1):
    """
    Walk every gesture → modality → videos folder and:
      - extract frames at `fps` into the matching modality/frames/<video_name>/ directory
    """
    for gesture in os.listdir(base_path):
        gesture_dir = os.path.join(base_path, gesture)
        if not os.path.isdir(gesture_dir):
            continue

        # for each modality (hand_only, full_body, etc.)
        for modality in os.listdir(gesture_dir):
            videos_dir = os.path.join(gesture_dir, modality, "videos")
            frames_base = os.path.join(gesture_dir, modality, "frames")

            if not os.path.isdir(videos_dir):
                continue

            for fname in os.listdir(videos_dir):
                if not fname.lower().endswith(".mp4"):
                    continue

                video_path = os.path.join(videos_dir, fname)
                video_name = os.path.splitext(fname)[0]
                out_dir    = os.path.join(frames_base, video_name)
                os.makedirs(out_dir, exist_ok=True)

                cmd = [
                    "ffmpeg",
                    "-i", video_path,
                    "-vf", f"fps={fps}",
                    os.path.join(out_dir, "frame_%03d.png")
                ]

                print("Running:", " ".join(cmd))
                subprocess.run(cmd, check=True)


if __name__ == "__main__":
    # e.g. root of your dataset  
    dataset_path = "gesture_dataset"
    extract_frames_with_ffmpeg(dataset_path, fps=30)
