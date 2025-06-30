import os
import sys

from encoder.VideoEncoder import VideoEncoder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AdaptiveStreamer:
    def __init__(self, input_path: str, output_path: str, num_streams: int, init_crf: int, encoder: VideoEncoder = VideoEncoder()) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.num_streams = num_streams
        self.init_crf = init_crf
        self.encoder = encoder
        
    def stream(self) -> None:
        root, ext = os.path.splitext(self.output_path)
        crf = self.init_crf
        scale_factor = 1.0
        step = 0.5

        for i in range(1, self.num_streams):
            scale_factor += step
            crf -= 1/step
            print(crf, scale_factor)
            output_stream_path = f'{root}_stream_{i}{ext}'
            self.encoder.encode_at_scaled_resolution(self.input_path, output_stream_path, crf=crf, scale_factor=scale_factor)
