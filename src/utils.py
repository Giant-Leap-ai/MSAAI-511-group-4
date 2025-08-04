from pathlib import Path
import numpy as np
from mido import MidiFile
from tqdm import tqdm
from typing import Union, Tuple, List

class MidiPreprocesser:
    '''
    Class that would process all files found
    inside the final_proj_data folder and retrieve
    all the midi info for each of the files

    Args:
        data_path : Path from pathlib where data folder is located.

    Returns:
        midi_object: will see :)

    Example:
        midipreprocesser = MidiPreprocesser(data_path = set_path)
        midiobj, labels_composer = midipreprocesser.get_midi_info()
    '''

    def __init__(self, data_path:Path):
        self.data_path = data_path
    
    def _convert_composers_class_idx(self, labels: List[str]) -> List[int]:
        class_indices = []
        for composer in labels:
            if composer == "Bach":
                class_indices.append(1)
            elif composer == "Beethoven":
                class_indices.append(2)
            elif composer == "Chopin":
                class_indices.append(3)
            elif composer == "Mozart":
                class_indices.append(4)
            else:
                class_indices.append(0)
        return class_indices

    def get_midi_info(self) -> Tuple[List[Tuple[str, MidiFile]], List[int]]:
        midis = []
        labels_composer = []
        for root, dirs, files in tqdm(self.data_path.walk(), desc="Reading composers.."):
            count = 0
            for file in tqdm(files, desc=f"Reading_{root.stem} files...", total=len(files)):
                if file.endswith(".mid"):
                    try:
                        midis.append((root.stem + "_" + str(count), MidiFile(Path(root) / file)))
                        labels_composer.append(root.name)
                        count += 1
                    except:
                        print(f"{file} cannot be read, is skipped")
                        continue
        labels_composer = self._convert_composers_class_idx(labels_composer)
        return midis, labels_composer

class MidiToNumpy:
    '''
    Class that would process one Midifile
    object, and do the following:
        - Set the midi ticks per beat
        - Set the fs to discretize Midi information -> Discrete symbolic numpy array
        - Iterate across all tracks and find events of the following:
            * set_tempo
            * note_on
            * note_off
        - create a numpy array of zeroes of size (128, T) 

        Args:
            file: Midifile containing all tracks to use.
            tempo: Integer representing default tempo time for a midi file in microseconds/beat.
            values can be 500,000 or 1000,000
            fs: Integer representing discretize frequency sample time for evets, default = 10
        
        Returns:
            np_piano: np.ndarray of size (128, T) representation
            of the midi file

        Example:
            midi_np_processor = MidiToNumpy(file = midi_file,
                                default_tempo = 500000, fs = 10)
            np_midi = midi_np_processor.get_np_array()
    '''

    def __init__(self, file:MidiFile, default_tempo:int = 500000, fs:int = 10) -> None:
        self.file = file
        self.ticks_per_beat = file.ticks_per_beat
        self.tempo = default_tempo
        self.fs = fs

    def _calculate_seconds(self, ticks:int) -> Union[float, int]:
        return (ticks / self.ticks_per_beat) * (self.tempo / 1_000_000)

    def _get_np_array_info(self) -> Tuple[float, float, int, int]:
        # List to hold note start and end info
        notes = []

        for track in self.file.tracks:
            time_ticks = 0
            ongoing_notes = {}
            for msg in track:
                time_ticks += msg.time
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo
                elif msg.type == 'note_on' and msg.velocity > 0:
                    # Start note
                    ongoing_notes[msg.note] = (time_ticks, msg.note, msg.velocity)
                elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                    # End note
                    if msg.note in ongoing_notes:
                        start_time_ticks, note, note_velocity = ongoing_notes.pop(msg.note)
                        
                        #Convert tick times to seconds
                        start_time = self._calculate_seconds(ticks=start_time_ticks)
                        time = self._calculate_seconds(ticks=time_ticks)
                        notes.append((start_time, time, note, note_velocity))
        return notes

    def get_np_array(self) -> Tuple[np.ndarray[int, float], str]:
        notes_info = self._get_np_array_info()

        #Let's get end time to create he np.ndarray
        _ , final_time , _ , _ = notes_info[-1]
        np_array = np.zeros(shape = (128, int(np.floor(final_time)*self.fs)), dtype=np.float32)

        for start_time, time, note, note_velocity in tqdm(notes_info, desc=f"Creating Piano roll: {self.file.filename.stem}", total=len(notes_info)):
            start_time_clipped = int(np.round(start_time*self.fs))
            time_clipped = int(np.round(time*self.fs))
            np_array[note, start_time_clipped:time_clipped] = note_velocity

        return np_array, self.file.filename.stem

def obtain_piano_rolls(midiobject: List[Tuple[str, MidiFile]]) -> Tuple [List[np.ndarray], List[str], List[str]]:
    '''
    Args:
        midiobject: list containing tuples of song names and related MidiFile
    
    Returns:
        list_np_arrays: list of np_arrays for each of the piano rolls.
        list_composer_names: list containing composer names.
        list_file_names: List containing song names.
    
    Example:
        list_np_arrays, list_composer_names = obtain_piano_rolls(midiobject = midiobj)
    '''

    list_np_arrays = []
    list_comp_names = []
    list_song_names = []
    for name , midifile in midiobject:
        # With customized class
        midi_np_processor = MidiToNumpy(file = midifile,
                            default_tempo = 500000, fs = 10)
        np_array, file_name = midi_np_processor.get_np_array()
        list_song_names.append(file_name)
        list_np_arrays.append(np_array)
        list_comp_names.append(name)

    return list_np_arrays, list_comp_names, list_song_names

class PianoRollsDiscreteEqualizer:
    '''
    Class that woild take a list of np.ndarrays of size
    (128, T). Where T is a varying number of discrete samples
    per piano roll.

    Args:
        - piano_rolls: List of np.ndarrays of size (128, T), with varying Ts
        - threshold: Integer of samples to equalize across all piano arrays.
    
    Returns:
        - equalized_piano_rolls: np.ndarray of shape (N, 128, Teq)
    
    Example:
        equalizer = PianoRollsDiscreteEqualizer(piano_rolls = previous_pianos)
        eq_piano_rolls = equalizer.get_equalized()
    '''

    def __init__(self,
        piano_rolls: List[np.ndarray],
        threshold: int = 2515) -> None:

        self.piano_rolls = piano_rolls
        self.piano_diff_lengths = []
        self.threshold = threshold
    
    def get_equalized(self) -> np.ndarray[int]:
        equalized_np_arrays = []
        for nparray in tqdm(self.piano_rolls, desc="Equalizing piano rolls...", total=len(self.piano_rolls)):
            if len(nparray) >= self.threshold:
                equalized_np_arrays.append(nparray[:, :self.threshold])
            else:
                tiled = nparray
                while tiled.shape[1] < self.threshold:
                    repeats = int((self.threshold // tiled.shape[1]) + 1)
                    tiled = np.tile(tiled, repeats)  # Repeat along time axis
                equalized_np_arrays.append(tiled[:, :self.threshold])

        return np.array(equalized_np_arrays, dtype=np.int64)
