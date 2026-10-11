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


version = 0.1


# Python依赖
requirements =
    python3,
    kivy==2.3.1,
    pillow,
    requests,
    urllib3,
    certifi,
    pyjnius


# 网络权限
android.permissions = INTERNET


# Android版本
android.api = 33
android.minapi = 30


# NDK版本
android.ndk = 25c


# 只编译你的手机架构
android.archs = arm64-v8a


# APK输出
android.debug_artifact = apk
android.release_artifact = apk


# 使用应用私有存储
android.private_storage = True


# 自动接受协议
android.accept_sdk_license = True


# 竖屏
orientation = portrait


# 不全屏
fullscreen = 0



[buildozer]

log_level = 2

warn_on_root = 1

# 避免重复更新SDK
android.skip_update = True
