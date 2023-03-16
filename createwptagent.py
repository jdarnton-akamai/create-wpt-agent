import logging
import numpy as np
import json
import requests
import sys
import random

# Set up logging
logging.basicConfig(filename='./wpt_activity.log', level=logging.DEBUG)

# Get Linode settings
linode_settings = {} # Create an empty dictionary

try:
    with open('./linode_settings.txt', 'r') as file:
        # Loop through each line in the file
        for line in file:
            # Split the line into key and value using the ':' delimiter
            key, value = line.strip().split(':')
            # Store the key:value pair in the dictionary
            linode_settings[key] = value.strip()
except:
    sys.exit('Could not find linode_settings.txt')

if ('api_token' in linode_settings) & ('username' in linode_settings) & ('password' in linode_settings) & ('root_pass' in linode_settings) & ('wpt_server' in linode_settings):
    api_token = linode_settings.get('api_token')
    sudo_user = linode_settings.get('username')
    sudo_password = linode_settings.get('password')
    root_password = linode_settings.get('root_pass')
    wpt_server = linode_settings.get('wpt_server')
else:
    sys.exit('Invalid linode_settings.txt - missing values')

# Get Agent Settings
try:
    with open('./agent_list.txt', 'r') as f:
        lines = f.read().splitlines()
        params = [line.split(',') for line in lines]
        matrix = np.array(params)
except:
    sys.exit('Could not find agent_list.txt')

# Setup POST request
url = "https://api.linode.com/v4/linode/instances"
headers = { 
    'Content-Type': 'application/json', 
    'Authorization': 'Bearer ' + api_token 
    }

empty_array = []
tags = ["webpagetest"]

# Loop through matrix of parameters
for row in matrix:

    # Extract parameters from row
    linode_region = row[0]
    wpt_location = row[1]
    wpt_key = row[2]

    # Construct JSON POST body
    stackscript_data = {
        'disable_root': 'Yes',
        'username': sudo_user,
        'password': sudo_password,
        'wpt_server': wpt_server,
        'wpt_location': wpt_location,
        'wpt_key': wpt_key
    }

    data = {
        'image': 'linode/ubuntu22.04',
        'region': linode_region,
        'type': 'g6-standard-2',
        'label': 'wpt-agent-' + str(random.randrange(0,1000,3)) + '-' + linode_region,
        'tags': tags,
        'root_pass': root_password,
        'authorized_users': empty_array,
        'booted': bool(True),
        'backups_enabled': bool(False),
        'private_ip': bool(False),
        'stackscript_id': 1137140,
        'stackscript_data': stackscript_data
    }

    # Convert dictionary to JSON string
    json_data = json.dumps(data)

    response = requests.post(url, headers=headers, data=json_data)

    # Check response status code
    if response.status_code == 200:
        print("For " + wpt_location + " POST request successful!")
        logging.info("Response for " + wpt_location, response.content)
    else:
        print("For " + wpt_location + " POST request failed.")
        print("Status Code for " + wpt_location, response.status_code)
        logging.info("Response for " + wpt_location, response.content)
    
# Log activity
logging.info("Complete!")