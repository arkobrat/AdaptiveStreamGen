from ffmpeg_quality_metrics import FfmpegQualityMetrics
import numpy as np

class VMAFCalculator:
    def calculate_vmaf(self, reference_path, distorted_path):
        ffqm = FfmpegQualityMetrics(
            reference_path,
            distorted_path,
        )

        metrics = ffqm.calculate(metrics=['vmaf'])

        vmaf_dict = metrics['vmaf']        
        vmaf_values = [frame['vmaf'] for frame in vmaf_dict]
        vmaf_score = np.mean(vmaf_values)

        return vmaf_score
