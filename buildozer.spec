[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt
version = 0.0.1

# 锁定版本！解决cffi找不到的报错，完整依赖：解析+下载封面全部可用
requirements = python3,kivy==2.3.1,pillow,android,cffi==1.16.0,requests==2.28.1,urllib3==1.26.16,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.enable_androidx = True
android.ndk = 25b

# Android 11+
android.minapi = 30
android.api = 33
android.archs = arm64-v8a
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
