[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt
version = 0.0.1

requirements = python3,kivy==2.3.1,requests,pillow,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.accept_sdk_license = True

# Android 11+
android.minapi = 30
# Android 14/15兼容
android.api = 35
android.archs = arm64-v8a
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
