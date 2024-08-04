import os
from datetime import datetime, timedelta

# Directory to start from
start_dir = 'capa-rules'
output_file = 'file_modification_dates.txt'

# Current date
current_date = datetime.now()

# Date thresholds
three_months_ago = current_date - timedelta(days=90)
start_of_year = datetime(current_date.year, 1, 1)

# Function to get all yml files and their last modified dates
def get_yml_files_and_dates(start_dir):
    yml_files = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                last_modified_date = os.path.getmtime(file_path)
                yml_files.append((file_path, last_modified_date))
    return yml_files

# Get the yml files and their dates
yml_files_and_dates = get_yml_files_and_dates(start_dir)

# Sort files by last modified date (most recent first)
yml_files_and_dates.sort(key=lambda x: x[1], reverse=True)

# Categorize files
new_files = []
recent_files = []
this_year_files = []
older_files = []

for file_path, last_modified_date in yml_files_and_dates:
    last_modified_date_dt = datetime.fromtimestamp(last_modified_date)
    if last_modified_date_dt > three_months_ago:
        recent_files.append((file_path, last_modified_date))
    elif last_modified_date_dt > start_of_year:
        this_year_files.append((file_path, last_modified_date))
    else:
        older_files.append((file_path, last_modified_date))

# Function to write categorized files to the text file
def write_category(f, category_name, files):
    f.write(f'=== {category_name} ===\n')
    for file_path, last_modified_date in files:
        last_modified_date_str = datetime.fromtimestamp(last_modified_date).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{file_path} {last_modified_date_str}\n')
    f.write('\n')

# Write the categorized information to a text file
with open(output_file, 'w') as f:
    write_category(f, 'Modified in the Past 3 Months', recent_files)
    write_category(f, 'Modified in the past 12 months', this_year_files)
    write_category(f, 'Older than 12 months', older_files)

print(f'File names and modification dates have been written to {output_file}')
