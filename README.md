# Multiclassification of Different Music Composers using Piano Rolls, extracted from MIDI files using Python.
This project is part of the AAI-511 Neural Networks course in the Master's of Science in Applied Artificial Intelligece Program at the University of San Diego (USD).

**-- Project Status: Completed**

To run this project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/Giant-Leap-ai/MSAAI-511-group-4.git```
2. Run with Jypiter: https://jupyter.org/install 

## Project Intro/Objective
The main objective of this project is to create two multiclassification computer vision models that are able to classify MIDI files -> Piano Rolls -> Composer (Bach, Bethoven, Chopin, Mozart). For this task we compared CNN and CNN-LSTM models. We got the data from: 
```
path = kagglehub.dataset_download("blanderbuss/midi-classic-music")
```

### Methods Used:
- Data Donwloading and reading, all steps are inside notebooks with ```data_reading.ipynb```