import math

from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import moviepy.editor as mpe
import time
import os

from utils import clean_filename, print_metadata

temp_audio_file_name = 'audio_temp.mp3'
temp_video_file_name = 'video_temp.mp4'


def download_vid(url, res_level='FHD'):
    ti = time.time()
    try:
        yt = YouTube(url,
                     on_progress_callback=download_progress_cb,
                     on_complete_callback=download_complete_cb
                     )
    except VideoUnavailable:
        print(f'Video {url} is unavailable, skipping.')
    else:
        dynamic_streams = []
        if res_level == '4K':
            dynamic_streams = ['2160p|160kbps',
                               '1440p|160kbps',
                               '1080p|160kbps',
                               '720p|160kbps',
                               '720p|128kbps',
                               '480p|160kbps',
                               '480p|128kbps']
        elif res_level == 'FHD':
            dynamic_streams = ['1080p|160kbps', '720p|160kbps', '720p|128kbps', '480p|160kbps', '480p|128kbps']

        video_stream = None
        audio_stream = None
        for ds in dynamic_streams:
            video_stream = yt.streams.filter(res=ds.split('|')[0], progressive=False).first()
            audio_stream = yt.streams.filter(abr=ds.split('|')[1], progressive=False).first()
            if (audio_stream is not None) & (video_stream is not None):
                print(f'Found {ds} stream')
                break

        print_metadata(yt, video_stream.filesize_mb, audio_stream.filesize_mb)

        video_stream.download(filename=temp_video_file_name)
        audio_stream.download(filename=temp_audio_file_name)

        join_video_and_audio_files(yt)

        print(f'Video successfully downloaded from {url}')
        seconds_taken = time.time() - ti
        print(f'Time taken: {math.floor(seconds_taken // 60)}m {math.floor(seconds_taken % 60)}s')


def download_progress_cb(stream, chunk, bytes_left):
    if stream.audio_codec is not None:
        return
    filesize_bytes = stream.filesize
    downloaded_bytes = filesize_bytes - bytes_left
    downloaded_percentage = downloaded_bytes / filesize_bytes * 100
    formatted_percentage = '{:.0f}%'.format(downloaded_percentage)
    print(f'{formatted_percentage} complete..')


def download_complete_cb(stream, file_path):
    if stream.audio_codec is not None:
        return
    print(f'Completed download of {stream.title}')


def join_video_and_audio_files(yt_obj):
    # TODO try ffmpeg instead to see if it's any faster
    # Setting the audio to the video
    video = mpe.VideoFileClip(temp_video_file_name)
    audio = mpe.AudioFileClip(temp_audio_file_name)
    final = video.set_audio(audio)
    # Output result
    final.write_videofile(clean_filename(yt_obj.title) + '.mp4')
    # Delete video and audio to keep the result
    os.remove(temp_video_file_name)
    os.remove(temp_audio_file_name)


video_link = input("Put your Youtube link here! URL: ")
download_vid(video_link, '4K')
