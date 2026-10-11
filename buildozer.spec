[app]

title = BiliPink

package.name = bilipink
package.domain = org.bilipink


source.dir = .


source.include_exts = py,png,jpg,jpeg,kv,json,txt,xml,atlas


version = 0.1


requirements =
    python3,
    kivy==2.3.1,
    pillow,
    requests,
    urllib3,
    certifi,
    pyjnius


android.permissions = INTERNET


android.api = 33
android.minapi = 30


android.ndk = 25b


android.archs = arm64-v8a


android.debug_artifact = apk
android.release_artifact = apk


android.private_storage = True


android.accept_sdk_license = True


orientation = portrait


fullscreen = 0



[buildozer]

log_level = 2

warn_on_root = 1

android.skip_update = True
