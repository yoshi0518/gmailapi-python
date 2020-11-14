# -*- coding: utf-8 -*-
"""
@name           send_message_03.py
@author         yoshi0518
@description    メッセージを送信する(添付ファイル)
@created        2020/11/13
@modified       2020/11/13
"""

import logging

import lib.gmail


##### 定数宣言 #####
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
LOG_MESSAGE_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


if __name__ == "__main__":

    # ロギング準備
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_MESSAGE_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    logger = logging.getLogger(__name__)

    # 処理開始
    logger.info(__file__ + " start" + lib.gmail.location())

    # Gmailオブジェクトを取得
    gmail = lib.gmail.GmailClass(path_json="./config/credentials.json")

    # メール本文ファイルを開く
    with open("body.txt", "r", encoding="utf-8") as fp:
        body = fp.read()

    # 添付ファイルリスト
    files = [
        "./attach/sample.csv",
        "./attach/sample.docx",
        "./attach/sample.jpg",
        "./attach/sample.pdf",
        "./attach/sample.png",
        "./attach/sample.pptx",
        "./attach/sample.txt",
        "./attach/sample.xlsx",
    ]

    # メッセージを送信
    message_id = gmail.send_message(__file__, body, "from@example.com", "to@example.com", files=files)
    logger.info("message_id: " + message_id + lib.gmail.location())

    # 処理終了
    logger.info(__file__ + " end" + lib.gmail.location())
