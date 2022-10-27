"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
from flask_sqlalchemy import SQLAlchemy  # Reviewed - CORRECT
from pprint import pprint
from credentials import webex_announcement_space_id, webex_access_token, admin_emails

# Variables
announcement_space_id = webex_announcement_space_id
access_token = webex_access_token

# Initializes Flask, Webex APIs
app = Flask(__name__)
webex_api = WebexTeamsAPI(access_token)


# DB Related
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Reviewed - CORRECT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages_db.db'  # Reviewed - CORRECT
db = SQLAlchemy(app)  # Reviewed - CORRECT


class MessageDB(db.Model):
    message_id = db.Column("Message_ID", db.String(100), primary_key=True)
    person_email = db.Column("Person_Email", db.String(100))
    message_text = db.Column("Message_Text", db.String(100))

    def __init__(self, message_id, person_email, message_text):
        self.message_id = message_id
        self.person_email = person_email
        self.message_text = message_text

# Creates database
db.create_all()


@app.route('/', methods=["GET", "POST"])
def post_announcement():
    # global repost_message_id
    if request.method == "POST":
        print('POST Received')
        # pprint(request.json)
        event = request.json['event']
        owned_by = request.json['ownedBy']
        data_person_email = request.json['data']['personEmail']

        # 1 - IF for created message - adds message info to DB
        if event == 'created':
            print(f'Message has been created by {owned_by}')
            pprint(request.json)
            _message_id_entry = request.json['data']['id']
            _person_email_entry = request.json['data']['personEmail']
            _message_text_entry = webex_api.messages.get(messageId=_message_id_entry)  # ADD .text at the end
            print(_message_id_entry)
            print(_person_email_entry)
            print(_message_text_entry.text)
            # ADD TO DATABASE
            new_message_db_entry = MessageDB(message_id=_message_id_entry,
                                             person_email=_person_email_entry,
                                             message_text=_message_text_entry.text)
            # print(new_message_db_entry.message_text)
            db.session.add(new_message_db_entry)
            try:
                print("Enters the TRY Block - Creating Entry in DB")
                db.session.commit()
            except:
                print("Enters the EXCEPT Block - Creating Entry in DB FAILED")
                db.session.rollback()
            return 'Success Message Created'

        # 2 - IF for deleted message by admin - deletes message id from DB
        elif event == 'deleted' and data_person_email in admin_emails:
            pprint(request.json)
            # print(data_person_email)
            # print(request.json['data']['id'])
            _message_id_to_delete = request.json['data']['id']
            print(_message_id_to_delete)
            delete_entry = MessageDB.query.get(_message_id_to_delete)
            print(delete_entry)
            if delete_entry:
                print('Entry Exists in DB')
                print('Deleting from DB:')
                db.session.delete(delete_entry)
                print(f'Message has been deleted by {data_person_email}')
                try:
                    print("Enters the TRY Block - Deleting Entry from DB")
                    db.session.commit()
                except:
                    print("Enters the EXCEPT Block - Deleting Entry from DB FAILED")
                    db.session.rollback()
                return 'Success'

            else:
                print('Entry does NOT Exist in DB')
                return 'Success Message Deleted'

        # 3 - IF message gets deleted by a non admin (WEBEX), repost message
        elif event == 'deleted' and data_person_email not in admin_emails:
            print('THIS MESSAGE IS BEING DELETED BY A NON-ADMIN - WEBEX ')
            pprint(request.json)
            _message_id_to_repost = request.json['data']['id']
            repost_entry_id = MessageDB.query.get(_message_id_to_repost)

            # Get from local DB messageID, user_email and message
            try:
                repost_message_id = repost_entry_id.message_id
                repost_person_email = repost_entry_id.person_email
                repost_message_text = repost_entry_id.message_text
                print(repost_message_id)
                print(repost_person_email)
                print(repost_message_text)
            except AttributeError:
                print('Message does not exist - continuing')

            if repost_entry_id:
                print('Message to repost EXISTS in DB')
                print('Reposting User Email and Message to SPACE')

                # repost_person_email = repost_entry_id.person_email
                repost_person_email = admin_emails[1]  # DELETE THIS LINE, JUST FOR TESTING
                repost_message_text = repost_entry_id.message_text
                webex_api.messages.create(roomId=announcement_space_id, text=f'{repost_message_text}')

                # Deletes Existing Message ID from Database to avoid repeated information
                delete_entry = MessageDB.query.get(repost_message_id)
                db.session.delete(delete_entry)

                try:
                    print("Enters the TRY Block - Deleting Entry from DB")
                    db.session.commit()
                except:
                    print("Enters the EXCEPT Block - Deleting Entry from DB FAILED")
                    db.session.rollback()

                return 'Success reposting deleted message by non-admin'

            else:
                print('Message DOES NOT exists in DB')

            return 'Success Message Deleted By Webex'

        else:
            print(f'Unknown')
            return 'Unknown'

    else:
        print('Received GET')
        return '<h1>GET Received<h1>'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
