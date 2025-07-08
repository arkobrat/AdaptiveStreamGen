# AdaptiveStreamGen
A multi-purpose `Python` library to predict optimal video encoding settings (`CRF`) and generate an adaptive stream. 

## Why use AdaptiveStreamGen
`ffmpeg` and the `Bento4` SDK are very powerful tools in themselves and in combination, can be used to create high-quality streaming media.

However, they are not exactly easy to use with video encoding settings, in particular, requiring a lot of tuning to achieve desirable results.

`AdaptiveStreamGen` is a library designed to make it easy for everyone to create standalone streams or full-fledged adaptive streams designed for streaming from a source video.

## Features
* Optimal `CRF` prediction to encode video using `Netflix`'s [VMAF](https://github.com/Netflix/vmaf) for evaluation.
* No pre-tuning needed for video encoding.
* Adaptive streaming implemented by automatically encoding videos to different resolutions based on a scaling factor.
* Easy conversion of unfragmented videos to an `MPEG-DASH` compatible format.
* Customizable encoder, presets and options selection for `ffmpeg`.

## Dependencies
* Requires [Python](https://www.python.org) 3.11+ to be installed
* [ffmpeg](https://ffmpeg.org)
* [Bento4](https://www.bento4.com)

## Usage

Install the requirements listed in `requirements.txt`.

Sample usage of the library is demonstrated in `main.py`.

