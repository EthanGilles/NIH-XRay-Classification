import os
import shutil
import random
from pathlib import Path

def split_images(source_dir, train_ratio=0.85):
    """
    Split images into training and testing sets while maintaining directory structure.
    
    Args:
        source_dir (str): Path to the main directory containing class subdirectories
        train_ratio (float): Ratio of images to use for training (default: 0.85)
    """
    base_dir = Path(source_dir).parent
    train_dir = base_dir / 'sorted' / 'training'
    test_dir = base_dir / 'sorted' / 'testing'
    
    # Create train and test directories if they don't exist
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    for class_name in os.listdir(source_dir):
        class_path = Path(source_dir) / class_name
        
        # Skip if not a directory
        if not class_path.is_dir():
            continue
            
        print(f"Processing class: {class_name}")
        
        train_class_dir = train_dir / class_name
        test_class_dir = test_dir / class_name
        train_class_dir.mkdir(exist_ok=True)
        test_class_dir.mkdir(exist_ok=True)
        
        images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        random.shuffle(images)  # Shuffle to ensure random distribution
        
        split_idx = int(len(images) * train_ratio)
        
        train_images = images[:split_idx]
        test_images = images[split_idx:]
        
        for img in train_images:
            src = class_path / img
            dst = train_class_dir / img
            shutil.copy2(src, dst)
            
        for img in test_images:
            src = class_path / img
            dst = test_class_dir / img
            shutil.copy2(src, dst)
            
        print(f"  {len(train_images)} images copied to training")
        print(f"  {len(test_images)} images copied to testing")

if __name__ == "__main__":
    # Assuming the script is in the same directory as the 'sorted' folder
    source_directory = "sorted"  # This should contain subdirectories for each class
    
    if not os.path.exists(source_directory):
        print(f"Error: Directory '{source_directory}' not found.")
        print("Please make sure the script is in the correct location relative to your 'sorted' folder.")
    else:
        split_images(source_directory)
        print("Dataset splitting completed successfully!")
