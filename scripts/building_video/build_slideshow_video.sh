INPUT_DIR="../../readme_files/screenshots"

OUTPUT_DIR="results"

MISC="$INPUT_DIR/misc"
DRAWIO="$INPUT_DIR/drawio"

WIDTH=1920
HEIGHT=1080

# WIDTH=1280
# HEIGHT=720

FILES=(

	# 1. Récupération des données via API (~50 attributs par offre d'emploi)
	$MISC/"json_document.png"

	# 2. Diagramme UML (modèle snowflake)
	$DRAWIO/"UML.png"

	# 3. Architecture du projet dockerisée
	$DRAWIO/"architecture_00--ALL.png"
	$DRAWIO/"architecture_01--ETL.png"
	$DRAWIO/"architecture_02--API.png"
	$DRAWIO/"architecture_03--VIZ.png"
	$DRAWIO/"architecture_04--MON.png"
	$DRAWIO/"architecture_00--ALL.png"

	# 4. Conteneurs docker
	$MISC/"docker_ps.png"

	# 5. Airflow pour l'orchestration des tâches (ETL)

	# 6. FastAPI pour la définition d'APIs

	# 7. Power BI pour la data viz

	# 8. Prometheus/Grafana pour le monitoring

)

rm $OUTPUT_DIR/* # pour être sûr de repartir de zéro

i=1
for img in "${FILES[@]}"; do
	printf -v num "%03d" "$i"
	ffmpeg -y -i "$img" \
		-vf "scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease,\
	     pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,\
	     setsar=1" \
		"$OUTPUT_DIR/$num.png"

	((i++))
done

ffmpeg -y \
	-loop 1 -t 5 -i $OUTPUT_DIR/001.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/002.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/003.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/004.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/005.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/006.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/007.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/008.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/009.png \
	-filter_complex "
[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v1];
[v1][2:v]xfade=transition=fade:duration=1:offset=8[v2];
[v2][3:v]xfade=transition=fade:duration=1:offset=12[v3];
[v3][4:v]xfade=transition=fade:duration=1:offset=16[v4];
[v4][5:v]xfade=transition=fade:duration=1:offset=20[v5];
[v5][6:v]xfade=transition=fade:duration=1:offset=24[v6];
[v6][7:v]xfade=transition=fade:duration=1:offset=28[v7];
[v7][8:v]xfade=transition=fade:duration=1:offset=32,format=yuv420p[v]
" \
	-map "[v]" \
	-c:v libx264 -pix_fmt yuv420p \
	$OUTPUT_DIR/output.mp4
