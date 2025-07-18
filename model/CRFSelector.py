import sys
import os

from vmaf.VMAFCalculator import VMAFCalculator
from encoder.VideoEncoder import VideoEncoder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CRFSelector:
    def __init__(self, encoder: VideoEncoder = VideoEncoder(), vmaf_calculator: VMAFCalculator = VMAFCalculator()) -> None:
        self.encoder = VideoEncoder()
        self.vmaf_calculator = VMAFCalculator()

    def cleanup(self, temp_files: list, best_crf: int, output_path: str) -> None:
        root, ext = os.path.splitext(output_path)
        
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                if temp_file == f'{root}_temp_{best_crf}{ext}':
                    os.rename(temp_file, output_path)
                else:
                    os.remove(temp_file)

    def find_crf_linear(self, input_path: str, output_path: str, min_crf: int, max_crf: int, vmaf_target: float) -> int:
        root, ext = os.path.splitext(output_path)
        crf_range = range(max_crf, min_crf, -1)
        temp_files = []

        for crf in crf_range:
            print(crf)

            temp_output_path = f'{root}_temp_{crf}{ext}'
            self.encoder.encode(input_path, temp_output_path, crf)
            temp_files.append(temp_output_path)

            vmaf = self.vmaf_calculator.calculate_vmaf(input_path, temp_output_path)

            print(vmaf)

            if vmaf >= vmaf_target:
                self.cleanup(temp_files, crf, output_path)
                return crf
            
        crf = crf_range[-1]
        self.cleanup(temp_files, crf, output_path)
        return crf
    
    def find_crf_binary(self, input_path: str, output_path: str, min_crf: int, max_crf: int, vmaf_target: float) -> int:
        root, ext = os.path.splitext(output_path)
        best_crf = max_crf
        temp_files = []

        while min_crf <= max_crf:
            mid_crf = (min_crf + max_crf) // 2
            print(mid_crf)

            temp_output_path = f'{root}_temp_{mid_crf}{ext}'
            self.encoder.encode(input_path, temp_output_path, mid_crf)
            temp_files.append(temp_output_path)

            vmaf = self.vmaf_calculator.calculate_vmaf(input_path, temp_output_path)
            print(vmaf)

            if vmaf >= vmaf_target:
                best_crf = mid_crf
                min_crf = mid_crf + 1

            else:
                max_crf = mid_crf - 1

        self.cleanup(temp_files, best_crf, output_path)

        return best_crf
