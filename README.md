# MPD Notificate

Simple notifcation daemon for MPD

Heavily inspired by https://github.com/felipemarinho97/musnify-mpd

## Dependencies
- python-mpd2 https://github.com/Mic92/python-mpd2
- libnotify

## Install
```
make install
```

to enable systemd service:
```
systemctl enable --user --now mpd-notificate.service
```

uninstall:
```
make uninstall
```
