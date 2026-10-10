[app]

title = BiliPink

package.name = bilipink

package.domain = org.bilipink


source.dir = .

source.include_exts = py,png,jpg,kv,atlas,ttf,txt


version = 0.0.1


requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,requests,libffi


entrypoint = main.py


android.accept_sdk_license = True

android.minapi = 21

android.api = 33

android.ndk = 25b

android.archs = arm64-v8a

android.ndk.parallel_jobs = 2


exclude_dirs = tests,.git,__pycache__


android.gradle_download = https://services.gradle.org/distributions/gradle-7.6.4-all.zip

android.gradle_plugin = 7.4.2

android.ndk_api = 21


p4a.bootstrap = sdl2


p4a.gradle_options = -Dorg.gradle.java.home=/usr/lib/jvm/temurin-17-jdk-amd64


android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


android.aab = False



[buildozer]

log_level = 2

warn_on_root = 1
