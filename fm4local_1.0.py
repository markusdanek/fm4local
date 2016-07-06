#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import urllib.request
from time import sleep
from sys import getsizeof
import os
# import sys
# from pprint import pprint
# from subprocess import call
# from datetime import datetime
#
#

BROADCAST_URL = 'http://audioapi.orf.at/fm4/json/2.0/broadcasts' # broadcast URL
showlist = [] # initialise showlist variable. Saves properties of each show for download
ignore =["4SL","4UL","4HOP","4TV","4LB","4SS","4DKM"] # Ignore list for shows you dont want to download
nday=4 # number of most recent days you want to download.

rday=7-nday # umber of days to delete from list

print('[ Fetching available shows ]')
days = requests.get(BROADCAST_URL).json() # getting list of available days and shows

for d in days[rday:]: # loop over days
    for show in d['broadcasts']:# loop over shows
        url = '{0}/{1}/{2}'.format(BROADCAST_URL, d['day'], show['programKey']) # building download link for stream URLs
        showStreams = requests.get(url).json() # download streamURLs and other info for the show

        if len(showStreams['streams']) > 0: # checking if list contains at least one stream
            streamList = [] # initialising list of available streams
            for stream in showStreams['streams']: # loop over all streams for the show
                streamList.append(stream['loopStreamId']) # saving all stream URLs of the show

            showURL = streamList # renaming streamList

        else:
            showURL = [] # if no stream is available, showURL is an empty list

        showlist.append({'startISO':show['startISO'], 'title':show['title'], 'programKey':show['programKey'],
                         'day':d['day'], 'showURL':showURL}) # saving all show info as dictionary in a list of shows


for show in showlist: # loop over each show to download all its parts
    if len(show['showURL']) == 0: # check if the list of streams is empty.
        print('****** {0} not available  ******'.format(show['title']))
        continue # if no stream available, continue to next show
    elif show['programKey'] in ignore: # check ignore list if user wants to ignore the show
        print('Ignoring {0}-{1}'.format(show['programKey'],show['title']))
        continue # if show is in the the list, continue to next show
    else:
        for url in show['showURL']: # loop over all parts of the show to download them
            print('[ downloading {0} - part {1} of {2}... ]'.format(show['title'], show['showURL'].index(url) + 1,
                                                                    len(show['showURL'])))

            downURL = 'http://loopstream01.apa.at/?channel=fm4&id={0}&offset=0'.format(url) # build complete stream URL

            # build filename to save the file Title-PartNumber-TotalParts-Day-ProgramKey.mp3
            filename = '{3}-{0}-{1}of{2}-{4}.mp3'.format(show['title'], show['showURL'].index(url) + 1,
                                                        len(show['showURL']), show['day'][4:], show['programKey'])

            filepath = os.path.join("fm4local", filename) # build OS independent filepath

            for attempt in range(9): # try to download the file 10 times, if it still failed, go to next show
                try:
                    response = urllib.request.urlopen(downURL) # request the file
                    data = response.read() # read the file
                    with open(filepath, "wb") as file: # open the local file for saving
                        file.write(data) # write the data to disk
                    print('download and save successful!')
                    break # download and save successful, go to next part of the show
                except ConnectionResetError: # try again in case of connection reset error
                    print('ConnectionResetError occurred. Waiting 10 seconds...')
                    sleep(10)
                    print('Attempt {0}: Trying again.'.format(attempt))
                except OSError: # try again in case of OSError
                    print('OSError occurred. ')
                    print('Attempt {0} failed: Waiting 10 seconds...'.format(attempt+1))
                    sleep(10)
                    if attempt<9:
                        print('Trying again...')
            else: # Failed 10 times to download the file successfully, go to next file
                print('******Exhausted all 10 retries. Continuing to next show...******')

print('Sync complete')




            # file.close() # not necesary when using with...as statements

            # r = requests.get(downURL, stream=True)
            # with open(filename, 'wb') as fd:
            #     for chunk in r.iter_content(chunk_size=1024):
            #         fd.write(chunk)