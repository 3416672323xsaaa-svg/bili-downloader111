[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt
version = 0.0.1

requirements = python3,kivy==2.3.1,requests,pillow,android,pyopenssl

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.accept_sdk_license = True
android.enable_androidx = True
android.ndk = 25b

# Android 11+
android.minapi = 30
# 改成33，兼容性稳定，不要35
android.api = 33
android.archs = arm64-v8a
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
