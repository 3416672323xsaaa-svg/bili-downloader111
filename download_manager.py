# download_manager.py
# -*- coding: utf-8 -*-
import threading
import os
import sys
import requests

if sys.platform == "android":
    from jnius import autoclass, cast
    MediaMuxer = autoclass('android.media.MediaMuxer')
    MediaFormat = autoclass('android.media.MediaFormat')
    File = autoclass('java.io.File')

class DownloadManager:
    def __init__(self):
        self.tasks = {}

    def get_dst_path(self):
        if sys.platform == "android":
            from android.storage import primary_external_storage_path
            root = primary_external_storage_path()
            save_dir = os.path.join(root, "Download", "BiliPink")
            os.makedirs(save_dir, exist_ok=True)
            return save_dir
        else:
            save_dir = "./download"
            os.makedirs(save_dir, exist_ok=True)
            return save_dir

    def output_dir(self):
        return self.get_dst_path()

    def add_task(self, name, func):
        t = threading.Thread(target=func)
        t.start()
        self.tasks[name] = t

    def download_file(self, url, save_path, progress_callback):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        resp = requests.get(url, headers=headers, stream=True, timeout=30)
        resp.raise_for_status()
        total_size = int(resp.headers.get('content-length', 0))
        downloaded = 0
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024*64):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_callback(downloaded, total_size)
        return save_path

    def merge_media_android(self, video_path, audio_path, out_path):
        """
        安卓原生MediaMuxer无损合并mp4 + m4a，**不需要ffmpeg**
        """
        if sys.platform != "android":
            raise Exception("仅安卓可用")
        # MediaMuxer 输出文件
        output_file = File(out_path)
        muxer = MediaMuxer(output_file.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4)

        # 读取视频轨道信息
        videoFd = File(video_path)
        audioFd = File(audio_path)

        # 注意：Bilibili DASH的视频是H264，音频是AAC，MediaMuxer原生支持
        # 这里使用MediaExtractor解析音视频轨道
        MediaExtractor = autoclass('android.media.MediaExtractor')
        videoExtractor = MediaExtractor()
        videoExtractor.setDataSource(videoFd.getAbsolutePath())
        audioExtractor = MediaExtractor()
        audioExtractor.setDataSource(audioFd.getAbsolutePath())

        # 找到视频轨道
        videoTrackIndex = -1
        for i in range(videoExtractor.getTrackCount()):
            fmt = videoExtractor.getTrackFormat(i)
            mime = fmt.getString(MediaFormat.KEY_MIME)
            if mime.startswith("video/"):
                videoTrackIndex = i
                break
        videoExtractor.selectTrack(videoTrackIndex)
        videoFormat = videoExtractor.getTrackFormat(videoTrackIndex)
        muxerVideoTrack = muxer.addTrack(videoFormat)

        # 找到音频轨道
        audioTrackIndex = -1
        for i in range(audioExtractor.getTrackCount()):
            fmt = audioExtractor.getTrackFormat(i)
            mime = fmt.getString(MediaFormat.KEY_MIME)
            if mime.startswith("audio/"):
                audioTrackIndex = i
                break
        audioExtractor.selectTrack(audioTrackIndex)
        audioFormat = audioExtractor.getTrackFormat(audioTrackIndex)
        muxerAudioTrack = muxer.addTrack(audioFormat)

        # 开始封装
        muxer.start()

        # 缓冲区
        ByteBuffer = autoclass('java.nio.ByteBuffer')
        BufferInfo = autoclass('android.media.MediaCodec$BufferInfo')
        info = BufferInfo()
        info.presentationTimeUs = 0

        # 写入视频样本
        bufSize = 1024 * 512
        buffer = ByteBuffer.allocate(bufSize)
        while True:
            sampleSize = videoExtractor.readSampleData(buffer, 0)
            if sampleSize < 0:
                break
            info.offset = 0
            info.size = sampleSize
            info.presentationTimeUs = videoExtractor.getSampleTime()
            info.flags = videoExtractor.getSampleFlags()
            muxer.writeSampleData(muxerVideoTrack, buffer, info)
            videoExtractor.advance()
            buffer.clear()

        # 写入音频样本
        buffer = ByteBuffer.allocate(bufSize)
        while True:
            sampleSize = audioExtractor.readSampleData(buffer, 0)
            if sampleSize < 0:
                break
            info.offset = 0
            info.size = sampleSize
            info.presentationTimeUs = audioExtractor.getSampleTime()
            info.flags = audioExtractor.getSampleFlags()
            muxer.writeSampleData(muxerAudioTrack, buffer, info)
            audioExtractor.advance()
            buffer.clear()

        # 结束
        muxer.stop()
        muxer.release()
        videoExtractor.release()
        audioExtractor.release()
        return True
