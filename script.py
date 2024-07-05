# script.py
import xbmc
import xbmcaddon
import xbmcgui
import json
import requests

# Get the addon settings
addon = xbmcaddon.Addon()
mobile_number = addon.getSetting('mobile_number')
otp = addon.getSetting('otp')

# Define the Jio TV API endpoint
api_endpoint = 'https://api.jiotv.com/api/v1'

# Define the function to login to the Jio TV API using mobile number and OTP
def login():
    payload = {'mobile_number': mobile_number, 'otp': otp}
    response = requests.post(api_endpoint + '/login', json=payload)
    if response.status_code == 200:
        return response.json()['token']
    else:
        return None

# Define the function to get the channel list
def get_channels(token):
    headers = {'Authorization': 'Bearer ' token}
    response = requests.get(api_endpoint + '/channels', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Define the function to play a channel
def play_channel(channel_id, token):
    headers = {'Authorization': 'Bearer ' token}
    response = requests.get(api_endpoint + '/channels/' + channel_id + '/stream', headers=headers)
    if response.status_code == 200:
        stream_url = response.json()['stream_url']
        xbmc.Player().play(stream_url)
    else:
        xbmcgui.Dialog().ok('Error', 'Failed to play channel')

# Main function
def main():
    token = login()
    if token:
        channels = get_channels(token)
        if channels:
            # Create a list of channels
            channel_list = []
            for channel in channels:
                channel_list.append((channel['name'], channel['id']))

            # Display the channel list to the user
            dialog = xbmcgui.Dialog()
            channel_index = dialog.select('Select a channel', [channel[0] for channel in channel_list])
            if channel_index!= -1:
                channel_id = channel_list[channel_index][1]
                play_channel(channel_id, token)
        else:
            xbmcgui.Dialog().ok('Error', 'Failed to retrieve channel list')
    else:
        xbmcgui.Dialog().ok('Error', 'Failed to login')

# Run the main function
if __name__ == '__main__':
    main()
