[app]
title = DL6-OxygenFight
package.name = dl6
package.domain = craft.soul
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,ogg
source.include_patterns = image/*
version = 12.28
fullscreen=0
requirements = python3,kivy==2.2.1,plyer,kivymd,libiconv,libffi
icon.filename = image/inhalation.png
presplash.filename = image/title.png
orientation = portrait
entrypoint = main.py
android.accept_sdk_license = True
android.allow_api_min = 21
android.api = 33
android.minapi = 21
android.ndk = 25b
exclude_patterns = **/test/*, **/tests/*
android.gradle_download = https://services.gradle.org/distributions/gradle-7.6.4-all.zip
android.gradle_plugin = 7.4.2
android.sdk = 33
android.ndk_api = 21
p4a.gradle_dependencies = gradle:7.6.4
p4a.bootstrap = sdl2
p4a.gradle_options = -Dorg.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
