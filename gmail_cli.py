# -*- coding: utf-8 -*-
"""
@name           gmail_cli.py
@author         yoshi0518
@description    Gmail送信CLI
@created        2020/11/14
@modified       2020/11/14
"""

import logging
from optparse import OptionParser

import lib.gmail


##### 定数宣言 #####
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
LOG_MESSAGE_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


def main():

    usage = """
  %prog -s "subject" -m "message_file.txt" -f "from@example.com" -t "to@example.com"
    [options] -c "cc@example.com" -b "bcc@example.com" -u "me" -j "credentials.json" -p "token.pickle"
    [args] "attach_file1" "asttach_file2"... """

    parser = OptionParser(usage=usage)

    # 件名
    parser.add_option("-s", "--subject", action="store", type="string", dest="subject", help="subject")

    # 本文
    parser.add_option("-m", "--message_file", action="store", type="string", dest="message_file", help="message file")

    # 送信元
    parser.add_option("-f", "--from", action="store", type="string", dest="sender", help="from")

    # 宛先
    parser.add_option("-t", "--to", action="store", type="string", dest="to", help="to")

    # カーボンコピー
    parser.add_option("-c", "--cc", action="store", type="string", dest="cc", help="cc", default=None)

    # ブラインドカーボンコピー
    parser.add_option("-b", "--bcc", action="store", type="string", dest="bcc", help="bcc", default=None)

    # ユーザーID
    parser.add_option("-u", "--user_id", action="store", type="string", dest="user_id", help="user_id", default="me")

    # 認証情報jsonファイル
    parser.add_option("-j", "--path_json", action="store", type="string", dest="path_json", help="path_json", default="credentials.json")

    # アクセストークンファイル
    parser.add_option("-p", "--path_pickle", action="store", type="string", dest="path_pickle", help="path_pickle", default="token.pickle")

    # 引数を取得
    options, files = parser.parse_args()

    logger.debug("subject: " + str(options.subject) + lib.gmail.location())
    logger.debug("message_file: " + str(options.message_file) + lib.gmail.location())
    logger.debug("from: " + str(options.sender) + lib.gmail.location())
    logger.debug("to: " + str(options.to) + lib.gmail.location())
    logger.debug("cc: " + str(options.cc) + lib.gmail.location())
    logger.debug("bcc: " + str(options.bcc) + lib.gmail.location())
    logger.debug("user_id: " + str(options.user_id) + lib.gmail.location())
    logger.debug("path_json: " + str(options.path_json) + lib.gmail.location())
    logger.debug("path_pickle: " + str(options.path_pickle) + lib.gmail.location())
    logger.debug("files: " + str(files) + lib.gmail.location())

    # メール本文ファイルを開く
    with open(options.message_file, "r", encoding="utf-8") as fp:
        body = fp.read()

    # 添付ファイル
    if not files:
        files = None

    # Gmailオブジェクトを取得
    gmail = lib.gmail.GmailClass(
        user_id=options.user_id,
        path_json=options.path_json,
        path_pickle=options.path_pickle,
    )

    # メッセージを送信
    message_id = gmail.send_message(
        options.subject,
        body,
        options.sender,
        options.to,
        cc=options.cc,
        bcc=options.bcc,
        files=files
    )

    logger.info("message_id: " + message_id + lib.gmail.location())


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

    main()

    # 処理終了
    logger.info(__file__ + " end" + lib.gmail.location())
