[app]

title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt,xml,atlas

version = 0.1

requirements =
    python3,
    kivy==2.2.1,
    pillow,
    requests,
    urllib3,
    certifi,
    jnius==1.5.0,
    cffi

android.permissions =
    INTERNET,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE

android.meta_data = android.permission.MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25c
android.archs = arm64-v8a

android.debug_artifact = apk
android.release_artifact = apk
android.private_storage = True

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
