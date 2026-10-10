[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json
source.include_patterns = assets/fonts/*
version = 0.0.1

requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,requests,certifi,urllib3,chardet,idna

entrypoint = main.py

android.accept_sdk_license = True
android.minapi = 21
android.api = 33
android.ndk = 25b
p4a.bootstrap = sdl2

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.enable_androidx = True

android.debug = True
android.logcat_filters = *:S python:D
android.ndk_path =
android.sdk_path =

p4a.source_dir =
p4a.local_recipes =
p4a.allow_prebuilt_recipes = True

buildozer.android.sdk_auto_update = False
buildozer.android.ndk_auto_update = False
