BiliPink 安卓 B 站视频下载器（无登录版）

本包包含：
- main.py：粉色中文 Kivy UI，支持 BV / AV / b23.tv 和分享文案输入、视频信息展示、清晰度选择、分P选择、下载进度和封面下载。
- bili_api.py：B站视频元信息、互动统计、分P信息、格式查询、封面下载。
- downloader.py：视频/画面/音频下载；清晰度选择和分P选择会传入下载流程。
- download_manager.py：下载任务和输出目录管理。
- assets/fonts/NotoSansCJK-Regular.ttc：中文字体，减少安卓中文方框问题。
- requirements.txt：Python依赖。

重要说明：
1. 当前版本未集成可确认能在 Android 上运行的 FFmpeg 二进制。完整视频遇到分离的视频/音频流时，MP4合并可能失败；仅音频转 MP3 也需要 FFmpeg。程序会提示错误，不应把未测试功能当成已保证。
2. 安卓 Kivy 默认把文件保存在应用私有目录的 Downloads 子目录。卸载应用可能删除这些文件；本版本尚未实现系统公共下载目录/SAF 文件选择器。
3. 不登录时，B站可能限制部分清晰度或格式；列表以当前 yt-dlp 实际取得的格式为准。
4. 分P选择会将选中的 P 编号加到下载链接。尚未在真实安卓设备上完成端到端下载测试。
5. Buildozer 配置的 source.include_exts 必须包含 py,ttc,png,jpg,jpeg,atlas,txt 等，才能把中文字体打进 APK。请保留你现有的 buildozer.spec 和 .github/workflows，不要删除或覆盖构建配置。

建议 requirements 至少包含 kivy==2.3.1、requests、yt-dlp；实际 APK 构建还需使用项目现有的 Buildozer / python-for-android 配置。
