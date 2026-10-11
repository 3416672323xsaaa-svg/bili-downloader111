[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt
version = 0.1

requirements = python3,kivy==2.2.1,pillow,android,cffi==1.16.0,requests==2.28.1,urllib3==1.26.16,certifi,jnius==1.5.0
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.meta_data = android.permission.MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25c
android.sdk = 24
android.archs = arm64‑v8a
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1
