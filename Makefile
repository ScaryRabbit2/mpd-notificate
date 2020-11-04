SOURCE=mpd-notificate.py
DESTINATION=/usr/bin/mpd-notificate

SERVICE=mpd-notificate.service
SERVICE-DESTINATION=/etc/systemd/user/$(SERVICE)

install:
	sudo cp $(SOURCE) $(DESTINATION)
	sudo cp $(SERVICE) $(SERVICE-DESTINATION)

uninstall:
	sudo rm $(DESTINATION)
	sudo rm $(SERVICE-DESTINATION)
