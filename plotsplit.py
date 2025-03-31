import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def visualize_data_distribution(data_dir, save_plots=True):
    """
    Create visualizations showing the distribution of images between training and testing sets.
    
    Args:
        data_dir (str): Path to the main 'sorted' directory
        save_plots (bool): Whether to save plots to files (default: True)
    """
    train_dir = Path(data_dir) / 'training'
    test_dir = Path(data_dir) / 'testing'
    
    if not train_dir.exists() or not test_dir.exists():
        print("Error: Could not find both 'training' and 'testing' directories.")
        print("Please make sure you've run the data splitting script first.")
        return
    
    # Get all class names
    class_names = [d.name for d in train_dir.iterdir() if d.is_dir()]
    class_names.sort()
    
    # Initialize counts
    train_counts = []
    test_counts = []
    total_train = 0
    total_test = 0
    
    # Count images in each class
    for class_name in class_names:
        train_class_dir = train_dir / class_name
        test_class_dir = test_dir / class_name
        
        train_count = len([f for f in train_class_dir.iterdir() if f.is_file()])
        test_count = len([f for f in test_class_dir.iterdir() if f.is_file()])
        
        train_counts.append(train_count)
        test_counts.append(test_count)
        total_train += train_count
        total_test += test_count
    
    # Create output directory if saving plots
    if save_plots:
        output_dir = Path(data_dir) / 'visualizations'
        output_dir.mkdir(exist_ok=True)
    
    # 1. Side-by-side Bar Graph
    plt.figure(figsize=(14, 7))
    bar_width = 0.35
    index = np.arange(len(class_names))
    
    # Create bars
    train_bars = plt.bar(index, train_counts, bar_width, label='Training', color='#3498db')
    test_bars = plt.bar(index + bar_width, test_counts, bar_width, label='Testing', color='#e74c3c')
    
    # Add labels and title
    plt.xlabel('Classes', fontsize=12)
    plt.ylabel('Number of Images', fontsize=12)
    plt.title('Training vs Testing Data Distribution by Class', fontsize=14, pad=20)
    plt.xticks(index + bar_width/2, class_names, rotation=45, ha='right')
    plt.legend()
    
    # Add value labels on bars
    for bar in train_bars + test_bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',
                 ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_plots:
        plt.savefig(output_dir / 'class_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Pie Chart of Overall Distribution
    plt.figure(figsize=(8, 8))
    sizes = [total_train, total_test]
    labels = [f'Training\n{total_train} images',
              f'Testing\n{total_test} images']
    colors = ['#3498db', '#e74c3c']
    explode = (0.05, 0)  # Explode the training slice slightly
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            shadow=True, startangle=90,
            textprops={'fontsize': 12})
    plt.title('Overall Training vs Testing Distribution', fontsize=14, pad=20)
    
    if save_plots:
        plt.savefig(output_dir / 'overall_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Stacked Bar Graph
    plt.figure(figsize=(14, 7))
    p1 = plt.bar(class_names, train_counts, color='#3498db', label='Training')
    p2 = plt.bar(class_names, test_counts, bottom=train_counts, color='#e74c3c', label='Testing')
    
    # Add value labels
    for i, (train, test) in enumerate(zip(train_counts, test_counts)):
        plt.text(i, train/2, f'{train}',
                 ha='center', va='center', color='white', fontweight='bold')
        plt.text(i, train + test/2, f'{test}',
                 ha='center', va='center', color='white', fontweight='bold')
    
    plt.xlabel('Classes', fontsize=12)
    plt.ylabel('Number of Images', fontsize=12)
    plt.title('Stacked Training vs Testing Distribution by Class', fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    if save_plots:
        plt.savefig(output_dir / 'stacked_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    data_directory = "sorted"  # Path to your sorted directory
    
    if not os.path.exists(data_directory):
        print(f"Error: Directory '{data_directory}' not found.")
    else:
        visualize_data_distribution(data_directory, save_plots=True)
        print("Visualizations created successfully!")
