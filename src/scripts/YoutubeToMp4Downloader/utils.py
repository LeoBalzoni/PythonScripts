def clean_filename(name):
    """Ensures each file name does not contain forbidden characters and is within the character limit"""
    #  Windows full path limit should be around 240, cutting down to 175.
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename


def print_metadata(youtube_obj, video_filesize, audio_filesize):
    print("_______________________________________________")
    print(f'Title: {youtube_obj.title}')
    print(f'Author: {youtube_obj.author}')
    print(f'Published date: {youtube_obj.publish_date.strftime("%Y-%m-%d")}')
    print(f'Number of views: {youtube_obj.views}')
    print(f'Length of video: {youtube_obj.length // 60}m {youtube_obj.length % 60}s')
    print(f'Video filesize: {video_filesize} MB')
    print(f'Audio filesize: {audio_filesize} MB')
    print('Starting download..')
    print("_______________________________________________")