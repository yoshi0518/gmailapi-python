# -*- coding: utf-8 -*-
"""
@name           get_labels.py
@author         yoshi0518
@description    ラベルを取得する
@created        2020/11/12
@modified       2020/11/12
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
    gmail = lib.gmail.GmailClass()

    # ラベルを取得
    labels = gmail.get_labels()
    for label in labels:
        logger.info(str(label) + lib.gmail.location())

    # 処理終了
    logger.info(__file__ + " end" + lib.gmail.location())
