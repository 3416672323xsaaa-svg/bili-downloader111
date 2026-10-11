[app]

# 手机桌面显示名称
title = BiliPink

# 包名
package.name = bilipink
package.domain = org.bilipink


# 项目目录
source.dir = .

# 包含文件
source.include_exts = py,png,jpg,jpeg,kv,json,txt,xml,atlas


version = 0.1


# Python依赖
requirements =
    python3,
    kivy==2.3.1,
    pillow,
    requests,
    urllib3,
    certifi,
    pyjnius,
    cffi


# 网络权限
android.permissions = INTERNET


# Android版本
# Android 11+
android.api = 33
android.minapi = 30


# NDK
android.ndk = 25c


# 你的手机 Redmi K60E
android.archs = arm64-v8a


# APK输出
android.debug_artifact = apk
android.release_artifact = apk


# 使用应用私有目录
android.private_storage = True


# 接受SDK协议
android.accept_sdk_license = True


# 横竖屏
orientation = portrait

fullscreen = 0



[buildozer]

log_level = 2

warn_on_root = 1

android.skip_update = True
