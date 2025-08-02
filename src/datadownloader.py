from typing import List, Tuple, Union
from pathlib import Path
import os


class DataRetriever:
    '''
    Class that would access a data folder
    containg multiple directories and zip files,
    where we would retrieve the MIDI files from:
        - Bach
        - Beethoven
        - Chopin
        - Mozart
    
    Args:
        data_path: pathlib path to the data folder where the data is contained
    
    Returns:
        retrieved_path: pathlib path where all the midi files of the 4 desired
        composers are.
    
    Example:
        retriever = DataRetriever(data_path = set_path)
        retrieved_path = retriever.subdivide_data()
    '''

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.dataset_path = data_path / "datasets"
        self.dataset_path.walk()
        self.composers = set(["Bach", "Beethoven", "Chopin", "Mozart"])
        self._set_composer_destination_dirs()
    
    def _get_composers_paths(self) -> List[Path]:
        composers_paths = []
        for root, dirs, files in self.dataset_path.walk():
            for dir in dirs:
                if dir in self.composers:
                    composers_paths.append(root / dir)
                continue
        return composers_paths

    def _set_composer_destination_dirs(self) -> None:
        destination_path = self.data_path / "final_proj_data"
        if destination_path.exists():
            print(f"{destination_path}: Already exists")
        else:
            destination_path.mkdir()
        
        self.new_composer_destination_paths = []
        for composer in self.composers:
            new_composer_path = destination_path / composer
            if new_composer_path.exists():
                print(f"{new_composer_path}: Already exists")
            else:
                new_composer_path.mkdir()
            self.new_composer_destination_paths.append(new_composer_path)

    def subdivide_data(self) -> Path:
        composers_paths = self._get_composers_paths()
        for i, composer in enumerate(composers_paths):
            composer_destination_path = self.new_composer_destination_paths[i]
            for root, dirs, files in composer.walk():
                for file in files:
                    if file.endswith(".mid"):
                        full_file_path = Path(root) / file
                        print(f"Found MIDI: {full_file_path}")
                        destination = composer_destination_path / file
                        os.replace(full_file_path, destination)
        return self.data_path / "final_proj_data"