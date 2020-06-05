import os
import pydicom

compressed_dir = "./Aj_19591007_03481716"
uncompressed_dir = compressed_dir+"_uncompressed"

if not os.path.exists(uncompressed_dir):
    os.makedirs(uncompressed_dir)

path, directories, files = list(os.walk(compressed_dir))[0]

for file in files:
    print(file)
    if '.dcm' in file:
        ds = pydicom.dcmread(os.path.join(compressed_dir, file))
        ds.decompress()
        ds.save_as(os.path.join(uncompressed_dir, file))
