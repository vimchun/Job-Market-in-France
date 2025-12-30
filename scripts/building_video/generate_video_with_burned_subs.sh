ffmpeg -i results/slideshow.mp4 \
	-vf "subtitles=results/slideshow.srt" \
	-c:v libx264 -crf 22 -c:a copy \
	results/slideshow_burned_subs.mp4
