import os
import time

import csv

from agent import get_browser
from config import output_path, columns, download_temp_path
from input import get_orders
from metadata import get_metadata
from ariti import get_all_doc_ids, get_ris_text, download_file, get_page_count
from risReader import RisReader


def convert_img(img, threshold):
    img = img.convert("L") # 處理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img


def check_dirs():
    if not os.path.exists(download_temp_path):
        os.mkdir(download_temp_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)


def main():
    browser = get_browser()
    orders = get_orders()

    for order in orders:
        metadatas = []
        dest_path = output_path + os.path.sep + order['title'] + '[' + order['handleId'] + ']'
        os.mkdir(dest_path)

        browser.get(order['url'])
        time.sleep(2)

        page_count = get_page_count(browser)

        for page in range(0, page_count):
            if page != 0:
                browser.get(order['url'] + '&page=' + str(page))
                time.sleep(2)

            ids = get_all_doc_ids(browser)
            for i in range(0, len(ids)):
                ris_text = get_ris_text(ids[i])
                ris = RisReader(ris_text)

                metadata = get_metadata(ris)
                metadata['contents'] = str(i) + '.pdf'
                metadata['dc.date[zh_TW]'] = order['date']
                metadatas.append(metadata)

                pdf = download_file(browser, ids[i])
                os.rename(pdf, dest_path + os.path.sep + metadata['contents'])
                # time.sleep()

        # save metadata to csv
        csv_file = dest_path + os.path.sep + 'metadata.csv'
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                for data in metadatas:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    browser.close()


check_dirs()
main()
