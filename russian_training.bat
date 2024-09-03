@echo off

if %1%==custom python vocabulary.py session custom_words.csv
if %1%==common python vocabulary.py session most_common_words.csv
if %1%==custom_eng python vocabulary.py session_eng custom_words.csv
if %1%==common_eng python vocabulary.py session_eng most_common_words.csv