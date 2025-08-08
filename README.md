# Multiclassification of Different Music Composers using Piano Rolls, extracted from MIDI files using Python.
This project is part of the AAI-511 Neural Networks course in the Master's of Science in Applied Artificial Intelligece Program at the University of San Diego (USD).

**-- Project Status: Completed**

To run this project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/Giant-Leap-ai/MSAAI-511-group-4.git```
2. Run with Jypiter: https://jupyter.org/install 

## Contrbutors:
- Lucas Young
- Titouan Magret
- Juan Pablo Triana Martinez
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
```
project-name/
├── data/                  # Raw and processed datasets
│   ├── datasets/          # Unmodified original data from kagglehub
│   └── final_proj_data/   # Subdivided data of desired 4 composers.
        ├── Bach/          # Subfolder containing all MIDI files of Bach
        ├── Bethoven/      # Subfolder containing all MIDI files of Bethoven
        ├── Chopin/        # Subfolder containing all MIDI files of Chopin
        ├── Mozart/        # Subfolder containing all MIDI files of Mozart
├── notebooks/             # Jupyter notebooks containing codes and models
├── src/                   # Source code for the project
│   ├── __init__.py
│   ├── datadownloader.py  # Contains code to download raw data from kagglehub
│   ├── utils.py           # All functions pertinent to preprocess MIDI -> `torch.tensor()`
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

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

- CNN Baseline model training on `(480, 125, 2515)` piano rolls. These were further transformed to `(Batch_size, 1, 125, 2515)` to be used with a small VGG16 architecture model, insipired by: 
https://poloclub.github.io/cnn-explainer/. All the steps can be found in `cnn_basemodel.ipynb`.

- CNN-LSTM model training on `(480, 125, 2515)` piano rolls. These were further transformed to `(Batch_size, Seq, 1, 125, 2515)` to be used with an adapted VGG16 inspired architecture model, alongside an LSTM cell. All the steps can be found in `cnn_lstm.ipynb`.

## Project Description

#### Dataset
- **Source**: https://www.kaggle.com/datasets/blanderbuss/midi-classic-music
- **Variables and Size** `music.midi` files containing metadata information of music partitutes of 175 composers, including: Bach, Beethoven, Mozart, Brahms, Chopin, Tchaikovsky, Strauss, Stravinski, Prokofiev, Rachmaninov, Bernstein, Bartok, Handel, Ravel, Scriabin, and others

#### Project Steps:
1. **Data Downloading/Preparation**: All data from MIDI files was donwloaded, and further separated into subfolders in order to analyze only four desired composers: Bach, Bethoven, Chopin, and Mozart.
2. **Data Cleaning/Preparation**: Since the CNN and CNN-LSTM models required 2D data, the MIDI files were preprocessed using customized classes, contained in `src/`, in order to obtain from `music.midi` -> `np.ndarray` of piano rolls. 
3. **EDA Piano Roll Data**: Once the piano rolls were found, and EDA was done to see how the piano rolls of different duration times behaved. Using different discretized time of songs, we found the median of all songs and used it as a threshold to *Equalize* all songs.
4. **CNN Model Training and Analysis**: The model's were evaluated based on The models were evaluated based on F1 score, Accuracies, Precisions, Recalls, and F1 Scores. We also used visualized confusion matrices
5. **CNN-LSTM Model Training and Analysis** Same as CNN, but with the added caviat of a sequence length used.

### Results
**CNN Confusion Matrix and Metrics**:
<img width="705" height="627" alt="Image" src="https://github.com/user-attachments/assets/d0d1f903-5050-4499-ab7e-06a3489faa13" />

**CNN-LSTM Confusion Matrix and Metrics**:
<img width="693" height="623" alt="Image" src="https://github.com/user-attachments/assets/5fd40999-4fc8-4e13-9a0e-edaa6a5b4ff5" />

Looking into both models, is safe to say the CNN-LSTM model outperforms CNN metrics by almost 10%~12% on all. There is indeed considerations regarding the distribution of the `y_train` used. 

There is slight data imbalances that were not addressed, so a consideration to improve even more is to undersample or data augment to have a balanced dataset for training. 

<img width="1606" height="428" alt="Image" src="https://github.com/user-attachments/assets/6e70568b-2987-462b-9d3a-56521b5761a6" />

Additionally, we explored relatively small sized compact models, so the possibility to use even deeper neural networks with more than 5 layers, or more complicated ones like computer vistion transformers or autoencoders, are also a possibility.

The key thing to note was the step y step process to obtain an entire project from MIDI -> Piano Rolls -> Composer Labelling using `Python`, and `PyTorch`.

Thank you for your time!

