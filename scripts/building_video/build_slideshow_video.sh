INPUT_DIR="../../readme_files/screenshots"

OUTPUT_DIR="results"

MISC="$INPUT_DIR/misc"
DRAWIO="$INPUT_DIR/drawio"
AIRFLOW="$INPUT_DIR/airflow"
FASTAPI="$INPUT_DIR/fastapi/slideshow"
POWERBI_ALL_OFFERS="$INPUT_DIR/power_bi/reports/1--all-offers"
POWERBI_COMPETENCES_XP="$INPUT_DIR/power_bi/reports/2--competences-experiences"
POWERBI_QUALITES_QUALIFS="$INPUT_DIR/power_bi/reports/3--qualites-qualifications"
POWERBI_LOCATION="$INPUT_DIR/power_bi/reports/4--location"
POWERBI_KEYWORDS="$INPUT_DIR/power_bi/reports/5--keywords"
PROM_GRAF="$INPUT_DIR/grafana/my_dashboard/dags_activity/with_annotations"

WIDTH=1920
HEIGHT=1080

# WIDTH=1280
# HEIGHT=720

FILES=(

	# 1. Collecte des données via API (~200k offres d'emploi récupérées en 10 mois, avec ~50 attributs par offre d'emploi)
	$MISC/"json_document.png"

	# 2. Diagramme UML (schéma en flocon de neige)
	$DRAWIO/"UML.png"

	# 3. Architecture dockerisée
	$DRAWIO/"architecture_00--ALL.png"
	$DRAWIO/"architecture_01--ETL.png"
	$DRAWIO/"architecture_02--API.png"
	$DRAWIO/"architecture_03--VIZ.png"
	$DRAWIO/"architecture_04--MON.png"
	$DRAWIO/"architecture_00--ALL.png"

	# 4. Conteneurs docker
	$MISC/"docker_ps.png"

	# 5. ETL grâce à une orchestration de tâches avec Airflow
	$AIRFLOW/"duration_dags.png"
	$AIRFLOW/"graphs_dags_1_2_from_pptx.png"

	# 6. Définition d'APIs avec FastAPI
	$FASTAPI/"00--fullscreen.png"
	$FASTAPI/"11--1-1b.png"
	$FASTAPI/"12--1-4.png"
	$FASTAPI/"21--2-1.png"
	$FASTAPI/"22--2-5.png"
	$FASTAPI/"31--3-1_with_black_sides.png" # barres sur les côtés pour éviter un resizing en plein écran par ffmpeg

	# 7. Data viz avec Power BI
	$POWERBI_ALL_OFFERS/"1-1.png"
	$POWERBI_ALL_OFFERS/"1-2--DA-DE-DS.png"
	$POWERBI_COMPETENCES_XP/"2-1.png"
	$POWERBI_QUALITES_QUALIFS/"3-1.png"
	$POWERBI_LOCATION/"4-1.png"
	$POWERBI_KEYWORDS/"5-1.png"
	# --
	$POWERBI_ALL_OFFERS/"1-5--DE.png"
	$POWERBI_COMPETENCES_XP/"2-4--DE.png"
	$POWERBI_QUALITES_QUALIFS/"3-4--DE.png"
	$POWERBI_LOCATION/"4-4--DE.png"
	$POWERBI_KEYWORDS/"5-4--DE.png"

	# 8. Monitoring avec Prometheus/Grafana
	$PROM_GRAF/"0-airflow_dags_datetime.png"
	$PROM_GRAF/"1-cadvisor.png"
	$PROM_GRAF/"2-postgres-exporter.png"
	$PROM_GRAF/"3-statsd-exporter.png"
	$PROM_GRAF/"4-node-exporter.png"
)

# rm $OUTPUT_DIR/* # pour être sûr de repartir de zéro

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
#
#
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
	-loop 1 -t 5 -i $OUTPUT_DIR/010.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/011.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/012.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/013.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/014.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/015.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/016.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/017.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/018.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/019.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/020.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/021.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/022.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/023.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/024.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/025.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/026.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/027.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/028.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/029.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/030.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/031.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/032.png \
	-loop 1 -t 5 -i $OUTPUT_DIR/033.png \
	-filter_complex "
[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v1];
[v1][2:v]xfade=transition=fade:duration=1:offset=8[v2];
[v2][3:v]xfade=transition=fade:duration=1:offset=12[v3];
[v3][4:v]xfade=transition=fade:duration=1:offset=16[v4];
[v4][5:v]xfade=transition=fade:duration=1:offset=20[v5];
[v5][6:v]xfade=transition=fade:duration=1:offset=24[v6];
[v6][7:v]xfade=transition=fade:duration=1:offset=28[v7];
[v7][8:v]xfade=transition=fade:duration=1:offset=32[v8];
[v8][9:v]xfade=transition=fade:duration=1:offset=36[v9];
[v9][10:v]xfade=transition=fade:duration=1:offset=40[v10];
[v10][11:v]xfade=transition=fade:duration=1:offset=44[v11];
[v11][12:v]xfade=transition=fade:duration=1:offset=48[v12];
[v12][13:v]xfade=transition=fade:duration=1:offset=52[v13];
[v13][14:v]xfade=transition=fade:duration=1:offset=56[v14];
[v14][15:v]xfade=transition=fade:duration=1:offset=60[v15];
[v15][16:v]xfade=transition=fade:duration=1:offset=64[v16];
[v16][17:v]xfade=transition=fade:duration=1:offset=68[v17];
[v17][18:v]xfade=transition=fade:duration=1:offset=72[v18];
[v18][19:v]xfade=transition=fade:duration=1:offset=76[v19];
[v19][20:v]xfade=transition=fade:duration=1:offset=80[v20];
[v20][21:v]xfade=transition=fade:duration=1:offset=84[v21];
[v21][22:v]xfade=transition=fade:duration=1:offset=88[v22];
[v22][23:v]xfade=transition=fade:duration=1:offset=92[v23];
[v23][24:v]xfade=transition=fade:duration=1:offset=96[v24];
[v24][25:v]xfade=transition=fade:duration=1:offset=100[v25];
[v25][26:v]xfade=transition=fade:duration=1:offset=104[v26];
[v26][27:v]xfade=transition=fade:duration=1:offset=108[v27];
[v27][28:v]xfade=transition=fade:duration=1:offset=112[v28];
[v28][29:v]xfade=transition=fade:duration=1:offset=116[v29];
[v29][30:v]xfade=transition=fade:duration=1:offset=120[v30];
[v30][31:v]xfade=transition=fade:duration=1:offset=124[v31];
[v31][32:v]xfade=transition=fade:duration=1:offset=128,format=yuv420p[v]
" \
	-map "[v]" \
	-c:v libx264 -pix_fmt yuv420p \
	$OUTPUT_DIR/slideshow.mp4
