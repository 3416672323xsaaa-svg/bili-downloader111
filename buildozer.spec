[app]

# APP名称
title = BiliPink

# 包名
package.name = bilipink
package.domain = org.bilipink

# 项目目录
source.dir = .

# 包含文件
source.include_exts = py,png,jpg,jpeg,kv,json,txt,xml,atlas

# 版本
version = 0.1


# Python依赖
requirements =
    python3
    kivy==2.3.1
    pillow
    requests
    urllib3
    certifi
    pyjnius


# 网络权限
android.permissions =
    INTERNET


# Android版本
# Android 13 API
android.api = 33

# 支持 Android 11+
android.minapi = 30

# NDK版本
android.ndk = 25c

# NDK编译接口
android.ndk_api = 30


# 只编译你的手机架构
android.archs = arm64-v8a


# APK输出
android.debug_artifact = apk
android.release_artifact = apk


# Android设置
android.accept_sdk_license = True

# 不使用私有存储
# 让下载文件可以访问公共Download目录
android.private_storage = False


# 屏幕方向
orientation = portrait

# 不全屏
fullscreen = 0



[buildozer]

# 显示详细日志
log_level = 2

# GitHub Actions允许root
warn_on_root = 1

# 不重复下载SDK
android.skip_update = True
