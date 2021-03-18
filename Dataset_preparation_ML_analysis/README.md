# Machine Learning preparation and analysis codes

## Introduction

This folder contains the routine designed by Maria De Luca during her Master Thesis.

A dataset containing the base-tracks for shower candidate is produced, then provided as input to a Random Forest classifier.

There are two versions, one for simulation csv and the other for data csv

Lettura_csv analyses the ML output and it produces histograms

## Dataset preparation from simulation

The scripts need to be launched in the following order (Concat_dataframe.py is launched twice):

1. Proiezioni.py

2. Inizio_sciame.py

3. Rect.py

4. Rect_crescenti.py

5. Taglio_Theta.py

6. Concat_dataframe.py

7. Ricerca_new.py

8. Concat_dataframe.py

9. Random_Forest_Ishower.py

## Dataset preparation from data

The scripts need to be launched in the following order (Concat_dataframe.py is launched twice):

1. Proiezioni_Theta.py

Between 1 and 2, produce "Inizio_candidati_sciami.csv"
Segments with the same TrackID within first three plates with theta <= 50 mrad.
Take last segment of the track

2. Data_rect.py

3. Data_rect_crescenti.py

4. Data_taglio_Theta.py

5. Concat_dataframe.py

6. Ricerca_complete.py

7. Concat_dataframe.py

9. Random_Forest_Ishower.py
