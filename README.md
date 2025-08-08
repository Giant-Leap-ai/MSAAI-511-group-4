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

### Methods and classes Used:
- Data Downloading, all steps are inside notebooks with ```data_reading.ipynb```
- Data Reading using a customized class called ``` DataRetriever(data_path = data_path)```.The following is the command to use after downloading data to obtain foldered data structure.

```
retriever = DataRetriever(data_path = data_path)
retrieved_path = retriever.subdivide_data()
```

##### Folder Structure
project-name/
├── data/                  # Raw and processed datasets
│   ├── datasets/          # Unmodified original data from kagglehub
│   └── final_proj_data/   # Subdivided data of desired 4 composers.
        ├── Bach/
        ├── Bethoven/
        ├── Chopin/
        ├── Mozart/
├── notebooks/             # Jupyter notebooks containing codes and models
├── src/                   # Source code for the project
│   ├── __init__.py
│   ├── datadownloader.py  # Contains code to download raw data from kagglehub
│   ├── utils.py           # All functions pertinent to preprocess MIDI -> `torch.tensor()`
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

- Data Cleaning and preparation, all steps and logic are in notebooks ```data_piano_roll_extraction.ipynb``` inside notebooks. The following are the commands used to obtain the piano rolls data, obtaining a tensor of size: `(480, 125, 2515)`

```
midipreprocesser = MidiPreprocesser(data_path = data_path)
midiobj, labels_composer = midipreprocesser.get_midi_info()

list_np_arrays, list_composer_names, list_song_names = obtain_piano_rolls(midiobject = midiobj)

equalizer = PianoRollsDiscreteEqualizer(piano_rolls = list_np_arrays, threshold = 2515)
eq_piano_rolls = equalizer.get_equalized()
```

##### Piano Roll Extracted, Repeated, and Equalized to 2515:

<img width="1415" height="670" alt="Image" src="https://github.com/user-attachments/assets/f3158cad-b685-427f-b4b3-d80c281da882" />

