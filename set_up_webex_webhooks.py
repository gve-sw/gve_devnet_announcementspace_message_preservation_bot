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
import webexteamssdk.exceptions
from webexteamssdk import WebexTeamsAPI, ApiError
import json
from credentials import webex_access_token, ngrok_address, ngrok_authtoken, webex_announcement_space_id

webex_api = WebexTeamsAPI(webex_access_token)
all_message_webhook = ''

try:
    all_message_webhook = webex_api.webhooks.create(name="massage_webhook",
                                                    targetUrl=ngrok_address,
                                                    resource="messages",
                                                    event="all",
                                                    secret=ngrok_authtoken,
                                                    filter=f'roomId={webex_announcement_space_id}')

    print(f"Created Message Webhook ID: {all_message_webhook.id}")
except ApiError as error:
    # print(error.message)
    print(f'The following error code was received: {error.status_code}')
    print("The webhook was not created")
    if error.status_code == 401:
        print("Please verify your Webex Access Token")
    elif error.status_code == 401:
        print("Please verify the Room ID")
    elif error.status_code == 409:
        print("A webhook with the same filter/targetUrl already exists, please verify Webhook in developers.webex.com")
    else:
        print("Please verify that you have proper credentials in crendentials.py")


# store the webhook id in a json document
if all_message_webhook:
    json_object = {"webhookId": f"{all_message_webhook.id}"}
    with open('webhook_id.json', 'w') as outfile:
        json.dump(json_object, outfile)
else:
    print("Error received")

# webexteamssdk.exceptions.ApiError: [401] Unauthorized - The request requires a valid access token set in the Authorization request header. [Tracking ID: ROUTER_6357EF2C-601C-01BB-013F-AC12DA16013F]
# webexteamssdk.exceptions.ApiError: [400] Bad Request - POST failed: HTTP/1.1 400 Bad Request (url = https://webhook-engine-a.wbx2.com/webhook-engine/api/v1/webhooks, request/response TrackingId = ROUTER_6357EF72-8F0A-01BB-013F-AC12DA16013F, error = 'Invalid value for filter: roomId') [Tracking ID: ROUTER_6357EF72-8F0A-01BB-013F-AC12DA16013F]