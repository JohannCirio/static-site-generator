import os
import shutil

def copy_static(src, destination):
    if not os.path.exists(src) or not os.path.exists(destination):
        return False
    
    shutil.rmtree(destination)
    os.mkdir(destination)
    paths = os.listdir(src)

    for path in paths:
        full_path = os.path.join(src, path)
        destination_full_path = os.path.join(destination, path)
        
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination_full_path)
        else:
            os.mkdir(destination_full_path)
            copy_static(full_path, destination_full_path)

