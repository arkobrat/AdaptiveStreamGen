import os
import sys

from encoder.VideoEncoder import VideoEncoder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AdaptiveStreamer:
    def __init__(self, input_path: str, output_path: str, init_crf: int, encoder: VideoEncoder = VideoEncoder()) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.init_crf = init_crf
        self.encoder = encoder
        
    def create_stream(self, min_width=854, min_height=480) -> None:
        root, ext = os.path.splitext(self.output_path)
        crf = self.init_crf
        scale_factor = 1.0
        step = 0.5
        stream_idx = 1

        width, height = self.encoder.get_resolution(self.input_path)

        while True:
            scale_factor += step
            crf -= 1/step
            print(crf, scale_factor)

            scaled_width = int(width / scale_factor)
            scaled_height = int(height / scale_factor)

            print(f'Scaled resolution: {scaled_width}x{scaled_height}')

            if scaled_width < min_width and scaled_height < min_height:
                break

            output_stream_path = f'{root}_stream_{stream_idx}{ext}'
            self.encoder.encode_at_scaled_resolution(self.input_path, output_stream_path, crf=crf, scale_factor=scale_factor)
            
            stream_idx += 1
