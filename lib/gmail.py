# -*- coding: utf-8 -*-
"""
@name           gmail.py
@author         yoshi0518
@description    Gmail操作に関する処理のモジュール
@created        2020/11/12
@modified       2020/11/12
"""

import base64
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import inspect
import logging
import mimetypes
import os
from pathlib import Path
import pickle

from apiclient import errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


##### 定数宣言 #####
SCOPES = [ # Gmail APIのスコープ
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.modify",
]


def location():
    """
    【処理内容】
    location関数を実行したファイル名、行数を取得する
    【引数】
    なし
    【戻り値】
    ファイル名、行数
    """

    frame = inspect.currentframe().f_back
    fname = os.path.basename(frame.f_code.co_filename)
    line = frame.f_lineno
    return f" ({fname}:{line})"


def decode_base64url_data(data):
    """
    【処理内容】
    base64urlのデコード
    【引数】
    data：エンコードする文字列
    【戻り値】
    エンコードした文字列
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message


class GmailClass:
    """
    【クラス内容】
    Gmailの送受信に利用する
    """

    ##### 変数宣言 #####
    _creds = None
    _logger = None
    _service = None
    _user_id = None


    def __init__(self, user_id="me", path_json="credentials.json", path_pickle="token.pickle"):
        """
        【処理内容】
        Gmail操作に必要な初期設定を行う
        【引数】
        path_json：認証情報jsonファイル
        path_pickle：アクセストークンファイル
        【戻り値】
        なし
        """

        self._logger = logging.getLogger(__name__)

        self._logger.debug("__init__ start" + location())

        self._user_id = user_id

        # アクセストークンを取得
        self.get_credential(path_json=path_json, path_pickle=path_pickle)
        self._logger.debug("creds: " + str(self._creds) + location())

        # Gmailにアクセスするリソースを取得
        self.get_service()
        self._logger.debug("service: " + str(self._service) + location())

        self._logger.debug("__init__ end" + location())


    def get_credential(self, path_json="credentials.json", path_pickle="token.pickle"):
        """
        【処理内容】
        アクセストークンの取得する
        認証情報jsonファイルからpickle形式でトークンを保存し、2回目以降は再利用する
        【引数】
        path_json：認証情報jsonファイル
        path_pickle：アクセストークンファイル
        【戻り値】
        なし
        """

        self._logger.debug("get_credential start" + location())

        if os.path.exists(path_pickle):
            with open(path_pickle, "rb") as token:
                self._creds = pickle.load(token)

        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(path_json, SCOPES)
                self._creds = flow.run_local_server()
                # self._creds = flow.run_console()
            with open(path_pickle, "wb") as token:
                pickle.dump(self._creds, token)

        self._logger.debug("get_credential end" + location())


    def get_service(self):
        """
        【処理内容】
        Gmailにアクセスするリソースを取得する
        【引数】
        なし
        【戻り値】
        なし
        """

        try:
            self._logger.debug("get_service start" + location())

            self._service = build("gmail", "v1", credentials=self._creds, cache_discovery=False)

            self._logger.debug("get_service end" + location())

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def get_labels(self):
        """
        【処理内容】
        ラベルを取得する
        【引数】
        なし
        【戻り値】
        labels：ラベルのリスト
        """

        try:
            self._logger.debug("get_labels start" + location())

            labels = self._service.users().labels().list(userId=self._user_id).execute()["labels"]

            self._logger.debug("get_labels end" + location())

            return labels

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def get_label_ids(self, label_names):
        """
        【処理内容】
        ラベルIDを取得する
        【引数】
        label_names：ラベル名のリスト
        【戻り値】
        label_ids：ラベルIDのリスト
        """

        try:
            self._logger.debug("get_label_ids start" + location())

            labels = self._service.users().labels().list(userId=self._user_id).execute()["labels"]

            label_ids = []
            for label_name in label_names:
                label_id = [label["id"] for label in labels if label["name"] == label_name][0]
                label_ids.append(label_id)

            self._logger.debug("get_label_ids end" + location())

            return label_ids

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def get_message_ids(self, query=None, label_id=None, count=3):
        """
        【処理内容】
        メッセージIDを取得する
        【引数】
        query：検索クエリ
            https://support.google.com/mail/answer/7190
        label_id：ラベルID
        count：取得数
        【戻り値】
        message_ids：メッセージIDのリスト
        """

        try:
            self._logger.debug("get_message_ids start" + location())

            if not query is None and not label_id is None:
                res = self._service.users().messages().list(
                    userId=self._user_id,
                    q=query,
                    labelIds=label_id,
                    maxResults=count
                ).execute()
            elif not query is None:
                res = self._service.users().messages().list(
                    userId=self._user_id,
                    q=query,
                    maxResults=count
                ).execute()
            elif not label_id is None:
                res = self._service.users().messages().list(
                    userId=self._user_id,
                    labelIds=label_id,
                    maxResults=count
                ).execute()
            else:
                res = self._service.users().messages().list(
                    userId=self._user_id,
                    maxResults=count
                ).execute()

            if res["resultSizeEstimate"] == 0:
                return None

            self._logger.debug("get_message_ids end" + location())

            return res["messages"]

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def get_messages(self, message_ids):
        """
        【処理内容】
        メッセージを取得する
        【引数】
        message_ids：メッセージIDのリスト
        【戻り値】
        messages：メッセージのリスト
        """

        try:
            self._logger.debug("get_messages start" + location())

            messages = []
            for message_id in message_ids:
                self._logger.debug("message_id: " + message_id + location())

                message = {}

                # メッセージを取得
                message_detail = (
                    self._service.users().messages().get(userId=self._user_id, id=message_id).execute()
                )

                self._logger.debug("message_detail: " + str(message_detail) + location())

                message["id"] = message_detail["id"]
                message["label_ids"] = message_detail["labelIds"]
                message["size"] = message_detail["payload"]["body"]["size"]

                for header in message_detail["payload"]["headers"]:
                    message[header["name"].lower()] = header["value"]

                # テキストメールの場合
                if 'data' in message_detail['payload']['body']:
                    message["body"] = decode_base64url_data(message_detail["payload"]["body"]["data"])

                # HTMLメールの場合
                else:
                    parts = message_detail['payload']['parts']

                    for part in parts:

                        if 'parts' in part:
                            for part_child in part["parts"]:
                                if part_child["mimeType"] == "text/plain":
                                    body = part_child["body"]["data"]
                                    break

                            break
                        else:
                            if part["mimeType"] == "text/plain":
                                body = part["body"]["data"]
                                break

                    message["body"] = decode_base64url_data(body)

                messages.append(message)

            self._logger.debug("get_messages end" + location())

            return messages

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def send_message(self, subject, body, sender, to, cc=None, bcc=None, files=None):
        """
        【処理内容】
        メッセージを送信する
        【引数】
        subject：件名
        body：本文
        sender：送信元
        to：宛先
        cc：カーボンコピー
        bcc：ブラインドカーボンコピー
        files：添付ファイル
        【戻り値】
        message_id：メッセージID
        """

        try:
            self._logger.debug("send_message start" + location())

            self._logger.debug("subject: " + subject + location())
            self._logger.debug("body: " + body + location())
            self._logger.debug("sender: " + sender + location())
            self._logger.debug("to: " + to + location())
            self._logger.debug("cc: " + str(cc) + location())
            self._logger.debug("bcc: " + str(bcc) + location())
            self._logger.debug("files: " + str(files) + location())

            if files:
                message = self.create_message_files(subject, body, files, sender, to, cc, bcc)
            else:
                message = self.create_message(subject, body, sender, to, cc, bcc)

            sent_message = (
                self._service.users().messages().send(userId=self._user_id, body=message).execute()
            )

            self._logger.debug("send_message end" + location())

            return sent_message["id"]

        except errors.HttpError as error:
            self._logger.error(f"An error occurred: {error}")


    def create_message(self, subject, body, sender, to, cc=None, bcc=None):
        """
        【処理内容】
        添付ファイルなしMIMETextをbase64エンコードする
        【引数】
        subject：件名
        body：本文
        sender：送信元
        to：宛先
        cc：カーボンコピー
        bcc：ブラインドカーボンコピー
        【戻り値】
        エンコードしたMIMEText
        """

        self._logger.debug("create_message start" + location())

        enc = "utf-8"
        message = MIMEText(body.encode(enc), _charset=enc)
        message["subject"] = subject
        message["from"] = sender
        message["to"] = to

        if cc:
            message["cc"] = cc

        if bcc:
            message["bcc"] = bcc

        encode_message = base64.urlsafe_b64encode(message.as_bytes())

        self._logger.debug("encode_message: " + str(encode_message) + location())

        self._logger.debug("create_message end")

        return {"raw": encode_message.decode()}


    def create_message_files(self, subject, body, files, sender, to, cc=None, bcc=None):
        """
        【処理内容】
        添付ファイルありMIMETextをbase64エンコードする
        【引数】
        subject：件名
        body：本文
        sender：送信元
        files：添付ファイルのリスト
        sender：送信元
        to：宛先
        cc：カーボンコピー
        bcc：ブラインドカーボンコピー
        【戻り値】
        エンコードしたMIMEText
        """

        self._logger.debug("create_message_files start" + location())

        message = MIMEMultipart()
        message["subject"] = subject
        message["from"] = sender
        message["to"] = to

        if cc:
            message["cc"] = cc

        if bcc:
            message["bcc"] = bcc

        enc = "utf-8"
        msg = MIMEText(body.encode(enc), _charset=enc)
        message.attach(msg)

        for index, file in enumerate(files):

            content_type, encoding = mimetypes.guess_type(file)

            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            main_type, sub_type = content_type.split("/", 1)

            self._logger.debug("file" + str(index + 1) + ": " + file + location())
            self._logger.debug("content_type: " + str(content_type) + location())
            self._logger.debug("encoding: " + str(encoding) + location())
            self._logger.debug("main_type: " + str(main_type) + location())
            self._logger.debug("sub_type: " + str(sub_type) + location())

            if main_type == "text" or main_type == "application":
                with open(file, "rb") as fp:
                    msg = MIMEApplication(fp.read(), _subtype=sub_type)
            elif main_type == "image":
                with open(file, "rb") as fp:
                    msg = MIMEImage(fp.read(), _subtype=sub_type)
            elif main_type == "audio":
                with open(file, "rb") as fp:
                    msg = MIMEAudio(fp.read(), _subtype=sub_type)
            else:
                with open(file, "rb") as fp:
                    msg = MIMEBase(main_type, sub_type)
                    msg.set_payload(fp.read())

            p = Path(file)
            msg.add_header("Content-Disposition", "attachment", filename=p.name)
            message.attach(msg)

        encode_message = base64.urlsafe_b64encode(message.as_bytes())

        # self._logger.debug("encode_message: " + str(encode_message) + location())

        self._logger.debug("create_message_files end" + location())

        return {"raw": encode_message.decode()}
