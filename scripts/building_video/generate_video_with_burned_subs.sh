INPUT_FILE="results/slideshow.mp4"
SUBTITLE_FILE="results/slideshow.srt"
OUTPUT_FILE="results/slideshow_burned_subs.mp4"

# Notes :
#   - Attention, les propriétés de "force_style" doivent être à la colonne 0
#   - Structure d’un code couleur ASS : &H AA BB GG RR   (AA=00 : opaque)
#   - MarginV pour décaler les subs vers le haut

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
