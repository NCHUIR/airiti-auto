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


def get_orders():
    return orders
