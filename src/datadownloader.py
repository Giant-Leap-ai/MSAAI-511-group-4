from typing import List, Tuple
from pathlib import Path
import shutil

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

        # Explicit, ordered list — not a set
        self.composers = ["Bach", "Beethoven", "Chopin", "Mozart"]

        # Map composer → destination Path
        self.dest_dirs = {
            c: (data_path / "final_proj_data" / c)
            for c in self.composers
        }
        for p in self.dest_dirs.values():
            p.mkdir(parents=True, exist_ok=True)

    def subdivide_data(self) -> Path:
        # Walk once and route every .mid by *name*, not by index
        for root, dirs, files in self.dataset_path.walk():
            composer = Path(root).name       # deepest directory’s name
            if composer not in self.dest_dirs:
                continue

            for f in files:
                if f.endswith(".mid"):
                    src = Path(root) / f
                    dst = self.dest_dirs[composer] / f

                    # If a file with the same name exists, append a suffix
                    if dst.exists():
                        dst = dst.with_stem(dst.stem + "_" + src.parent.name)

                    shutil.copy2(src, dst)   # copy to keep original intact
        return self.data_path / "final_proj_data"
