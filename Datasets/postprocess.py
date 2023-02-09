# Importing Image class from PIL module
from PIL import Image
import os
import argparse

def getImagesPaths(root):
    paths = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name[-3:] not in ["JPG", "jpg", "png", "PNG"] :	
                continue
            paths.append(os.path.join(path, name))

    return paths



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', default='images/')
    parser.add_argument('--output_folder', default='images/')
    parser.add_argument('--captcha_type', default='skbank')
    args = parser.parse_args()
    
    folder = args.output_folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    paths = getImagesPaths(args.input_folder)
    
    captcha_type = args.captcha_type


    iteration = len(paths)
    for i, path in enumerate(paths):
        
        im = Image.open(path)
        
        if captcha_type == 'megabank':
            im1 = im.crop((2400, 757, 2600, 855)) # megabank
        elif captcha_type == 'skbank':
            im1 = im.crop((2269, 602, 2523, 682)) # skbank
        else:
            im1 = im
            
        path = os.path.join(folder, f'{str(i).zfill(4)}.jpg')
        im1 = im1.save(path)

        if i % int(iteration/100) == 0:
            print(f'downloading ... {int(i/iteration*100)}%', end='\r')

    print('downloading ... done')
    

if __name__ == '__main__':
    main()