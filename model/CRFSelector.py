import sys
import os

from vmaf.VMAFCalculator import VMAFCalculator
from encoder.VideoEncoder import VideoEncoder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CRFSelector:
    def __init__(self):
        self.encoder = VideoEncoder()
        self.vmaf_calculator = VMAFCalculator()

    def find_best_crf_linear(self, input_path: str, output_path: str, min_crf: int, max_crf: int, vmaf_target: float) -> int:
        root, ext = os.path.splitext(output_path)
        
        crf_range = range(max_crf, min_crf, -1)

        for crf in crf_range:
            print(crf)

            temp_output_path = f'{root}_temp_{crf}{ext}'
            self.encoder.encode(input_path, temp_output_path, crf)

            vmaf = self.vmaf_calculator.calculate_vmaf(input_path, temp_output_path)

            print(vmaf)

            if vmaf >= vmaf_target:
                return crf
            
        return crf_range[-1]
    
    def find_best_crf_binary(self, input_path: str, output_path: str, min_crf: int, max_crf: int, vmaf_target: float) -> int:
        root, ext = os.path.splitext(output_path)

        best_crf = max_crf

        while min_crf <= max_crf:
            mid_crf = (min_crf + max_crf) // 2
            print(mid_crf)

            temp_output_path = f'{root}_temp_{mid_crf}{ext}'
            self.encoder.encode(input_path, temp_output_path, mid_crf)

            vmaf = self.vmaf_calculator.calculate_vmaf(input_path, temp_output_path)

            print(vmaf)

            if vmaf >= vmaf_target:
                best_crf = mid_crf
                min_crf = mid_crf + 1

            else:
                max_crf = mid_crf - 1

        return best_crf
