import os
import shutil
import random

def split_data(main_dir, train_dir, test_dir, split_ratio=0.9):
    # Create the necessary directories if they don't exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Loop over each label folder (sub-directory) in the main directory
    for label in os.listdir(main_dir):
        label_path = os.path.join(main_dir, label)
        
        if os.path.isdir(label_path):
            # Create label directories inside training and testing directories
            train_label_dir = os.path.join(train_dir, label)
            test_label_dir = os.path.join(test_dir, label)
            
            if not os.path.exists(train_label_dir):
                os.makedirs(train_label_dir)
            if not os.path.exists(test_label_dir):
                os.makedirs(test_label_dir)
            
            # Get all image files in the current label folder
            images = [f for f in os.listdir(label_path) if os.path.isfile(os.path.join(label_path, f))]
            
            # Shuffle images to ensure random distribution
            random.shuffle(images)
            
            # Split images into training and testing sets
            split_index = int(len(images) * split_ratio)
            train_images = images[:split_index]
            test_images = images[split_index:]
            
            # Move images to the corresponding folders
            for image in train_images:
                src = os.path.join(label_path, image)
                dst = os.path.join(train_label_dir, image)
                shutil.move(src, dst)
            
            for image in test_images:
                src = os.path.join(label_path, image)
                dst = os.path.join(test_label_dir, image)
                shutil.move(src, dst)

if __name__ == "__main__":
    main_directory = "output"  # Replace with the path to your main directory
    sorted_directory = "sorted"  # Replace with the desired path for sorted data
    training_directory = os.path.join(sorted_directory, "training")
    testing_directory = os.path.join(sorted_directory, "testing")
    
    split_data(main_directory, training_directory, testing_directory)
    print("Data has been split into training and testing sets.")