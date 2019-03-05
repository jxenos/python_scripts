import os
import json
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


origin_folder = 'asdf'
dest_folder = 'wildlife'

try:
    os.mkdir(dest_folder)
except Exception:
    pass

copytree(origin_folder, dest_folder)

json_file_path = './'

file_json = json.load(open(origin_folder + '.json', 'rb'))

new_json = dict(file_json)
new_json['frames'] = {}
new_json['visitedFrames'] = []

bad_files = []

n = 0

for img_file in os.scandir(dest_folder):
    if img_file.name in file_json['frames']:
        # check for data
        if file_json['frames'][img_file.name] != []:
            # if some add to new dictionary
            garbage, ext = os.path.splitext(img_file.name)
            new_name = '{:06}'.format(n) + ext
            new_json['frames'][new_name] = file_json['frames'][img_file.name]
            new_json['visitedFrames'].append(new_name)

            # change filename
            os.rename(img_file.path, os.path.join(dest_folder, new_name))

            n += 1
        else:
            # if none add to bad lists
            bad_files.append(img_file.name)
    else:
        # if none add to bad lists
        bad_files.append(img_file.name)

# save new file
with open(dest_folder + '.json', 'w+') as outfile:
    json.dump(new_json, outfile)

for bad_file in bad_files:
    os.remove(os.path.join(dest_folder, bad_file))

# list files we couldn't find data for
print('================================')
print('BAD FILES:')
print(bad_files)
