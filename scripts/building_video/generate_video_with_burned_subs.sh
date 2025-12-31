# marche :
# ffmpeg -i results/slideshow.mp4 \
# 	-vf "subtitles=results/slideshow.srt" \
# 	-c:v libx264 -crf 22 -c:a copy \
# 	results/slideshow_burned_subs.mp4

INPUT_FILE="results/slideshow.mp4"
SUBTITLE_FILE="results/slideshow.srt"
OUTPUT_FILE="results/slideshow_burned_subs.mp4"
# ffmpeg -i $INPUT_FILE -filter_complex "subtitles=$INPUT_FILE:force_style='BackColour=&HA0000000,BorderStyle=4,Fontsize=18'" $OUTPUT_FILE

# test sur plusieurs lignes OK
# attention, les propriétés de "force_style" doivent être à la colonne 0

# Structure d’un code couleur ASS : &H AA BB GG RR   (AA=00 : opaque)

# ffmpeg -y -i $INPUT_FILE -filter_complex "subtitles=$SUBTITLE_FILE:force_style='\
# BackColour=&HA0000000,\
# PrimaryColour=&H00FF0000,\
# BorderStyle=4,\
# Fontsize=16,\
# FontName=Arial'" \
# 	$OUTPUT_FILE

# test custom

# PrimaryColour=&H0001FFFF,\
# BackColour=&HFF000000,\
# OutlineColour=&HFFFFFFFF,\

ffmpeg -y -i $INPUT_FILE -filter_complex "subtitles=$SUBTITLE_FILE:force_style='\
PrimaryColour=&H001FFFFF,\
OutlineColour=&H00000000,\
BorderStyle=1,\
Outline=1,\
Shadow=0,\
Fontsize=14,\
MarginV=20,\
FontName=Arial'" \
	$OUTPUT_FILE

# MarginV pour décaler les subs vers le haut
