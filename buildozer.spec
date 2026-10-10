[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,ttf,txt,json

version = 0.0.1

requirements = python3,kivy==2.3.1,pillow,requests,certifi

entrypoint = main.py

android.accept_sdk_license = True
android.minapi = 21
android.api = 33
android.ndk = 25b
android.ndk_api = 21

p4a.python_version = 3.9
p4a.bootstrap = sdl2

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.enable_androidx = True

buildozer.android.sdk_auto_update = False
buildozer.android.ndk_auto_update = False

[buildozer]
log_level = 2
warn_on_root = 0
