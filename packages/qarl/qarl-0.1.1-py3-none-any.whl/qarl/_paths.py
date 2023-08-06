import os

# Define common directories
qarl_dir = os.path.expanduser('~/.qarl')
boxes_dir = os.path.join(qarl_dir, 'boxes')

# Create any vital directories
os.makedirs(boxes_dir, exist_ok=True)