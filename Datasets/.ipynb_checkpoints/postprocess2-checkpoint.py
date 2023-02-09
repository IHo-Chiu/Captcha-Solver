
from PIL import Image
import os
import csv

image_dir = "skbank_postprocessed"
def getImagesPaths(root):
    paths = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name[-3:] not in ["JPG", "jpg", "png", "PNG"] :	
                continue
            paths.append(os.path.join(path, name))

    return paths

paths = getImagesPaths(image_dir)
paths.sort()

labels = []
with open('skbank.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        labels.append(row[1])

d = {}
for i, (path, label) in enumerate(zip(paths, labels)):
    d[label] = path

iter = len(d)
with open('skbank2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    for i, k in enumerate(d):
        im = Image.open(d[k])
        im1 = im
        im1 = im1.save(f'skbank_postprocessed2/{str(i).zfill(4)}.png')

        writer.writerow([f'skbank_postprocessed2/{str(i).zfill(4)}.png', k])

        if i % int(iter/100) == 0:
            print(f'downloading ... {int(i/iter*100)}%', end='\r')
                
    print('downloading ... done')