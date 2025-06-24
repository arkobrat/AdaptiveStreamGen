import os
import subprocess
import json

class VideoEncoder:
    def __init__(self, config_path: str = 'ffmpeg_config.json'):
        self.config = self.__load_config__(os.path.abspath(os.path.join(os.path.dirname(__file__), config_path)))
        self.codec =  self.config.get('codec', 'libx264')
        self.preset = self.config.get('preset', 'medium')
        self.options = self.config.get('options', [])

    def __load_config__(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        
        except FileNotFoundError:
            print(f'{config_path} not found. Using default configuration.')
            return {}

    def encode(self, input_path: str, output_path: str, crf: int) -> None:
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-c:v', self.codec, 
            '-crf', str(crf),
            '-preset', self.preset,
            '-an',
            output_path,
        ]

        if self.options:
            cmd += self.options

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
