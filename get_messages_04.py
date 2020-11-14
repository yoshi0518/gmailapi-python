# -*- coding: utf-8 -*-
"""
@name           get_messages.py
@author         yoshi0518
@description    メッセージを取得する(ラベル、件数指定)
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

    # ラベルIDを取得
    label_ids = gmail.get_label_ids(["Chatwork_eigyo", "Chatwork_soudan"])
    logger.info("label_ids: " + str(label_ids) + lib.gmail.location())

    for label_id in label_ids:
        logger.info("label_id: " + str(label_id) + lib.gmail.location())

        # メッセージIDを取得
        message_ids = gmail.get_message_ids(label_id=label_id, count=2)
        logger.info("message_ids: " + str(message_ids) + lib.gmail.location())

        if message_ids is None:
            logger.warning("no result data!")
            continue

        tmp_message_ids = [message_id["id"] for message_id in message_ids]
        logger.info("tmp_message_ids: " + str(tmp_message_ids) + lib.gmail.location())

        # メッセージを取得
        messages = gmail.get_messages(tmp_message_ids)
        for message in messages:
            logger.info("message:" + lib.gmail.location())
            for item in message.items():
                logger.info("  " + str(item) + lib.gmail.location())

    # 処理終了
    logger.info(__file__ + " end" + lib.gmail.location())
