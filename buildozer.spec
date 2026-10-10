[app]

title = BiliPink

package.name = bilipink

package.domain = org.bilipink

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json

version = 0.0.1

requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,requests,yt-dlp,certifi,urllib3,chardet,idna

entrypoint = main.py

android.accept_sdk_license = True

android.minapi = 21

android.api = 33

android.ndk = 25b

android.bootstrap = sdl2

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.enable_androidx = True
