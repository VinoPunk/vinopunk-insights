import os
def print_tree(start_path='.', indent=''):
    for item in sorted(os.listdir(start_path)):
        path = os.path.join(start_path, item)
        print(indent + '├── ' + item)
        if os.path.isdir(path):
            print_tree(path, indent + '│   ')

print_tree('.')  # or replace '.' with your repo path
