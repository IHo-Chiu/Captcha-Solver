
import os
import requests
import argparse

url = "https://portal.tbb.com.tw/tbbportal/CaptchaImg.jsp?Mon%20Jan%2009%202023%2014:03:06%20GMT+0800%20(%A5x%A5_%BC%D0%B7%C7%AE%C9%B6%A1)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default='images/')
    parser.add_argument('--num', default=100)
    args = parser.parse_args()
    
    folder = args.folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    iteration = int(args.num)
    for i in range(iteration):
        
        img_data = requests.get(url).content 
        path = os.path.join(folder, f'{str(i).zfill(4)}.jpg')
        with open(path, 'wb') as handler: 
            handler.write(img_data)

        if i % int(iteration/100) == 0:
            print(f'downloading ... {int(i/iteration*100)}%', end='\r')

    print('downloading ... done')
    
    

if __name__ == '__main__':
    main()