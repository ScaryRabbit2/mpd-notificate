#!/bin/python3

import time
import os
from pathlib import Path
from mpd import MPDClient
from mpd import CommandError
from subprocess import Popen
from gi.repository import Notify
from gi.repository.GdkPixbuf import Pixbuf

# cache folder for storing album arts
CACHE = str( Path.home() ) + '/.cache/mpd-notify'

# conection to MPD
HOST = "localhost"
PORT = 6600

#global MPD variable
client = MPDClient()

#init libnotify
Notify.init("mpd-notificate")

def notify ( head, body, albumArt ):
	notif = Notify.Notification.new(head, body)
	notif.set_urgency( Notify.Urgency.LOW )
	if albumArt:
		pic = Pixbuf .new_from_file(albumArt)
		notif.set_image_from_pixbuf(pic)

	notif.show()

def getImage ( path ):
	fileName = CACHE + "/tmp.png"

	#does not get the same picture more times
	if getImage . prevPath == path:
		return fileName
	getImage . prevPath = path

	# try to get image
	try:
		buf = client . albumart ( path )
	except CommandError:
		return ""

	# write raw image to file
	file = open( fileName, "wb" )
	file.write( buf )
	file.close()
	return fileName

# Parses path into folders and file
def parseFile ( path ):
	folder = ""
	file = ""
	for i in path:
		if ( i == '/' ):
			folder += file if not folder else '/' + file
			file = ""
		else:
			file += i

	return folder, file

def getData ( song ):
	head = ""
	body = ""
	folder, file = parseFile( song['file'] )

	# if artist available, otherwise folder name
	if 'artist' in song:
		head = song['artist']
	else: head = folder

	# if title available, oherwise file name
	if 'title' in song:
		body = song['title']
	else: body = file

	return head, body

# handles metadata
def handleNotify ( song , stop = False ):
	# if there is no selected, it doesnt try to get them
	if 'file' in song:
		head, body = getData( song )
		image = getImage ( song['file']  )
	else:
		image = head = body = ""

	# stopped message with no picture
	if stop:
		head = 'Stopped'
		image = ""

	notify( head, body, image )

# endless loop, checks for activity
def loop():
	prevSong = client . status() [ 'state' ]
	prevStatus = client . currentsong()

	while True:
		client . idle ( 'player' )
		curSong = client . currentsong()
		curStatus = client . status() [ 'state' ]

		if prevStatus == 'play':
			if curStatus in [ 'pause', 'stop' ]: # stop playing
				handleNotify( curSong, True )
			elif curSong != prevSong: # change playing song
				handleNotify( curSong )
		elif curStatus != prevStatus: # start playing
			handleNotify ( curSong )

		prevSong = curSong
		prevStatus = curStatus

# starts loop and connects to client
def main():
	client . connect ( HOST, PORT )
	getImage . prevPath = ""
	loop()

if __name__ == "__main__":
	main()
