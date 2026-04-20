import shutil
import tarfile
import subprocess
from pathlib import Path


RAW_SCARED_ROOT = Path("/l/users/omar.mohamed/datasets/SCARED")
OUTPUT_ROOT = Path("/l/users/omar.mohamed/datasets/SCARED_prepared")


def dataset_id_to_raw_name(dataset_id: int) -> str:
    return f"dataset_{dataset_id}"


def keyframe_id_to_raw_name(keyframe_id: int) -> str:
    return f"keyframe_{keyframe_id}"


def dataset_id_to_prepared_name(dataset_id: int) -> str:
    return f"dataset{dataset_id}"


def keyframe_id_to_prepared_name(keyframe_id: int) -> str:
    return f"keyframe{keyframe_id}"


def split_name_for_dataset(dataset_id: int) -> str:
    return "train" if dataset_id < 8 else "test"


def extract_tar_if_needed(tar_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    if not tar_path.exists():
        print(f"[skip] missing archive: {tar_path}")
        return

    if any(output_dir.iterdir()):
        print(f"[skip] already extracted: {output_dir}")
        return

    print(f"[extract] {tar_path} -> {output_dir}")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=output_dir)


def copy_file_if_needed(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        print(f"[skip] already exists: {dst}")
        return

    print(f"[copy] {src} -> {dst}")
    shutil.copy2(src, dst)


def prepare_one_keyframe(dataset_id: int, keyframe_id: int) -> None:
    raw_dataset = dataset_id_to_raw_name(dataset_id)
    raw_keyframe = keyframe_id_to_raw_name(keyframe_id)

    prepared_dataset = dataset_id_to_prepared_name(dataset_id)
    prepared_keyframe = keyframe_id_to_prepared_name(keyframe_id)

    split = split_name_for_dataset(dataset_id)

    raw_keyframe_root = RAW_SCARED_ROOT / raw_dataset / raw_keyframe
    raw_data_dir = raw_keyframe_root / "data"

    prepared_keyframe_root = OUTPUT_ROOT / split / prepared_dataset / prepared_keyframe
    prepared_data_dir = prepared_keyframe_root / "data"

    left_dir = prepared_data_dir / "left"
    right_dir = prepared_data_dir / "right"
    scene_points_dir = prepared_data_dir / "scene_points"
    frame_data_dir = prepared_data_dir / "frame_data"

    left_dir.mkdir(parents=True, exist_ok=True)
    right_dir.mkdir(parents=True, exist_ok=True)
    scene_points_dir.mkdir(parents=True, exist_ok=True)
    frame_data_dir.mkdir(parents=True, exist_ok=True)

    # Extract archives
    extract_tar_if_needed(raw_data_dir / "scene_points.tar.gz", scene_points_dir)
    extract_tar_if_needed(raw_data_dir / "frame_data.tar.gz", frame_data_dir)

    # Copy static files that may be useful later
    static_files = [
        "Left_Image.png",
        "Right_Image.png",
        "left_depth_map.tiff",
        "right_depth_map.tiff",
        "point_cloud.obj",
        "left_point_cloud.obj",
        "right_point_cloud.obj",
        "endoscope_calibration.yaml",
        "README.txt",
    ]
    for name in static_files:
        src = raw_keyframe_root / name
        if src.exists():
            copy_file_if_needed(src, prepared_keyframe_root / name)

    # Keep original RGB video too, and extract frames for EndoMUST
    rgb_video = raw_data_dir / "rgb.mp4"
    if rgb_video.exists():
        copy_file_if_needed(rgb_video, prepared_data_dir / "rgb.mp4")
        extract_rgb_frames_if_needed(rgb_video, left_dir)

def extract_rgb_frames_if_needed(video_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    if not video_path.exists():
        print(f"[skip] missing video: {video_path}")
        return

    if any(output_dir.iterdir()):
        print(f"[skip] frames already extracted: {output_dir}")
        return

    print(f"[extract] {video_path} -> {output_dir}")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-start_number",
        "1",
        str(output_dir / "%010d.png"),
    ]
    subprocess.run(cmd, check=True)

def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "train").mkdir(exist_ok=True)
    (OUTPUT_ROOT / "test").mkdir(exist_ok=True)

    print("Raw dataset root:", RAW_SCARED_ROOT)
    print("Prepared dataset root:", OUTPUT_ROOT)

    for dataset_id in range(1, 11):
        for keyframe_id in range(1, 6):
            raw_keyframe_root = (
                RAW_SCARED_ROOT
                / dataset_id_to_raw_name(dataset_id)
                / keyframe_id_to_raw_name(keyframe_id)
            )
            if not raw_keyframe_root.exists():
                print(f"[skip] missing: {raw_keyframe_root}")
                continue

            print(f"\n=== Preparing dataset{dataset_id}/keyframe{keyframe_id} ===")
            prepare_one_keyframe(dataset_id, keyframe_id)

    print("\nDone.")


if __name__ == "__main__":
    main()