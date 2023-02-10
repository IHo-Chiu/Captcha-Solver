import torch
from PIL import Image
from strhub.data.module import SceneTextDataModule


import os
import argparse
import csv

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
    parser.add_argument('--output_csv', default='test.csv')
    args = parser.parse_args()
    
    folder = args.output_folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    paths = getImagesPaths(args.input_folder)
    # print(len(paths))


    # Load model and image transforms
    parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()
    img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)


    labels = []
    for i, path in enumerate(paths):
        img = Image.open(path).convert('RGB')
        # Preprocess. Model expects a batch of images with shape: (B, C, H, W)
        img = img_transform(img).unsqueeze(0)

        logits = parseq(img)
        logits.shape  # torch.Size([1, 26, 95]), 94 characters + [EOS] symbol

        # Greedy decoding
        pred = logits.softmax(-1)
        label, confidence = parseq.tokenizer.decode(pred)

        labels.append(label[0])

        print(label[0])

        if len(paths) > 100 and i % int(len(paths)/100) == 0:
            print(f'running ... {int(i/len(paths)*100)}%', end='\r')

    print('running ... done')


    with open(args.output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        batch = zip(paths, labels)
        for i, (path, label) in enumerate(batch):
            writer.writerow([path, label])

            if len(paths) > 100 and i % int(len(paths)/100) == 0:
                print(f'save result ... {int(i/len(paths)*100)}%', end='\r')

        print('save result ... done')
    

if __name__ == '__main__':
    main()