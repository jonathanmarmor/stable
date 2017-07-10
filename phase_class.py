#!/usr/bin/env python

import sox


class Sample(object):
    def __init__(self, file_path):
        self.file_name = file_name
        self.full_duration = sox.file_info.duration(file_name)
        self.phrase_duration = 4.207
        self.start_pad_duration = 0.910
        self.end_pad_duration = 0.116


class Phase(object):
    def __init__(self, sample_file_name, output_file_name, gap=0.5, repeat_count=5):
        self.sample = Sample(sample_file_name)
        self.output_file_name = output_file_name
        self.gap = gap
        self.repeat_count = repeat_count
        self.temp_folder = 'tmp/'

    def make_track(self, output_file_name, gap, repeat_count, has_initial_rest=False, mute_first=False):
        rest_duration = self.sample.full_duration + gap - self.sample.start_pad_duration - self.sample.end_pad_duration

        # if mute_first:
        #     repeat_count -= 1

        tfm = sox.Transformer()
        tfm.pad(end_duration=rest_duration)
        if repeat_count > 0:
            tfm.repeat(count=repeat_count)
        # if mute_first:
            # TODO





        if has_initial_rest:
            tfm.pad(start_duration=rest_duration + ((self.sample.full_duration - rest_duration) / 2.0))
        tfm.build(sample.file_name, output_file_name)

    def checker_track(self, output_file_name, gap=1.0, repeat_count=5, mute_first=False):
        """Repeat the sample on alternating tracks so the fade in and out can overlap"""
        track_a_file = self.temp_folder + 'track-a.wav'
        track_b_file = self.temp_folder + 'track-b.wav'

        half, remainder = divmod(repeat_count, 2)
        track_a_repeat_count = half + remainder - 1
        track_b_repeat_count = half - 1
        self.make_track(track_a_file, gap, track_a_repeat_count, mute_first=mute_first)
        self.make_track(track_b_file, gap, track_b_repeat_count, has_initial_rest=True)

        cbn = sox.Combiner()
        # cbn.silence(location=1)
        # cbn.silence(location=-1)
        cbn.build([track_a_file, track_b_file], output_file_name, 'mix-power')

    def go(self):
        track_file_names = []
        for i in range(1, 4):
            track_file_name = self.temp_folder + 'track-{}.wav'.format(i)
            track_file_names.append(track_file_name)
            mute_first = False
            if i == 1:
                mute_first = True
            self.checker_track(track_file_name, gap=self.gap * i, repeat_count=self.repeat_count, mute_first=mute_first)

        cbn = sox.Combiner()
        cbn.build(track_file_names, self.output_file_name, 'mix-power')


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-n',
    #     '--n-tracks',
    #     help='how many tracks to generate')
    # args = parser.parse_args()

    # simple_phase(args.n_tracks)
    sample_file_name = 'master_sample.wav'
    output_file_name = 'output.wav'
    gap = 0.5
    repeat_count = 5
    Phase(sample_file_name, output_file_name, gap, repeat_count)
