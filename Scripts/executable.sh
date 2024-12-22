input_file_path="$1"

if [ $# -ne 1 ]; then
    echo "Il faut un argument qui est le nom complet du fichier texte d'entrée."
else
    python analyseur.py "$input_file_path" | tee result.txt
fi