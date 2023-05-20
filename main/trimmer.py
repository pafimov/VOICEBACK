import ffmpeg

def trim(in_name, out_name, start, end):
    input_file = ffmpeg.input(in_name)
    pts = "PTS-STARTPTS"
    video = input_file.trim(start=start, end=end).setpts(pts)
    audio = (input_file
            .filter_("atrim", start=start, end=end)
            .filter_("asetpts", pts))
    both = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(both, out_name, format="mp4")
    ffmpeg.run(output, overwrite_output=True)

def trim_audio(in_name, out_name, start, end):
    input_file = ffmpeg.input(in_name)
    pts = "PTS-STARTPTS"
    audio = (input_file
            .filter_("atrim", start=start, end=end)
            .filter_("asetpts", pts))
    output = ffmpeg.output(audio, out_name, format="mp3")
    ffmpeg.run(output, overwrite_output=True)