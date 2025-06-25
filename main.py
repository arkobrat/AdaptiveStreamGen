import sys
import os
from model.CRFSelector import CRFSelector

if __name__ == '__main__':
    if len(sys.argv) !=  6:
        print("Usage: python3 main.py <input_video> <output_video> <min_crf> <max_crf> <vmaf_target>")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2]
    min_crf = int(sys.argv[3])
    max_crf = int(sys.argv[4])
    vmaf_target = float(sys.argv[5])

    # input_video = 'video/input.mkv'
    # output_video = 'video/output.mkv'
    # min_crf = 14
    # max_crf = 23
    # vmaf_target = 97.0

    crf_selector = CRFSelector()
    best_crf = crf_selector.find_best_crf_binary(input_video, output_video, min_crf, max_crf, vmaf_target)
    
    print('Best CRF: ', best_crf)
