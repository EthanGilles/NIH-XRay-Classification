import os
import matplotlib.pyplot as plt
import argparse
import numpy as np

def count_images_and_plot(directory_path, output_graph_path='label_distribution.png'):
    """
    Counts images in each subdirectory and creates a rainbow-colored bar chart.
    
    Args:
        directory_path (str): Path to directory containing label subdirectories
        output_graph_path (str): Path to save the output graph image
    """
    # Count images in each subdirectory
    label_counts = {}
    
    for label in os.listdir(directory_path):
        label_dir = os.path.join(directory_path, label)
        if os.path.isdir(label_dir):
            num_images = len([f for f in os.listdir(label_dir) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
            if num_images > 0:
                label_counts[label] = num_images

    if not label_counts:
        print("No images found in subdirectories!")
        return

    # Sort by count (descending)
    sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [x[0] for x in sorted_labels]
    counts = [x[1] for x in sorted_labels]

    # Create figure with rainbow colors
    plt.figure(figsize=(12, 6))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(labels)))
    bars = plt.bar(labels, counts, color=colors)
    
    # Add count labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
               f'{int(height)}',
               ha='center', va='bottom', fontsize=9)

    plt.xlabel('Labels', fontweight='bold')
    plt.ylabel('Number of Images', fontweight='bold')
    plt.title('Image Distribution Across Labels', fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Save and show
    plt.savefig(output_graph_path, dpi=300, bbox_inches='tight')
    print(f"Rainbow-colored graph saved to {output_graph_path}")
    plt.show()

    # Print summary
    print("\nLabel Distribution Summary:")
    for label, count in sorted_labels:
        print(f"{label}: {count} images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create rainbow-colored bar chart of image distribution.')
    parser.add_argument('--directory', required=True, help='Path to label directories')
    parser.add_argument('--output', default='label_distribution.png', help='Output graph path')
    args = parser.parse_args()

    count_images_and_plot(args.directory, args.output)
