python3 "/home/deva/Documents/programs/other/ods-to-csv.py" "/home/deva/Documents/pali_resources/Pātimokkha Word by Word.ods" Sheet1 20

cd "/home/deva/Documents/programs/other"
jupyter nbconvert --to script "patimokkha filter.ipynb"
python3 "patimokkha filter.py"
