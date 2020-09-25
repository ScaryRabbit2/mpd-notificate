#!/bin/python3
import time
import os
from pathlib import Path
from mpd import MPDClient
from mpd import CommandError
from subprocess import Popen

client = MPDClient()
CACHE = str( Path.home() ) + '/.cache/mpd-notify'
HOST = "localhost"
PORT = 6600
	
def notify ( head, body, albumArt ):
	if albumArt:
		Popen(['notify-send', '-u', 'low', '-i', albumArt, head, body])
	else:
		Popen(['notify-send', '-u', 'low', head, body])

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

def getImage ( path ):
	try:
		buf = client . albumart ( path )		
	except CommandError:
		return ""

	fileName = CACHE + "/tmp.png"

	file = open( fileName, "wb" )
	file.write( buf )
	file.close()
	return fileName

def getData ( song ):
	head = ""
	body = ""
	folder, file = parseFile( song['file'] )

	if 'artist' in song:
		head = song['artist']
	else: head = folder

	if 'title' in song:
		body = song['title']
	else: body = file

	return head, body

def handleNotify ( song , stop = False ):
	if 'file' in song:
		head, body = getData( song )
		image = getImage ( song['file']  )
	else:
		image = head = body = ""

	if stop:
		head = 'Stopped'
		image = ""

	notify( head, body, image )

def loop():
	prevSong = client . status() [ 'state' ]
	prevStatus = client . currentsong()

	while True:
		client . idle ( 'player' )
		curSong = client . currentsong()
		curStatus = client . status() [ 'state' ]

		if curSong != prevSong or curStatus != prevStatus:
			if curStatus == 'play':
				handleNotify( curSong )
			else:
				handleNotify( curSong, True )

		prevSong = curSong
		prevStatus = curStatus


def main():
	client . connect ( HOST, PORT )
	loop()
	
def start():
	try:
		main()
	except ConnectionError:
		start()

if __name__ == "__main__":
	start()