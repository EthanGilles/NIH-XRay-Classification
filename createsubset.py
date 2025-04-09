import os
import shutil
import random
from pathlib import Path

def create_subset(src_dir: str, dest_dir: str, fraction: float = 0.1):
    """
    Creates a subset of the dataset located in src_dir, copying only a fraction of the images
    into dest_dir while maintaining the same directory structure.
    
    Args:
        src_dir (str): Path to the original dataset root directory (e.g., "sorted").
        dest_dir (str): Path to the new subset dataset root directory (e.g., "sorted_subset").
        fraction (float): Fraction of images to include in the subset.
    """
    subsets = ['training', 'testing']
    labels = ['finding', 'nofinding']
    
    for subset in subsets:
        for label in labels:
            src_path = Path(src_dir) / subset / label
            dest_path = Path(dest_dir) / subset / label
            dest_path.mkdir(parents=True, exist_ok=True)

            all_images = list(src_path.glob("*"))
            num_to_copy = max(1, int(len(all_images) * fraction))

            sampled_images = random.sample(all_images, num_to_copy)

            for image_path in sampled_images:
                shutil.copy(image_path, dest_path / image_path.name)

            print(f"Copied {num_to_copy} images to {dest_path}")

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    create_subset("sorted", "sorted_subset", fraction=0.1)

