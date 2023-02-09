# Captcha OCR

## get result with our fine tuned model
* download fine tuned weight
    ``` bash
    bash ./download.sh
    ```
* read image with weight
    ``` bash
    python read.py outputs/parseq/combined/checkpoints/epoch=196-step=104472-val_accuracy=100.0000-val_NED=100.0000.ckpt \
        --images path/to/image/folder/*
    ```

## Finetune from pretrained weight
* prepare datasets
    1. use tools/create_lmdb_dataset.py transform csv file to lmdb datasets
    ``` bash
    python create_lmdb_dataset.py \
        --inputPath path\to\dataset\folder \
        --gtFile path\to\csvfile.csv \
        --outputPath data\test\dataset_name
    ```
    2. prepare train\val datasets
    ``` bash
    cp data\test\dataset_name_train\* data\train\real
    cp data\test\dataset_name_test\* data\val
    ```

* start training
    ``` bash
    ./train.py pretrained=parseq
    ```
    
## Testing
* prepare datasets
    1. use tools/create_lmdb_dataset.py transform csv file to lmdb datasets
    ``` bash
    python create_lmdb_dataset.py \
        --inputPath path\to\dataset\folder \
        --gtFile path\to\csvfile.csv \
        --outputPath data\test\dataset_name
    ```
    2. prepare test datasets
    ``` bash
    cp data\test\dataset_name_test\* data\test\dataset_name\
    ```
    3. edit strhub/data/module.py
    ``` python
    TEST_BENCHMARK_SUB = ('dataset_name_1', 'dataset_name_2', 'dataset_name_3')
    TEST_BENCHMARK = ('dataset_name_1', 'dataset_name_2', 'dataset_name_3')
    ```
    4. edit test.py
    ``` python
    charset_test = string.digits + string.ascii_uppercase
    ```
    5. edit config/main.yaml
    ``` yaml
    charset_test: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ```
* start testing
    ``` bash
    python test.py
    ```

    
## get pretrained result with parseq pretrained weight
``` bash
python get_pretrained_result.py \
    --input_folder path/to/image/folder  \
    --output_csv path/to/result.csv

```

## Run Fast API Server
``` bash
python run_fastapi.py
```