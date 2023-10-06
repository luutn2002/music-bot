import pandas as pd

class Playlist:
    def __init__(self):
        self.song = pd.DataFrame(columns=['name', 'download_link'])
    
    def add(self, 
            name: str, 
            link: str):
        self.song.loc[len(self.song.index)] = [name, link] 

    def drop_first(self):
        self.song = self.song.iloc[1:]
    
    def get_first(self):
        return self.song.iloc[0]