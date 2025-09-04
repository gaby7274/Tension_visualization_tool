#!/usr/bin/env python2
#
#  ScoreParserClass.py
#
#  Class to create Musical Score objects which contain data and methods for interacting with score data.
#
#  Copyright 2018-2022 by Dr. Randall E. Cone - All rights reserved.
#


from pprint import pprint
from tabnanny import verbose

import xml.etree.cElementTree as etree
from HarmonyClass.HarmonyClass import HarmonyClass

from NoteClass.NoteClass import NoteClass


class ScoreParserClass():

    def __init__(self, filename=None, parse_harmony_parts=True, calculate_harmony=True, verbose=0):

        # Initial_key:
        self.initial_key = None

        # Note palette (respective of the key):
        self.note_palette = None
        

        #whether or not to parse harmony parts
        self.parse_harmony_parts = parse_harmony_parts
        #wheather or not calculate harmony
        self.calculate_harmony = calculate_harmony

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
        # formulas for the scale, so WWHWWWH, WHWWHWW and so forth
        self.formulas_for_scales = {
            "major": [2, 2, 1, 2, 2, 2, 1],
            "natural_minor": [2, 1, 2, 2, 1, 2, 2],
            "harmonic_minor": [2, 1, 2, 2, 1, 3, 1],
            "melodic_minor": [2, 1, 2, 2, 1, 1, 1, 1, 1]
        }

        # posible scales the score follows
        self.possible_scales = {
            "major": [],
            "natural_minor": [],
            "harmonic_minor": [],
            "melodic_minor": []
        }
        # at measure, which scales can the song be
        self.possible_scales_at_measure = {}

        # creating a dict that is going to be distributed as such, where n is the duration of measure
        '''{
            part-1
                measure-1
                measure-2
                measure-3
                    0 noteObject-prototype
                    1 noteObject
                    2
                    3
                    ...
                    n
            part-2
            part-3


        }'''

        # self harmony class

        self.harmony_class = None

        self.harmony_class_array = []

        if(filename == None):
            return



        # TEMPORARY dict, measures_where_harmony_changed

        self.MWHC = {}

        #

        # Complete score in vertical
        self.CSIV = {}
        # Create a data/method Object for this score:
        self.score_object = self.parse_musicxml_file(filename, verbose=verbose)
        if(verbose >= 1):
            pprint("This is the part object: ")
            pprint(self.parts)
        #self.harmony_class.setPartCollection(self.parts, verbose=verbose)

    # Parser for music_xml_file:

    def parse_musicxml_file(self, filename, verbose):

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
                    'is_empty': True,

                    # add key_changes attribute, for harmonies
                    "key_change": [],
                    "time_change": []
                }

                self.CSIV[sp.attrib['id']] = {}
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

                            # GASP Set up initial key, as well as dictionary of any explicit key changes:

                            # With the scale, and the list to simulate piano,
                            # put it in the parts key_change

                            self.calculate_scale(fifths.text, verbose)
                            self.harmony_piano = self.createHarmonyPiano(
                                verbose)
                            if(verbose >= 1):
                                pprint(self.harmony_piano)

                            self.possible_scales_at_measure[measure_number] = self.possible_scales

                            # to set the ending measure if there are any change other than the first
                            index = len(self.parts[partidx]["key_change"]) - 1

                            if(index >= 0):
                                self.parts[partidx]["key_change"][index]['ending_measure'] = measure_number
                            self.parts[partidx]["key_change"].append({
                                "possible_scales": self.possible_scales,
                                "starting_measure": measure_number-1,
                                "key": self.initial_key,
                                "harmony_piano": self.harmony_piano,
                                "ending_measure": None
                            })

                            if(verbose >= 1):
                                print(
                                    "These are the possible scales at measure #%d" % measure_number)
                                pprint(self.possible_scales)
                                pprint(self.possible_scales_at_measure)

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
                        # set the time changes NOTE: its repetition of data but one that Gabriel (me)
                        # understands better

                        index = len(self.parts[partidx]["time_change"])-1
                        if(index >= 0):
                            self.parts[partidx]["time_change"][index]["ending_measure"] = measure_number
                        self.parts[partidx]['time_change'].append({
                            "starting_measure": measure_number-1,
                            "numbeats": numbeats,
                            "beattype": beattype,
                            "num_divs": numdivs,
                            "ending_measure": None
                        })
                    # Create harmony piano, basically a piano with one octave

                    start_index = 0
                    # if harmony_class was already defined, this means that measure is not the initial
                    # and we should calculate harmony in the current state
                    # Then, the start index will be the next note index in each part
                    # if(self.harmony_class != None):

                    # to check measures from starting index to measure_number-1

                    # if at measure 9 there is a key change, starting measure is 0, ending measure is 8
                    # and then it will search from measure 0 to 7 making 8 total measures
                    # self.harmony_class.setPartCollection(
                    #    self.parts, verbose=verbose, ending_measure=measure_number-1)
                    # self.harmony_class_array.append(self.harmony_class)
                    #start_index = {}
                    # for partind in self.parts:
                    #    start_index[partind] = {
                    #        'start_idx': len(self.parts[partind]['notes']),
                    #        'starting_measure': measure_number - 1
                    #    }

                    # self.harmony_class = HarmonyClass(
                    #    self.possible_scales, self.harmony_piano, start_index, numdivs)
                    # if(verbose >= 1):
                    #    pprint("These are the possible Triads: ")

                    #    pprint(self.harmony_class.triads)
                    #    pprint("These are the possible diatonic chords")
                    #    pprint(self.harmony_class.constructed_chords)
                    #    pprint(
                    #        "These are the triads/chords per each note")
                    #    pprint(self.harmony_class.note_with_triads)
                    #    pprint(self.harmony_class.note_with_chords)
                    #self.MWHC[measure_number] = self.harmony_class

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
        if(self.calculate_harmony==True):
            self.harmony_class = HarmonyClass(self.parts, calculate_harmony_algorithm=self.calculate_harmony,verbose=verbose)

        return note_collection, self.parts

    def calculate_scale(self, fifths, verbose):
        # if the song is in flats, use FKNN
        fifths = int(fifths)
        if fifths < 0:
            keys = list(self.FKNN.keys())
        # the song is in sharps
        else:
            keys = list(self.SKNN.keys())

        # remove A0, B0 and Bb0/A#0 so the keys can really be circular
        keys.pop(0)
        keys.pop(0)
        keys.pop(0)

        # find middle C
        index_of_c4 = keys.index('C4')

        index_of_note = (index_of_c4 + 7 * (fifths)) % len(keys)
        if(verbose >= 1):
            print("index of note: ", index_of_note)
            print("note: ", keys[index_of_note])
            print("KEYS: ", keys)

        # Empty the self.possible_scales
        self.possible_scales = {
            "major": [],
            "natural_minor": [],
            "harmonic_minor": [],
            "melodic_minor": []
        }
        for form in self.formulas_for_scales.keys():

            for i in range(len(self.formulas_for_scales[form])):

                self.possible_scales[form].append(keys[index_of_note])
                index_of_note = (
                    index_of_note + self.formulas_for_scales[form][i]) % len(keys)
            if form == "major":

                # after the first scale, major, the  starting point is going to be the relative minors
                index_of_note -= 3

    # create the double linked list

    def createHarmonyPiano(self, verbose):

        # Pseudo NDLL with dictionary
        # Can be more efficient, but sanity checking

        dictionary_to_send = {
            "major": [],
            "minor": []
        }

        # Get the first note in the scale
        major_note = self.possible_scales["major"][0]
        minor_note = self.possible_scales["natural_minor"][0]

        # if(verbose >= 1):
        #pprint("First scale note: ", major_note)
        #pprint("First minor scale note: ", minor_note)

        ind_of_major_note = self.note_palette.index(major_note[0])
        ind_of_minor_note = self.note_palette.index(minor_note[0])

        for i in range(12):
            dictionary_to_send['major'].append(
                self.note_palette[((ind_of_major_note + i) % len(self.note_palette))])
            dictionary_to_send['minor'].append(
                self.note_palette[((ind_of_minor_note + i) %
                                   len(self.note_palette))]
            )
        return dictionary_to_send
