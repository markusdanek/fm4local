# fm4local

Python 3.5 script to download all fm4_7tage shows to a local folder. The program works without any external dependencies for the goal is to install and run it easily on a Freenas server as daily chron job. 

Licenced under the BSD-2-Clause License

## Features
* Downloads all FM4 streams of a defined number of days (max. 7) in the format date-title-partOfShow-ShowID.mp3
* Shows you dont want to be downloaded can be put on the ignorelist using their showID
* Number of days is defined by the variable nday in the script (I hope to make that easier in the future)
* Files older than nday are deleted on each run
* Files already downloaded and within the range of nday are skipped. No need to re-download the whole week every day. 


## To-Do for 2.0
* Introduce flag system for destination folder flag
* separate out day limitation
* Stitch multipart shows to single mp3
* id3 tagging
* implement logfile system

