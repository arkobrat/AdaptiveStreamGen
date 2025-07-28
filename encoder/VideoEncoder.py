import os
import subprocess
import json

class VideoEncoder:
    def __init__(self, config_path: str = None) -> None:
        if not config_path:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))
        
        self.config = self.__load_config__(config_path)
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
        
    def get_resolution(self, input_path) -> tuple:
        cmd = ['ffprobe', 
               '-v', 
               'error', 
               '-select_streams', 
               'v:0', '-show_entries', 
               'stream=width,height', 
               '-of', 
               'default=noprint_wrappers=1:nokey=1', 
               input_path]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        width, height = map(int, result.stdout.split())
        return width, height

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

    def encode_at_scaled_resolution(self, input_path: str, output_path: str, crf: int, scale_factor: float) -> None:
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', f'scale=iw/{scale_factor}:ih/{scale_factor}',
            '-c:v', self.codec,
            '-crf', str(crf),
            '-preset', self.preset,
            '-an',
            output_path,
        ]

        if self.options:
            cmd += self.options

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
