import os
import shutil
import pandas as pd

# Paths
data_dir = 'data'
label_csv = 'label_csv.csv'
output_dirs = {
    'nofinding': 'output/nofinding',
    'finding': 'output/finding'
}
log_file = 'image_sort_log.txt'

# Create output directories if they don't exist
for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Load labels
df = pd.read_csv(label_csv)

# Normalize column names if needed
df.columns = df.columns.str.lower()
image_col = df.columns[0]
label_col = df.columns[1]

# Open log file
with open(log_file, 'w') as log:
    log.write("ImageName,Labels,Category,Status\n")
    
    # Process each image
    for index, row in df.iterrows():
        image_name = row[image_col]
        labels = str(row[label_col]).split('|')

        # Determine the category based on label
        if labels == ['No Finding']:
            category = 'nofinding'
        else:
            category = 'finding'

        # Search in each subdirectory/images/
        found = False
        for subfolder in range(1, 13):
            folder_name = f'images_{subfolder:03d}'
            image_path = os.path.join(data_dir, folder_name, 'images', image_name)
            if os.path.isfile(image_path):
                shutil.copy(image_path, output_dirs[category])
                log.write(f"{image_name},{'|'.join(labels)},{category},Copied\n")
                found = True
                break

        if not found:
            log.write(f"{image_name},{'|'.join(labels)},N/A,Not Found\n")
            print(f"Warning: {image_name} not found in any subdirectory.")

print("Done sorting images. Log written to image_sort_log.txt.")

