# gmailapi-python

## Author

yoshi0518

## Description

Gmail Api usage example and Gmail Api CLI

## lib/gmail.py

Gmail API Class and utility function.

- location

  Get the file name and the number of lines where the location function was executed

- decode_base64url_data

  Base64url decoding

- GmailClass.__init__

  Make the initial settings required for Gmail operation

- GmailClass.get_credential

  Get an access token

- GmailClass.get_service

  Get resources to access Gmail

- GmailClass.get_labels

  Get the label

- GmailClass.get_label_ids

  Get label ID

- GmailClass.get_message_ids

  Get the message ID

- GmailClass.get_messages

  Get the message

- GmailClass.send_message

  Send a message

- GmailClass.create_message

  Base64 encode MIME Text without attachments

- GmailClass.create_message_files

  Base64 encode MIME Text with attachments

## gmail_cli.py

Gmail Api Command Line Interface

## How to Use

- get_labels.py
- get_label_ids.py

  Get labels

- get_messages_01.py
- get_messages_02.py
- get_messages_03.py
- get_messages_04.py

  Get Messages

- send_message_01.py
- send_message_02.py
- send_message_03.py

  Send Messages

- gmail_cli.py

```
# Basic usage
$ python gmail_cli.py -s "subject" -m "body.txt" -f "from@example.com" -t "to1@example.com,to2@example.com"

# Use configuration
$ python gmail_cli.py -s "subject" -m "body.txt" -f "from@example.com" -t "to@example.com" -j "./config/credentials.json" -p "./config/token.pickle"

# Use CC and BCC
$ python gmail_cli.py -s "subject" -m "body.txt" -f "from@example.com" -t "to@example.com" -c "cc@example.com" -b "bcc@example.com"

# Use Attach Files
$ python gmail_cli.py -s "subject" -m "body.txt" -f "from@example.com" -t "to@example.com" "./attach/sample.txt" "./attach/sample.csv"
```

## Link

[Gmail API](https://developers.google.com/gmail/api)

[Gmail Search Query](https://support.google.com/mail/answer/7190)
