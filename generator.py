from random import randint

from midiutil import MIDIFile

from constants import notes, octave, gammes

partition_size = 20
croche_max_proportion = 0.8
tempo = 200  # In BPM
# instrument = 15 clavecin 14 xylo 75 flute de pan
instrument = 101
tonalite = "do_majeur"

"""
The best:
- instument: 75 (flute de pan),
- size: 20
- tonalite: la_mineur
- tempo: 80
"""


def create_partition(allowed_notes, intervals):
    """

    :param allowed_notes: list of notes as defined in constants.py
    :param intervals: list of integer intervals (number of notes to jump in allowed_notes)
    :param rythm: list of values either 0.5 (blanche), 1 (noire) or 2 (croche) of length partition_size
    :return:
    """
    partition = [allowed_notes[0]]
    last_note_index = 0
    # first note and last 2 already defined
    for interval in intervals:
        last_note_index = (last_note_index + interval) % len(allowed_notes)
        partition.append(allowed_notes[last_note_index])

    partition.append(allowed_notes[4])

    # hidden gem in memory of Eve Pachoud: une fontaine

    return partition


def write_midi_file(partition, rythm):
    # MIDI note number
    track = 0
    channel = 0
    time = 0  # In beats
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track automatically created)
    MyMIDI.addProgramChange(track, channel, time, instrument)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(partition):
        MyMIDI.addNote(track, channel, pitch, time, rythm[i], volume)
        time = time + rythm[i]

    with open("major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def generate_intervals():
    intervals = []
    large_interval_threshold = 2
    consecutive_large_intervals = 0
    for _ in range(partition_size - 3):
        interval = randint(0, len(allowed_notes) - 1)
        if interval > large_interval_threshold:
            consecutive_large_intervals += 1
        if consecutive_large_intervals > 1:
            consecutive_large_intervals = 0
            interval = randint(0, min(len(allowed_notes) - 1, large_interval_threshold))
        intervals.append(interval)

    return intervals


def generate_rythm():
    rythms = []
    croche_max = int(croche_max_proportion * partition_size)
    croche = 0
    possible_rythm = [0.5, 1, 2]
    for _ in range(partition_size):
        if croche % 2 == 1:
            index = 2
            croche += 1

        elif croche >= croche_max:
            index = randint(0, 1)

        else:
            index = randint(0, 2)
            if (index == 2): croche += 1

        rythms.append(possible_rythm[index])

    return rythms


allowed_notes = gammes[tonalite]
intervals = generate_intervals()
partition = create_partition(allowed_notes, intervals)
rythm = generate_rythm()
write_midi_file(partition, rythm)
