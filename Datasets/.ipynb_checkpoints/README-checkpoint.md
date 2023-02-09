# Captcha Dataset

## Download Datasets

``` bash
bash ./download.sh
```

|       | [**台企銀(tbbank)**](https://portal.tbb.com.tw/) | [**兆豐銀(megabank)**](https://www.megabank.com.tw/) | [**新光銀(skbank)**](https://www.skbank.com.tw/) |
| ----- | ------ | -------- | ------ |
| Train |  9000  |  4000    |  4000  |
| Test  |  1000  |  1000    |  1000  |

## Dataset Collect Flow

### 1. data collection
* tbbank: 蒐集 10000 張圖片並放到 tbbank_raw 資料夾
    ``` bash
    python tbbank_crawler.py \
        --folder tbbank_raw \
        --num 10000 
    ```
* megabank
    1. 將 **megabank.py** 下載到自己的電腦（需要螢幕截圖功能所以不能在server上做）
    2. 下載需要的 **chromedriver** 並放在程式碼同一個資料夾
    3. 蒐集 5000 張圖片並放到 megabank_raw 資料夾
        ``` bash
        python megabank.py \
            --folder megabank_raw \
            --num 5000 
        ```
    4. 對所有圖片進行裁切
        ``` bash
        python postprocess.py \
            --input_folder megabank_raw \
            --output_folder megabank_postprocessed \
            --captcha_type megabank 
        ```
* skbank
    1. 將 **skbank.py** 下載到自己的電腦（需要螢幕截圖功能所以不能在server上做）
    2. 下載需要的 **chromedriver** 並放在程式碼同一個資料夾
    3. 蒐集 5000 張圖片並放到 skbank_raw 資料夾
        ``` bash
        python skbank.py \
            --folder skbank_raw \
            --num 5000 
        ```
    4. 對所有圖片進行裁切
        ``` bash
        python postprocess.py \
            --input_folder skbank_raw \
            --output_folder skbank_postprocessed \
            --captcha_type skbank 
        ```
### 2. data labeling
* 使用 parseq pretrained model 進行預先標注
    ``` bash
    python trytrysee.py \
        --input_folder ../dataset/tbbank_raw \
        --output_csv ../dataset/tbbank.csv
    python trytrysee.py \
        --input_folder ../dataset/megabank_postprocessed \
        --output_csv ../dataset/megabank.csv
    python trytrysee.py \
        --input_folder ../dataset/skbank_postprocessed \
        --output_csv ../dataset/skbank.csv
    ```

* 刪除重複資料（須改程式碼內資料夾路徑）
    ``` bash
    python postprocessed2.py
    ```