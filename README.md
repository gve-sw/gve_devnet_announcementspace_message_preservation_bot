# gve_devnet_announcementspace_message_preservation_bot
Webex BOT that preserves messages written by moderators of an only announcement space. 
The messages are preserved in a DB until deleted by the moderators. 
The messages will be preserved if deleted by non-moderators. 


## Contacts
* Max Acquatella

## WARNING
This is SAMPLE CODE, it does not follow code security best practices (token and password security enforcement), 
its purpose is to demonstrate the use of Cisco APIs, not recommended to use in production environments. 

## Solution Components and Requirements
* Webex Organization, familiarity with Webex for Developers, Webex SDK, Webhooks and obtaining 
information using Webex REST APIs.
https://developer.webex.com/

* Familiarity with NGROK tunnels: 
https://ngrok.com/

## Installation/Configuration
NOTE: This code was tested using macOS Python3 virtual environments. For Windows Python3 Virtual Environments please
see: https://www.youtube.com/watch?v=APOPm01BVrk

#### Download code (git clone), install virtual environment, install requirements:

Download Code:
```BASH
git clone https://wwwin-github.cisco.com/gve/gve_devnet_announcementspace_message_preservation_bot.git 
```
Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```
Install Requirements.txt
```BASH
pip3 install -r requirements.txt
```

#### NGROK, get API key and Secret, get URL and register Webex Webhook
NGROK:
PLease follow the instruction to download and install NGROK from the following website: 

https://ngrok.com/

NOTE: By the time of this writing, Webex and NGROK had communications issues, so we tested the NGROK tunnel 
using the --region UE

```Bash
ngrok http 8080 --region=eu
```
The code uses the local port 8080, this can be changed if required. 

Save the public URL in credentials.py

#### Get Webex Space ID and Webex BOT token
Use the following Webex API to extract the room ID (create a new Room if it does not exist):
```text
https://developer.webex.com/docs/api/v1/rooms/list-rooms
```
Assign moderators to the Room/Space

Obtain Webex Admin temporary token using this link:
```text
https://developer.webex.com/docs/getting-started
```

Save token in credentials.py
NOTE: The previous token will last only for 12 hours. For a permanent token please create an integration. See:
```text
https://developer.webex.com/docs/integrations
```


#### Assign admins (moderators)
In credentials.py, fill out the list named 'admin_emails' with the moderators of the room. 
These administrators will be able to write messages in the room and delete said messages both from the room 
and from the database.
Messages deleted by any other user NOT in this list should be preserved and reposted by the code. 
In order to promote a user from the announcement space, just right-click the user and promote to moderator. 
This user will be able to post/delete messages in the space, though if this user is not in the list of admins, 
the messages deleted by the "non-admin" user will be reposted.

#### Register Webhook
There is an auxiliary script to register the required webhook, please run this script first. The Webhook ID will be
saved in "webhook_id.json". The main script will pull the Webhook ID from this json document. 

```bash
python3 set_up_webex_webhooks.py
```

Make sure that all the required credentials are in place: 

![/IMAGES/1image.png](/IMAGES/1image.png)

#### run python3 app.py 
Via command line, start the FLASK application: 

```bash
 python3 app.py 
```


## Usage

The code will add a database folder, which will contain the messages created by the room admins/moderators.

The code will output multiple messages:

![/IMAGES/2image.png](/IMAGES/2image.png)

Once the Space moderators post messages, the code will create a database called "messages_db.db" and store
messages posted by moderators. Moderators that are not admininistrator will be able to post messages, but if
said moderators delete messages, these deleted messages will be reposted by the code (on behalf of the user that
created the Webex API Token).

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.