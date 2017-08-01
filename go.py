#!/usr/bin/env python

from phase import Phase


def main():
    phaser = Phase(
        sample_file_name='master_sample.wav',
        output_file_name='output.wav',
        start_pad_duration=0.910,
        end_pad_duration=0.116)

    track_a_file = phaser.temp_folder + 'arch-track-a.wav'
    track_b_file = phaser.temp_folder + 'arch-track-b.wav'

    phaser.phase(output_file_name=track_a_file, n_tracks=9, gap=0.03, repeat_count=172)
    phaser.phase(output_file_name=track_b_file, n_tracks=12, gap=0.012, repeat_count=20, end_align=True)

    cbn = phaser.sox.Combiner()
    cbn.build([track_a_file, track_b_file], phaser.output_file_name, 'concatenate')


if __name__ == '__main__':
    main()
