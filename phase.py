#!/usr/bin/env python

import sox


TMP_FOLDER = 'tmp/'
ORIGINAL_SAMPLE = 'master_sample.wav'
SAMPLE_FULL_DURATION = sox.file_info.duration(ORIGINAL_SAMPLE)
PHRASE_DURATION = 4.207
START_PAD_DURATION = 0.910
END_PAD_DURATION = 0.116


def make_track(output_filename, gap, repeat_count, has_initial_rest=False):
    rest_duration = SAMPLE_FULL_DURATION + gap - START_PAD_DURATION - END_PAD_DURATION
    tfm = sox.Transformer()
    tfm.pad(end_duration=rest_duration)
    if repeat_count > 0:
        tfm.repeat(count=repeat_count)
    if has_initial_rest:
        tfm.pad(start_duration=rest_duration + ((SAMPLE_FULL_DURATION - rest_duration) / 2.0))
    tfm.build(ORIGINAL_SAMPLE, output_filename)


def checker_track(output_filename, gap=1.0, repeat_count=5):
    """Repeat the sample on alternating tracks so the fade in and out can overlap"""
    track_a_file = TMP_FOLDER + 'track-a.wav'
    track_b_file = TMP_FOLDER + 'track-b.wav'

    half, remainder = divmod(repeat_count, 2)
    track_a_repeat_count = half + remainder - 1
    track_b_repeat_count = half - 1
    make_track(track_a_file, gap, track_a_repeat_count)
    make_track(track_b_file, gap, track_b_repeat_count, has_initial_rest=True)

    cbn = sox.Combiner()
    # cbn.silence(location=1)
    # cbn.silence(location=-1)
    cbn.build([track_a_file, track_b_file], output_filename, 'mix-power')


def phase():
    track_filenames = []
    for i in range(1, 15):
        track_filename = TMP_FOLDER + 'track-{}.wav'.format(i)
        track_filenames.append(track_filename)
        checker_track(track_filename, gap=.01 * i, repeat_count=300)

    cbn = sox.Combiner()
    cbn.build(track_filenames, 'output.wav', 'mix-power')


# def simple_phase(n_tracks=10):
#     n_tracks = int(n_tracks)

#     track_filenames = []
#     trim_amount = 0.830
#     trim_change = (trim_amount - .02) / n_tracks
#     for i in range(n_tracks):
#         tfm = sox.Transformer()
#         tfm.trim(trim_amount, SAMPLE_FULL_DURATION)
#         tfm.fade(fade_in_len=0.01)
#         trimmed_file = TMP_FOLDER + 'trimmed-{}.wav'.format(i)
#         tfm.build(ORIGINAL_SAMPLE, trimmed_file)

#         cbn = sox.Combiner()
#         track_filename = TMP_FOLDER + 'output-{}.wav'.format(i)
#         track_filenames.append(track_filename)
#         cbn.build([trimmed_file] * n_tracks, track_filename, 'concatenate')

#         trim_amount -= trim_change

#     cbn = sox.Combiner()
#     cbn.build(track_filenames, 'output.wav', 'mix-power')


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-n',
    #     '--n-tracks',
    #     help='how many tracks to generate')
    # args = parser.parse_args()

    # simple_phase(args.n_tracks)
    phase()
