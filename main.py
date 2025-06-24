import sys
import os

from encoder.VideoEncoder import VideoEncoder
from vmaf.VMAFCalculator import VMAFCalculator

def find_best_crf(input_path: str, output_path: str, min_crf: int, max_crf: int, vmaf_target: float) -> int:
    encoder = VideoEncoder()
    vmaf_calculator = VMAFCalculator()

    crf_range = range(max_crf, min_crf, -1)

    root, ext = os.path.splitext(output_path)

    for crf in crf_range:
        print(crf)

        temp_output_path = f'{root}_temp_{crf}{ext}'
        encoder.encode(input_path, temp_output_path, crf)

        vmaf = vmaf_calculator.calculate_vmaf(input_path, temp_output_path)

        print(vmaf)

        if vmaf >= vmaf_target:
            return crf
        
    return crf_range[-1]

if __name__ == '__main__':
    # if len(sys.argv) !=  6:
    #     print("Usage: python3 main.py <input_video> <output_video> <min_crf> <max_crf> <vmaf_target>")
    #     sys.exit(1)

    # input_video = sys.argv[1]
    # output_video = sys.argv[2]
    # min_crf = int(sys.argv[3])
    # max_crf = int(sys.argv[4])
    # vmaf_target = float(sys.argv[5])

    input_video = 'input.mkv'
    output_video = 'output.mkv'
    min_crf = 14
    max_crf = 23
    vmaf_target = 97.0

    best_crf = find_best_crf(input_video, output_video, min_crf, max_crf, vmaf_target)
    print('Best CRF: ', best_crf)
