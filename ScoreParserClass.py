#!/usr/bin/env python2
#
#  ScoreParserClass.py
#
#  Class to create Musical Score objects which contain data and methods for interacting with score data.
#
#  Copyright 2018-2022 by Dr. Randall E. Cone - All rights reserved.
#

import xml.etree.cElementTree as etree

from NoteClass.NoteClass import NoteClass


class ScoreParserClass():

    def __init__(self, filename='default.xml', verbose=2):

        # Initial_key:
        self.initial_key = None

        # Note palette (respective of the key):
        self.note_palette = None

        # Score time signature(s), and what measure they start on:
        #   Note: the keys for this dictionary are the measure numbers
        #              where the time signature begins:
        #         the values for this dictionary are:
        #              positive integers indicating the number of sharps, or
        #              nagative integers indicating the number of flats
        self.time_signatures = {}

        # Score keys, and what measure they start on:
        #   Note: the keys for this dictionary are the measure numbers
        #              where the key begins.
        #         the values for this dictionary are three element (integer) lists, where
        #              the first integer is the number of beats per measure;
        #              the second integer is the type of beat;
        #              the third integer is the number of divisions within a beat (for duration calculations)
        #         e.g. 3/4 time with 8 divisions per beat is [3, 4, 8]
        self.keys = {}

        # Smallest note duration:
        self.smallest_note_duration = 1000000

        # Dictionary of parts/instruments:
        self.parts = {}

        # data tree from musicxml:
        self.tree = None

        # Establish full range of semitones:
        self.flat_notes = ['C', 'Db', 'D', 'Eb', 'E',
                           'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.sharp_notes = ['C', 'C#', 'D', 'D#',
                            'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        self.revnote_idx = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
                            'Cb': 11, 'B#': 0, 'Db': 1, 'C#': 1, 'Eb': 3, 'D#': 3,
                            'Fb': 4, 'E#': 5, 'Gb': 6, 'F#': 6, 'Ab': 8, 'G#': 8,
                            'Bb': 10, 'A#': 10}

        # Flat Key Piano Note Numbers:
        self.FKNN = {'A0': 0, 'Bb0': 1, 'B0': 2}

        # Sharp Key Piano Note Numbers:
        self.SKNN = {'A0': 0, 'A#0': 1, 'B0': 2}

        # Piano number palette:
        self.piano_palette = None

        # Build remaining note numbers:
        count = 3
        for i in range(1, 9):
            for j in range(len(self.flat_notes)):
                self.FKNN[self.flat_notes[j] + str(i)] = count
                self.SKNN[self.sharp_notes[j] + str(i)] = count
                count += 1

        if (verbose == 2):
            print('\nPalette of Flat Notes:')
            print(self.FKNN)
            print('\nPalette of Sharp Notes:')
            print(self.SKNN)
            print('\n')

        # Create a data/method Object for this score:
        self.score_object = self.parse_musicxml_file(filename, verbose=verbose)

    # Parser for music_xml_file:

    def parse_musicxml_file(self, filename, verbose=2):

        print('Verbosity setting: {}'.format(verbose))

        if (verbose >= 1):
            print('\n' + '*'*10 + ' Music file: {} '.format(filename) + '*'*10)

        # Establish etree from musicxml file:
        self.tree = etree.parse(filename)

        note_collection = set()

        # Counter for number of parts:
        numparts = 0

        # Get information about the number and type of score parts:
        for elem in self.tree.iterfind('part-list'):
            for sp in elem.iter('score-part'):
                # Add part to dictionary of parts:
                self.parts[numparts] = {
                    'id': sp.attrib['id'],
                    'number': numparts,
                    'notes': [],
                    'number_of_measures': 0,
                    'measure_durations': [],
                    'is_empty': True
                }
                numparts = numparts + 1

            if (verbose == 2):
                print('Last valid SCOREPART Detected: ' +
                      str(sp.tag) + ' ' + str(sp.attrib['id']))

        # Counter for part number:
        partidx = 0

        # Iterate through (content) of each of this score's PARTS:
        for elem in self.tree.iterfind('part'):

            if (verbose >= 1):
                print('\n' + '-'*30 +
                      ' Beginning of Part {} '.format(partidx) + '-'*30 + '\n')

            # Flag to set as False if (non-rest) notes are found in the current part:
            part_empty_flag = True

            # Reset note counter for this part:
            part_note_counter = 0

            if (verbose == 2):
                print('\nContent of SCOREPART: ' +
                      str(elem.tag) + ' ' + str(elem.attrib['id']))

            # Reset Measure Duration to 0 unless a new one is detected:
            measure_duration = 0

            # MEASURES:
            for measure in elem.iter('measure'):

                if (verbose >= 1):
                    print('MEASURE ' +
                          str(measure.attrib['number']) + ' BEGINS')

                # New measure:
                measure_number = int(measure.attrib['number'])

                # Reset note counter for this measure:
                measure_note_counter = 0

                # Detect key and time signature, and any changes thereof:
                for attr in measure.iter('attributes'):
                    for key in attr.iter('key'):
                        for fifths in key.iter('fifths'):
                            if (verbose >= 1):
                                print('KEY CHANGE: ' + str(fifths.tag) +
                                      ' ' + str(fifths.text))

                            # Set up initial key, as well as dictionary of any explicit key changes:
                            self.initial_key = int(fifths.text)
                            self.keys[measure_number] = int(fifths.text)

                            # Set up note palette for this key:
                            if (self.keys[measure_number] >= 0):  # sharps
                                self.note_palette = self.sharp_notes
                                self.piano_palette = self.SKNN
                                if (verbose == 2):
                                    print('  KEY in Sharps')
                            else:
                                self.note_palette = self.flat_notes
                                self.piano_palette = self.FKNN
                                if (verbose == 2):
                                    print('  KEY in Flats')

                    time_change_flag = False

                    for divs in attr.iter('divisions'):
                        numdivs = int(divs.text)
                        time_change_flag = True

                    for tsym in attr.iter('time'):
                        for beats in tsym.iter('beats'):
                            numbeats = int(beats.text)
                        for bt in tsym.iter('beat-type'):
                            beattype = int(bt.text)
                        time_change_flag = True

                    if time_change_flag:
                        measure_duration = numdivs * numbeats
                        self.time_signatures[measure_number] = [
                            numbeats, beattype, numdivs]

                # Traverse Notes and Backup (False) Notes (really, all elements in this measure):
                for n in measure.iter('*'):
                    # if (verbose >= 1):
                    #    print('\tPrimary Tag: {}'.format(n.tag))

                    # Work only on regular notes and "backup"/"forward" notes:
                    if ((n.tag == 'note') or (n.tag == 'backup') or (n.tag == 'forward')):

                        # Identify note:
                        if (verbose >= 1):
                            print('\n\tNew note: {}'.format(n.tag))

                        # Initialize Note object:
                        new_note = NoteClass()
                        new_note.measure_number = int(measure_number)

                        # Handle Backups and Forwards separately:
                        if (n.tag == 'backup'):
                            new_note.backup = True
                            if (verbose >= 1):
                                print('\t\tNew Backup Note: {}'.format(n.tag)
                                      + ' part#: {}'.format(partidx) + ' measure#: {}'.format(measure_number))

                            # Retrieve backup (false) note duration:
                            for note_dur in n.iter('duration'):
                                if (verbose >= 1):
                                    print('\t\tBackup Note Duration: {}'.format(note_dur.tag)
                                          + ' {}'.format(note_dur.text))
                                new_note.duration = int(note_dur.text)

                        elif (n.tag == 'forward'):
                            new_note.forward = True
                            if (verbose >= 1):
                                print('\t\tNew Note: {}'.format(n.tag)
                                      + ' part#: {}'.format(partidx) + ' measure#: {}'.format(measure_number))

                            # Retrieve forward (false) note duration:
                            for note_dur in n.iter('duration'):
                                if (verbose >= 1):
                                    print('\t\tForward Note Duration: {}'.format(note_dur.tag)
                                          + ' {}'.format(note_dur.text))
                                new_note.duration = int(note_dur.text)

                        # This can only be a standard note or a rest:
                        else:
                            # Is this note really a rest?
                            for rest in n.iter('rest'):
                                if (verbose >= 1):
                                    print('\t\tNew rest: {}'.format(rest.tag))
                                new_note.rest = True

                            # Is this note a grace note?
                            for grace in n.iter('grace'):
                                if (verbose >= 1):
                                    print(
                                        '\t\tGrace Note: {}\n'.format(grace.tag))
                                new_note.grace = True

                                # TEMPORARY:
                                new_note.duration = 0

                            # Retrieve note length type:
                            for note_len in n.iter('type'):
                                if (verbose >= 1):
                                    print('\t\t' + str(note_len.tag) +
                                          ' ' + str(note_len.text))
                                new_note.type = note_len.text

                            # Retrieve note duration:
                            for note_dur in n.iter('duration'):
                                if (verbose >= 1):
                                    print('\t\t' + str(note_dur.tag) +
                                          ' ' + str(note_dur.text))
                                new_note.duration = int(note_dur.text)

                            # Check and record if this is the new smallest note duration:
                            if new_note.duration < self.smallest_note_duration:
                                # Only do this if the note length is non-zero:
                                if new_note.duration > 0:
                                    self.smallest_note_duration = new_note.duration

                            # Retrieve note accidentals:
                            for note_acc in n.iter('accidental'):
                                new_note.accidental = note_acc.text
                                if (verbose >= 1):
                                    print('\t\t' + str(note_acc.tag) +
                                          ' ' + str(note_acc.text))

                            # Retrieve note voice within part:
                            for note_voice in n.iter('voice'):
                                if (verbose >= 1):
                                    print('\t\t' + str(note_voice.tag) +
                                          ' ' + str(note_voice.text))
                                new_note.voice = int(note_voice.text)

                            # Retrieve tie information:
                            for note_tie in n.iter('tie'):
                                if note_tie.attrib['type'] == 'start':
                                    new_note.tiestart = True
                                elif note_tie.attrib['type'] == 'stop':
                                    new_note.tiestop = True
                                if (verbose >= 1):
                                    print('\t\t' + str(note_tie.tag) +
                                          ' ' + str(note_tie.attrib['type']))

                            # Keep track of note order in measure for this voice:
                            new_note.order_in_measure = measure_note_counter
                            new_note.order_in_part = part_note_counter

                            if (verbose >= 1):
                                print('\t\torder in measure: ' +
                                      str(new_note.order_in_measure))
                                print('\t\torder in part: ' +
                                      str(new_note.order_in_part))

                            for p in n.iter('pitch'):

                                # We have detected a pitch for a proper note, so this part is not empty:
                                part_empty_flag = False

                                if (verbose >= 1):
                                    print('\t\tPitch Detected: {}'.format(p.tag))

                                # Establish pitch class
                                for s in p.iter('step'):
                                    if (verbose >= 1):
                                        print('\t\t' + str(s.tag) +
                                              ' ' + str(s.text))
                                    new_note.pitch_class = s.text

                                # Establish octave:
                                for o in p.iter('octave'):
                                    if (verbose >= 1):
                                        print('\t\t' + str(o.tag) +
                                              ' ' + str(o.text))
                                    new_note.octave = int(o.text)

                                # Establish alteration (accidental in numerical form):
                                for a in p.iter('alter'):
                                    if (verbose >= 1):
                                        print('\t\t' + str(a.tag) +
                                              ' ' + str(a.text))
                                    new_note.alteration = int(a.text)

                                    # Alteration was present, so we alter pitch class:
                                    oldnote = new_note.pitch_class
                                    newnum = (
                                        self.revnote_idx[oldnote] + new_note.alteration) % 12

                                    # Fix octave, if necessary:
                                    # Drop octave:
                                    if (self.revnote_idx[oldnote] + new_note.alteration < 0):
                                        new_note.octave = new_note.octave - 1
                                    # Move octave up:
                                    elif (self.revnote_idx[oldnote] + new_note.alteration > 11):
                                        new_note.octave = new_note.octave + 1

                                    if (verbose >= 1):
                                        print('\t\t newnum: ' + str(newnum))

                                    new_note.pitch_class = self.note_palette[newnum]

                                # Determine piano note number and name
                                #  NOTE: the +3 is for A0->Bb0:
                                newnum = self.revnote_idx[new_note.pitch_class]
                                new_note.piano_note_number = (
                                    new_note.octave-1) * 12 + 3 + newnum
                                new_note.piano_note_name = new_note.pitch_class + \
                                    str(new_note.octave)

                                if (verbose >= 1):
                                    print('\t\tConverted pitch class: ' +
                                          str(new_note.pitch_class))
                                    print('\t\tPiano note name: ' +
                                          new_note.piano_note_name)
                                    print('\t\tCalculated piano #: ' +
                                          str(new_note.piano_note_number))
                                    print('\t\tLookup piano #: {}'.format(
                                        self.piano_palette[new_note.piano_note_name]))

                        note_collection.add(new_note)
                        self.parts[partidx]['notes'].append(new_note)

                        measure_note_counter += 1
                        part_note_counter += 1
                # END EXTERIOR OF NOTE LOOP

                # Record the duration of the measure just analyzsed:
                self.parts[partidx]['measure_durations'].append(
                    measure_duration)
                if (verbose >= 1):
                    print('MEASURE ' + str(measure_number) +
                          ' ENDS, Duration: ' + str(measure_duration) + '\n')

            # END EXTERIOR OF MEASURE LOOP
            if (verbose >= 1):
                print('Final count on number of measures in part: ' +
                      str(measure_number))
                print('Final count on number of notes in part: ' +
                      str(part_note_counter))

            # Record total number of measures in part:
            self.parts[partidx]['number_of_measures'] = measure_number

            # Check flag to see if part was only rests (empty):
            if (part_empty_flag == True):
                self.parts[partidx]['is_empty'] = True

                if (verbose >= 1):
                    print('This Part is empty: ' +
                          str(self.parts[partidx]['is_empty']))

            else:  # Part not empty
                self.parts[partidx]['is_empty'] = False

                if (verbose >= 1):
                    print('This Part is empty: ' +
                          str(self.parts[partidx]['is_empty']))

            partidx = partidx + 1

        # END EXTERIOR OF PART LOOP

        return note_collection
