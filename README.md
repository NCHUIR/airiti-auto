# ariti-auto
華藝線上圖書館網站下載文件並轉檔成dspace上傳的CSV格式的自動化工具
# Usage
## Set up chromedriver
請依照電腦的作業系統與安裝的Google Chrome版本下載正確的[chrome driver](https://chromedriver.chromium.org/)
並放到```resources/```裡，Windows系統請保持命名```chromedriver.exe```，Linux系統請保持命名```chromedriver```。
## Prepare input
請編輯```input.py```來指定要下載的期刊URL及標題、handleID等資料：
```python
orders = [
    {
        # 資料夾的名稱會是 'title[handleId]'
        'title': '中華水土保持學報第50卷4期',
        'handleId': '10000',
        'url': 'http://www.airitilibrary.com/Publication/alPublicationJournal?PublicationID=02556073&IssueID=202004070001',
        'date': '2019-12-01'    # 出版物出版日期，會自動填入metadata.csv
    }
    # 可以有多個
]

```
多個項目將批次執行。
## Run
```
python main.py
```
### For WINDOWS
```
chcp 65001
```
[reference](https://coder.tw/?p=7487)

## Result
執行結果會放在```output/```資料夾中。

# Detail
請確保```temp/download/```資料夾存在且內容爲空。

# Enhancement
目前是使用pytesseract來處理captcha驗證碼，約5次成功1次，若要加快可以引入其他辨識準確率更高的方案。

# Author
張世澤 <[zhshize@smail.nchu.edu.tw](mailto:zhshize@smail.nchu.edu.tw)> 2020
