# Pour le readme github (pas celui du Gihutb Pages) :
#  quand on glisse dépose la vidéo, il faut qu'elle prenne moins de 10 MB...
#    (renommer le fichier avant le glisser déposer car on voit le nom du fichier sur github)
#
# Ce script sert à compresser la vidéo avec les sous-titres
#
INPUT_FILE="results/slideshow_burned_subs.mp4"
OUTPUT_FILE="results/slideshow_burned_subs_less_than_10_mb.mp4"

ffmpeg -y -i $INPUT_FILE \
	-c:v libx264 -crf 30 -preset slow \
	-an $OUTPUT_FILE

# CRF : entre 0 et 51.
#   - 0 → presque sans perte (très gros fichier).
#   - 51 → compression maximale, qualité très faible.
# Typiquement entre 18 et 28 pour un bon compromis qualité/taille.
