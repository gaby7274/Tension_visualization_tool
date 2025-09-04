
from decimal import DivisionUndefined
from faulthandler import disable
from math import floor
from pprint import pprint
import json
from threading import Thread
from time import sleep
from copy import copy

from regex import P
verbose = 1


def parseParts(id, is_empty, measure_durations, number, number_of_measures, notes: list, diction_to_send, num_divs, start_index, ending_measure):

    if(is_empty == True):
        return
    each_measure_list = []

    note_to_be_added = notes.pop(0)
    print("Note is: ", note_to_be_added)
    duration = note_to_be_added.duration

    # this means that start_index will have a different start index for notes, and a specific start index for measure
    if(type(start_index) is dict):
        measure_start = start_index[number]['starting_measure']
    else:
        measure_start = 0

    for measure in range(measure_start, ending_measure):
        counter = 0
        each_measure_list.append([])

        measure_dur = measure_durations[measure]
        # notes to add per division of measures

        notes_to_add = measure_dur/num_divs

        for i in range(num_divs):
            each_measure_list[measure].append({
                "sub_beat_"+i: []
            })

        while(counter < measure_durations[measure]):
            if(note_to_be_added.rest == False and note_to_be_added.pitch_class == None):
                print("It has no pitch and no rest, what is it?: ")
                print(note_to_be_added)
                print('piano_note:', note_to_be_added.piano_note_name)
                note_to_be_added = notes.pop(0)
                print("Note is:", note_to_be_added)
                duration = note_to_be_added.duration
                continue
            sub_beat = floor(counter/note_to_be_added)
            each_measure_list[measure]["sub_beat_"+sub_beat].append({
                'pitch': note_to_be_added.pitch_class,
                'octave': note_to_be_added.octave,
                'is_rest': note_to_be_added.rest
            })
            counter += 1
            duration -= 1
            if(duration <= 0 and len(notes) > 0):
                note_to_be_added = notes.pop(0)
                print("Note is: ", note_to_be_added)
                duration = note_to_be_added.duration

    diction_to_send[number] = each_measure_list


class HarmonyClass():

    # constructor

    # the first attribute is the scale, and the second
    # attribute is the whole piano starting from any key
    # harmony_piano = Note object Linked list, its a piano, where each key has a name,
    # a previous and a next. Initialized by score parser

    # nevermind, if i use the flat/sharp_notes is better

    # scales: dict,  harmony_piano: dict, start_index, num_divs) -> None:
    def __init__(self, parts=None, calculate_harmony_algorithm=True, verbose=1, parse_harmony_parts=True):
        self.parts = parts
        # It is going to be 0, the root, and the intervals are numbers
        # so a P5 would be in 7
        print("Parts!")
        pprint(parts)
        self.chord_formulas = {
            "triads": {
                'major': ["M", "m", "m", "M", "M", "m", "m-dim"],
                # Should I add the V in this scale too?
                'natural_minor': ["m", 'm-dim', 'M', 'm', 'm', 'M', 'M'],
                'harmonic_minor': ["m", "m-dim", "M-aug", 'm', "M", "M", 'm-dim'],
                # tentative
                'melodic_minor': ["m", 'm', 'M-aug', 'M', 'M', 'M', 'm-dim', 'M', 'm-dim']
            },


            "sevenths": {
                # , 'm-dim-dim7']
                'major': ["M-maj7", "m-m7", "m-m7", "M-maj7", "M-7", "m-m7", 'm-dim-m7'],
                'natural_minor': ["m-m7", 'm-dim-dim7', 'M-maj7', 'm-m7', 'M-7', 'M-maj7', 'm-dim-dim7'],

                # this is wrong, but for the sake of seeing if it gets stuff done
                'harmonic_minor': ["m-m7", 'm-dim-dim7', 'M-maj7', 'm-m7', 'M-7', 'M-maj7', 'm-dim-dim7'],
                'melodic_minor': ["m-m7", 'm-dim-dim7', 'M-maj7', 'm-m7', 'M-7', 'M-maj7', 'm-dim-dim7', "M", 'M']
            }}

        self.triads = {
            "major": {

            },
            "natural_minor": {

            },
            "harmonic_minor": {

            },
            "melodic_minor": {

            }
        }
        self.constructed_chords = {
            "major": {

            },
            "natural_minor": {

            },
            "harmonic_minor": {

            },
            "melodic_minor": {

            }
        }
        # basically each note in scale/chords will have their own chords
        # So for the C we will have C :{
        #   tone:{
        #       Cmaj7
        #       }
        #   third:{
        #     Amin7
        # }
        # fifth:{
        #     F  and so on
        # }
        # }
        triad_to_send = {
            "major": {},
            "natural_minor": {},
            "harmonic_minor": {},
            "melodic_minor": {}

        }

        self.note_with_chords = {
            "major": {},
            "natural_minor": {},
            "harmonic_minor": {},
            "melodic_minor": {}
        }

        # Goal: to create threads for each part. and put it in a function
        # Outdated--> create a dictionary for every note inside the piano. Might be useful for non-diatonic chords
        self.threads_that_parse_parts = []

        # temporary!

        if(self.parts == None):
            return

        number_of_measures = self.parts[0]['number_of_measures']
        self.all_measures = []

        if(not parse_harmony_parts):
            return

        for i in range(number_of_measures):
            self.all_measures.append({
                "measure_"+str(i): {},

            })
            for partidx in self.parts.keys():
                self.all_measures[i]["measure_" +
                                     str(i)]["part-"+str(partidx)] = {}

        for partidx in self.parts.keys():
            new_thread = Thread(target=self.parseParts, args=(

                self.parts[partidx]["id"],
                self.parts[partidx]["is_empty"],
                self.parts[partidx]["key_change"],
                self.parts[partidx]["measure_durations"],
                self.parts[partidx]["notes"],
                self.parts[partidx]["number"],
                self.parts[partidx]["number_of_measures"],
                self.parts[partidx]["time_change"]
            ))
            new_thread.start()
            self.threads_that_parse_parts.append(new_thread)

        for i in range(len(self.threads_that_parse_parts)):
            self.threads_that_parse_parts[i].join()

        #    for key in self.note_with_chords:
        #        for note in harmony_piano['major']:
        #            self.note_with_chords[key][note] = {}
        #            triad_to_send[key][note] = {}

        self.parsed_notes_per_measure = {}

        for partidx in self.parts.keys():
            self.parsed_notes_per_measure["part-" +
                                          str(partidx)] = self.parseNotesV2(self.parts[partidx], partidx)
        # self.parseChord()
        #self.partCollection = None
        if(verbose == 2):
            print("WHat is this and is it correct")
            pprint(self.parsed_notes_per_measure)
            print("notes")
            pprint(self.parts)

        if(calculate_harmony_algorithm):
        # temporary
            self.harmony_result = {}
            for partidx in self.parts.keys():
                if(self.parts[partidx]["is_empty"] == True):
                    continue
                self.harmony_result[partidx] = self.harmony_algorithmV3(
                    self.parsed_notes_per_measure["part-"+str(partidx)],
                    "part-"+str(partidx),
                    self.parts[partidx]["key_change"])
            if(verbose >= 1):
                print("result of harmony algorithm")
                pprint(self.harmony_result)

    def harmony_algorithmV3(self, parsed_notes: dict, partidx, key_change):
        # this is changing when we add the measure key changes, we'd
        # have to have track of which measures
        # have which keys, so if in measure 0 we are in C and measure 5 we are at C minor
        # this has to change
        key_change_index = 0
        #winner_per_measure_subdivision = {}
        winner_per_m_s = {}
        #carrying_pivot_chords = []

        # temporary, how to know which mode is in C major or A minor.

        mode = "major"

        # assumes that chord starts on the Tonic as carrying pivot, if its in C major, it will get C
        first_note = key_change[key_change_index]["possible_scales"][mode][0][0]

        # harmony_graph
        harmony_graph = key_change[key_change_index]["harmony_graph_triads"]

        # circle of fifths

        circle_of_fifths: list = key_change[key_change_index]["circle_of_fifths"][mode]

        # triads as a dictionary with all diatonically triads
        triads = key_change[key_change_index]["mode_triads_and_notes"][mode]["triads"]
        # CM: {
        # label: CM,
        # notes: {C, E, G}
        #
        # }

        # pivot
        pivot = key_change[key_change_index]["mode_triads_and_notes"][mode]["notes"][first_note]["tone"]["label"]
        winner_last_div = {
            "label": pivot,
            "position_array": [0, 0, 0],
            "weight": 0,
            "notes_present": [0, 0, 0]
        }
        # For the circle of fifths
        last_note_played = first_note
        cof_last_note_index = circle_of_fifths.index(first_note)

        # if a phrase is flagged as a circle of fifths passing, set to True, and say if the step is -1 (fifths below)
        # or step is 1 (fifths above)

        # all chords can be accessed by pitch with this variable

        all_chords = key_change[key_change_index]["mode_triads_and_notes"][mode]["notes"]

        # circle of fifths phrasing
        cof_phrasing = False
        cof_step = 0
        # chords following cof
        cof_chord_order = [all_chords[last_note_played]['tone']["label"]]

        for measure in parsed_notes.items():

            # measure is [("measure-0",{subdivision arrays})]

            if(verbose >= 1):
                print("what is measure")
                pprint(measure)
            measure_name = measure[0]
            subdivisions_dictionary = measure[1]

            #
            winner_per_m_s[measure_name] = {}

            for subdivision in subdivisions_dictionary.items():

                # subdivision is ("subdivision-0", array_of_notes = [{note},{note}])
                # where length of the array depends on duration of the note

                subdivision_label = subdivision[0]

                array_of_notes_dictionaries = subdivision[1]

                winner_per_m_s[measure_name][subdivision_label] = []

                # a list of dicts, containing (chord_label, notes_played=[1,0,1,1], weight?)
                #possible_chords = {}
                if(verbose >= 1):
                    print("These are the notes analyzed on: ",
                          measure_name, ' : ', subdivision_label)
                    pprint(array_of_notes_dictionaries)

                found_a_winner = False
                disabled_chords = []
                # debug while
                loop_counter = 0

                while(not found_a_winner):

                    print("loop number: ", loop_counter)
                    loop_counter += 1
                    possible_chords = {}
                    # label with the biggest sum of intense_array and position

                    most_present_chords = []
                    highest_present_weight = 0

                    for i in range(len(array_of_notes_dictionaries)):
                        note_dict = array_of_notes_dictionaries[i]

                        if(note_dict["is_rest"]):
                            continue
                        note_pitch = note_dict["pitch"]

                        all_chords_from_pitch = all_chords[note_pitch]

                        # can it be way more efficient if i just check the intervals from harmony piano?

                        #position is tone, third, fifth and seventh
                        for position in all_chords_from_pitch.keys():
                            # since we are later going to use arrays, this is the better approach
                            # for chord in all_chords_from_pitch[position]:
                            chord_dict = all_chords_from_pitch[position]
                            weight = 0

                            if(verbose == 2):
                                print("for this note: ", note_pitch,
                                      ' look at the ', position, ' and get this chord: ')
                                pprint(chord_dict)

                            # HYPOTHESIS, if the note is not on the pivot chord connected vertices,
                            # that is, if the note has no relationship to the possible next chords, then
                            # its a passing note. If not, record which position and chord.

                            # Second Hypothesis, let's see every note, for chord progressions happening in a measure.
                            # for example, Am Dm in a same beat.
                            # if(chord_dict['label'] in harmony_graph[pivot]):

                            # this array is going to have a 1 on the position, if that note is present

                            # example, if A is present in a Fmaj7 chord, then this array is [0,1,0,0]
                            current_position_array = [0, 0, 0]

                            # just in case, the same thing but with the pitch class on each index
                            notes_present_array = [0, 0, 0]

                            # This is called intensity. Intensity I defined it by how many times
                            # said note was played in a beat of a measure. If the note was played
                            # it was meant to be noticed. If there is a phrase, like D E D C, the D
                            # is meant to be noticed, and we can possibly in the future add if its going down
                            # or up

                            intensity_array = [0, 0, 0]

                            # if the chord is already present in possible_chord dictionary, retrieve its information
                            if(chord_dict["label"] in possible_chords):
                                current_position_array = possible_chords[chord_dict["label"]
                                                                         ]["position_array"]
                                notes_present_array = possible_chords[chord_dict["label"]
                                                                      ]["notes_present"]
                                intensity_array = possible_chords[chord_dict["label"]
                                                                  ]["intensity_array"]

                            if(position == "tone"):
                                index = 0
                            elif(position == "third"):
                                index = 1
                            elif(position == "fifth"):
                                index = 2
                            elif(position == "seventh"):
                                index = 3

                            # if its the same chord than last time, record new position array
                            if(winner_last_div["label"] == chord_dict['label']):
                                winner_last_div["position_array"][index] = 1
                                winner_last_div['notes_present'][index] = note_pitch
                            current_position_array[index] = 1

                            notes_present_array[index] = note_pitch
                            intensity_array[index] += 1
                            #weight = 1
                            this_chord_presence_weight = 0

                            # testing, should i use current, or winner_last_div
                            if(winner_last_div["label"] == chord_dict['label']):
                                for j in range(len(intensity_array)):
                                    this_chord_presence_weight += intensity_array[j] + \
                                        winner_last_div["position_array"][j]
                            else:
                                for j in range(len(intensity_array)):
                                    this_chord_presence_weight += intensity_array[j] + \
                                        current_position_array[j]
                            if(chord_dict["label"] not in disabled_chords):
                                if this_chord_presence_weight > highest_present_weight:
                                    most_present_chords = [chord_dict['label']]
                                    highest_present_weight = this_chord_presence_weight
                                elif this_chord_presence_weight == highest_present_weight:
                                    most_present_chords.append(
                                        chord_dict['label'])

                                possible_chords[chord_dict["label"]] = {
                                    # "weight": weight,
                                    "notes_present": notes_present_array,
                                    "position_array": current_position_array,
                                    "label": chord_dict["label"],
                                    "weight": 0,
                                    "intensity_array": intensity_array,
                                    "chord_presence": this_chord_presence_weight

                                }
                            # elif
                            # if(verbose == 2):
                            #    print("THis chord did not make it: ")
                            #    pprint(chord_dict)
                            #    print("Because this is the vertex we are looking at: ",
                            #          pivot, "and these are its edges:")
                            #    pprint(harmony_graph[pivot])

                        # if the chord[tone] of
                        # index_of_current_note = circle_of_fifths.index(
                        #    note_pitch)
                        # fifth up                                           #fifth_down
                        # if(index_of_current_note-1 == cof_last_note_index or index_of_current_note+1 == cof_last_note_index):
                        #    cof_phrasing = True
                            #cof_step = - 1
                        #    cof_chord_order.append(
                        #        all_chords[note_pitch]["tone"]["label"])

                            # cof_chord_order.append(all_chords[note_pitch]["tone"])

                        # fifth down
                        # elif(index_of_current_note+1 == cof_last_note_index):
                        #    cof_phrasing = True
                        #    cof_step = 1
                        #    cof_chord_order = [
                        #        all_chords[last_note_played]["tone"]["label"], all_chords[note_pitch]["tone"]["label"]]

                    # this variable is going to decide which chord wins
                    max_weight = 0
                    # possible winners will contain chord winners
                    possible_winners = []
                    there_is_tie = False
                    # test, check for circle of fifths phrasing, and then if there is no cof_phrasing end it.
                    # if(cof_phrasing and (cof_chord_order[0] in harmony_graph[pivot])):
                    #    for chord_label in cof_chord_order:
                    #        pivot = chord_label
                    #        weight_of_edge = harmony_graph[pivot][chord_label]["weight"]
                    #        possible_winners.append({
                    #            "label": chord_label,
                    #            "notes_present": possible_chords[chord_label]["notes_present"],
                    #            "position_array": possible_chords[chord_label]["position_array"],
                    #            "weight": self.calculate_weight(weight_of_edge, possible_chords[chord_label]["position_array"])
    #
                    #        })
                    # this is for the chords outside of pivot
                    secondary_max_weight = 1

                    # if there are chords who can follow up then run the algorithm.
                    # elif

                    # if this is set to true, then there is an intense chord, and it is connected to the harmony_graph
                    if(verbose >= 1):
                        print("Checkpoint! ")
                        print("Intense chords: ", most_present_chords)
                        print("Possible chords:")
                        pprint(possible_chords)
                        print("Pivot: ", pivot)
                        print("winner last div:")
                        pprint(winner_last_div)
                    found_intense_connected_chord = False
                    if(possible_chords):
                        if(verbose >= 1):
                            print(
                                "These are the chords that are going to be analyzed")
                            pprint(possible_chords)
                        for chord_items in possible_chords.items():

                            # TEMP
                            chord_label = chord_items[0]
                            chord = chord_items[1]

                            # if the chord_labe

                            if(chord_label in harmony_graph[pivot] and chord_label in most_present_chords):
                                found_intense_connected_chord = True
                                found_a_winner = True

                                position_array = chord["position_array"]
                                if(chord["label"] == winner_last_div["label"]):
                                    position_array = winner_last_div["position_array"]
                                chord_presence = chord["chord_presence"]

                                weight_of_edge = harmony_graph[pivot][chord["label"]]["weight"]
                                this_chord_weight = self.calculate_weight(
                                    weight_of_edge, position_array, chord_presence)
                                if(verbose >= 1):
                                    print(
                                        "Looking at the ", chord["label"], "and it has ", position_array, " in its position array")
                                    print("It has this weight: ",
                                          this_chord_weight)

                                if this_chord_weight > max_weight:
                                    max_weight = this_chord_weight
                                    possible_winners = [{
                                        "label": chord['label'],
                                        "position_array":chord["position_array"],
                                        "notes_present":chord['notes_present'],
                                        "weight": this_chord_weight
                                    }]
                                    there_is_tie = False

                                elif(this_chord_weight == max_weight):
                                    possible_winners.append({
                                        "label": chord['label'],
                                        "position_array": chord["position_array"],
                                        "notes_present": chord['notes_present'],
                                        "weight": this_chord_weight
                                    })
                                    if(verbose == 2):
                                        print("THERE WAS A TIE BETWEEN: ")
                                        pprint(possible_winners)
                                    there_is_tie = True

                        # if it is inside of this if, that means, most_intense_chords are not connected to harmony_graph[pivot]
                        # It could be that it was connected, but not on
                        # the most intense, so this code is, check if there can be
                        # a connection between the most intense, and an intermidiate chord.
                        if(found_intense_connected_chord != True):

                            # if there is no connection, then we need to go to the second most intense chords

                            found_a_connection = False

                            # the biggest connected edge weight
                            max_connected_edge_weight = 0
                            # the label max weight corresponds to
                            max_label = 0
                            winner_chord_label = 0
                            for chord_label in most_present_chords:
                                for connected_chord in harmony_graph[pivot].keys():
                                    # go for each connected edge, see if its connected to
                                    # the label, check for its weight and pick the highest weight
                                    # if there is only one, then the progression first is the connected_edge, then
                                    # ,chord_label.
                                    # if there is more than one then ????????
                                    # if there is no connection to that chord, then what happened???
                                    if(connected_chord in disabled_chords or connected_chord not in possible_chords):
                                        if(verbose >= 1):
                                            print(
                                                "This chord is in disabled chords: ", connected_chord)
                                            pprint("Disabled_chords: ")
                                            pprint(disabled_chords)
                                            print("At measure: ", measure_name)
                                            print("At subdivision: ",
                                                  subdivision_label)
                                            print("Notes analyzed: ")
                                            pprint(notes_present_array)
                                            print("pivot: ", pivot)
                                        continue
                                    intermidiate_chord_vertex = possible_chords[connected_chord]
                                    # Example,  on how this works
                                    # Lets say the chord_label says Dm, and the progression is Em, Am, Dm.
                                    # pivot is Em. since Em, is not connected to Dm, but we want to get
                                    # from Em, to Am, to Dm. So we check for each connected_chord from the
                                    # pivot, Em.
                                    # we then check if they are connected to Dm. If they are, calculate the weight of
                                    # that one, to later choose between the biggest weight.

                                    # this condition says, is this edge connected to the chord we are looking for, AND, do they play the
                                    # 1st note of the chord (because the first note of the chord indicates)
                                    # the chord they are at
                                    # Change to 2
                                    if(verbose >= 1):
                                        print('if',  chord_label, "in")
                                        pprint(harmony_graph[connected_chord])
                                        print('from', connected_chord)

                                    # and intermidiate_chord_vertex['position_array'][0] == 1):
                                    if(chord_label in harmony_graph[connected_chord]):

                                        position_array = intermidiate_chord_vertex["position_array"]

                                        if(chord_label == winner_last_div["label"]):
                                            position_array = winner_last_div["position_array"]
                                        chord_presence = intermidiate_chord_vertex["chord_presence"]

                                        weight_of_edge = harmony_graph[pivot][intermidiate_chord_vertex["label"]]["weight"]
                                        this_chord_weight = self.calculate_weight(
                                            weight_of_edge, position_array, chord_presence)

                                        if(verbose >= 1):
                                            print('WE ARE IN')
                                            print('Stats: ')
                                            print(
                                                "weight of edge: ", weight_of_edge, "\n this_chord_weight: ", this_chord_weight)
                                            print(
                                                "The if statement results in :", this_chord_weight >= 2 * weight_of_edge)

                                        # the reason for this, if this_chord_weight >= 2*weight_of_edge, that means that at least
                                        # the 1 is being played, or the 3,5th are being played
                                        if(this_chord_weight >= 2 * weight_of_edge):
                                            found_a_connection = True

                                            # if(weight_of_edge >= max_connected_edge_weight):
                                            #    max_label = intermidiate_chord_vertex["label"]

                                            if this_chord_weight > secondary_max_weight:
                                                secondary_max_weight = this_chord_weight
                                                max_label = intermidiate_chord_vertex["label"]
                                                chosen_intermidiate = {

                                                    "label": intermidiate_chord_vertex["label"],
                                                    "position_array": position_array,
                                                    "notes_present": intermidiate_chord_vertex["notes_present"],
                                                    "weight": this_chord_weight

                                                }

                                                winner_chord_label = chord_label
                                            # elif(this_chord_weight == secondary_max_weight):
                                            #    # there is a tie between the intermidiate
                                            #    chosen_intermidiate[intermidiate_chord_vertex["label"]] = {
                                            #        "label": intermidiate_chord_vertex["label"],
                                            #        "position_array": position_array,
                                            #        "notes_present": intermidiate_chord_vertex["notes_present"],
                                            #        "weight": this_chord_weight
                                            #    }

                                        else:
                                            continue

                                    else:
                                        continue

                            if(not found_a_connection):
                                for label in most_present_chords:
                                    disabled_chords.append(label)

                            elif(len(chosen_intermidiate) >= 1):
                                destination_chord = possible_chords[winner_chord_label]
                                weight_of_edge = harmony_graph[max_label][destination_chord["label"]]["weight"]

                                this_chord_weight = self.calculate_weight(weight_of_edge, destination_chord["position_array"],
                                                                          destination_chord["chord_presence"])
                                possible_winners = [chosen_intermidiate,
                                                    {
                                                        "label": destination_chord["label"],
                                                        "weight": this_chord_weight,
                                                        "notes_present": destination_chord["notes_present"],
                                                        "position_array": destination_chord["position_array"]
                                                    }
                                                    ]
                                found_a_winner = True
                                if(verbose >= 1):
                                    print("These were the winners")
                                    pprint(possible_winners)
                                winner_last_div = possible_winners[len(
                                    possible_winners)-1]
                                pivot = winner_last_div["label"]
                                winner_per_m_s[measure_name][subdivision_label] = possible_winners

                        # then this means there was an intense chord and a connection
                        # here ties will be decided?

                        # if this is true, possible chords has len > 0
                        elif(found_intense_connected_chord == True):
                            if(there_is_tie and verbose >= 1):
                                print("THERE IS A TIE BETWEEN")
                                pprint(possible_winners)
                            elif(verbose >= 1):
                                print("No tie, this was the winner")
                                pprint(possible_winners)

                            winner_per_m_s[measure_name][subdivision_label] = possible_winners

                            winner_last_div = possible_winners[len(
                                possible_winners)-1]
                            pivot = winner_last_div["label"]
                            found_a_winner = True

                    elif((not possible_chords)):
                        print("NO IDENTIFIABLE CHORDS INSIDE OF DIATONIC")
                        if(verbose >= 1):
                            print(
                                "Nobody won, can be unidentified chord or the same.")
                            print("these are the notes")
                            pprint(array_of_notes_dictionaries)
                        winner_per_m_s[measure_name][subdivision_label] = [{
                            "label": "UNIDENTIFIED",
                            "notes_played_in_sub_div": array_of_notes_dictionaries
                        }]
                        found_a_winner = True
                    # if(len(possible_winners) > 0):
                    #    if(there_is_tie and verbose >= 1):
                    #        print("THERE IS A TIE BETWEEN")
                    #        pprint(possible_winners)
                    #    elif(verbose >= 1):
                    #        print("No tie, this was the winner")
                    #        pprint(possible_winners)

                    #    winner_per_m_s[measure_name][subdivision_label] = possible_winners

                    #    winner_last_div = possible_winners[0]
                    #    pivot = winner_last_div["label"]
                if(verbose >= 1):
                    print("For measure ", measure_name,
                          " and subdiv ", subdivision_label)
                    print('chosen winner is: ')
                    print(winner_last_div)
        return winner_per_m_s

    def harmony_algorithmV2(self, parsed_notes: dict, partidx):

        # changing when we add the measure key changes, we'dhave to have track of which measures
        # have which keys
        key_change_index = 0
        #winner_per_measure_subdivision = {}
        winner_per_m_s = {}
        #carrying_pivot_chords = []

        # temporary, how to know which mode is in C major or A minor.

        mode = "major"

        for measure in parsed_notes.items():
            measure_name = parsed_notes[0]
            subdivisions_dictionary = parsed_notes[1]

            # not the best algorithm but
            # we assume new chords each measure

            carrying_pivot_chords = []

            for subdivision in subdivisions_dictionary.items():
                subdivision_label = subdivision[0]

                # each element of array is a note_dict containing {order_in_measure, pitch}
                array_of_notes_dictionaries = subdivision[1]
                new_pivot_chords = {}

                max_weight = 0

                for i in range(len(array_of_notes_dictionaries)):
                    note_dict = array_of_notes_dictionaries[i]

                    if(note_dict["is_rest"]):
                        continue
                    note_pitch = note_dict["pitch"]
                    all_chords_from_pitch = self.key_change[partidx][mode]["notes"][note_pitch]

                    # can it be way more efficient if i just check the intervals from harmony piano?

                    #position is tone, third, fifth and seventh
                    for position in all_chords_from_pitch.keys():
                        # since we are later going to use arrays, this is the better approach
                        # for chord in all_chords_from_pitch[position]:
                        chord_dict = all_chords_from_pitch[position]
                        weight = 0
                        if(not new_pivot_chords.has_key(chord_dict["label"])):

                            # this array is going to have a 1 on the position, if that note is present

                            # example, if A is present in a Fmaj7 chord, then this array is [0,1,0,0]
                            position_array = [0, 0, 0, 0]
                            # just in case, the same thing but with the pitch class on each index
                            notes_present_array = [0, 0, 0, 0]
                            if(position == "tone"):
                                index = 0
                            elif(position == "third"):
                                index = 1
                            elif(position == "fifth"):
                                index = 2
                            elif(position == "seventh"):
                                index = 3

                            position_array[index] = 1
                            notes_present_array[index] = note_pitch
                            weight = 1
                            new_pivot_chords[chord_dict["label"]] = {
                                "weight": weight,
                                "notes_present": notes_present_array,
                                "note_position": position_array
                            }

                        else:
                            if(position == "tone"):
                                index = 0
                            elif(position == "third"):
                                index = 1
                            elif(position == "fifth"):
                                index = 2
                            elif(position == "seventh"):
                                index = 3
                            position_array = new_pivot_chords[chord_dict["label"]
                                                              ]["note_position"]
                            notes_present_array = new_pivot_chords[chord_dict["label"]
                                                                   ]["notes_present"]
                            if(position_array[index] == 0):
                                position_array[index] = 1
                                notes_present_array[index] = note_pitch
                                weight = new_pivot_chords[chord_dict["label"]
                                                          ]["weight"] + 1
                                new_pivot_chords[chord_dict["label"]] = {
                                    "weight": weight,
                                    "notes_present": notes_present_array,
                                    "note_position": position_array
                                }
                        if(max_weight < weight):
                            max_weight = weight

    def parseNotesV2(self, part: dict, partidx):
        notes = part['notes'].copy()
        number_of_measures = part["number_of_measures"]
        measure_durations = part["measure_durations"]
        time_changes = part["time_change"]
        is_empty = part['is_empty']

        note_to_be_added = notes.pop(0)
        duration = note_to_be_added.duration

        # reference Measure 1: subdivision 1, 2, 3, 4,
        dictionary_to_send = {}
        if(is_empty):
            return None

        for i in range(len(time_changes)):
            starting_measure = time_changes[i]["starting_measure"]
            ending_measure = time_changes[i]["ending_measure"]
            if(ending_measure == None):
                ending_measure = number_of_measures
            for j in range(starting_measure, ending_measure):
                measure_dur = measure_durations[j]
                dictionary_to_send["measure_"+str(j)] = {}
                # amount of notes per array according to the duration, so if variable is 8, and i find a note
                # with duration 8, the array is full
                amount_of_notes = int(measure_dur /
                                      time_changes[i]["numbeats"])
                if(verbose >= 1):
                    print("Amount of notes:", amount_of_notes)
                amount_of_arrays = int(measure_dur/amount_of_notes)
                for k in range(amount_of_arrays):
                    subdivision_array = []
                    counter = 0
                    order_of_notes = 0
                    while(counter < amount_of_notes and len(notes) > 0):
                        if(note_to_be_added.rest == False and note_to_be_added.pitch_class == None):
                            if(verbose >= 1):
                                print("Not a pitch, nor rest",
                                      note_to_be_added)
                            note_to_be_added = notes.pop(0)
                            duration = note_to_be_added.duration
                            continue
                        if(verbose >= 1):
                            print("This is the note on measure-" +
                                  str(j)+" on part-"+str(part["number"]))
                            print(note_to_be_added)

                        # This means, if the array is still empty enough to fit a duration,
                        # then put it in
                        if(duration <= amount_of_notes - counter):
                            counter += duration
                            subdivision_array.append({
                                "pitch": note_to_be_added.pitch_class,
                                "octave": note_to_be_added.octave,
                                "duration": note_to_be_added.duration,
                                "order_of_notes": order_of_notes,
                                "is_rest": note_to_be_added.rest
                            })
                            order_of_notes += 1
                            note_to_be_added = notes.pop(0)
                            duration = note_to_be_added.duration
                        # Only part of the note fits
                        elif(duration > amount_of_notes-counter):
                            note_to_be_added.duration -= (
                                amount_of_notes - counter)
                            duration = note_to_be_added.duration

                            subdivision_array.append({
                                "pitch": note_to_be_added.pitch_class,
                                "octave": note_to_be_added.octave,
                                "duration": amount_of_notes - counter,
                                "order_of_notes": order_of_notes,
                                "is_rest": note_to_be_added.rest
                            })
                            counter = amount_of_notes
                            order_of_notes += 1
                    dictionary_to_send["measure_" +
                                       str(j)]["subdivision_"+str(k)] = subdivision_array
        return dictionary_to_send

    def parseParts(self, id, is_empty, key_change, measure_durations, notes, number, number_of_measures, time_change):

        # initialize the part number on each measure

        if(is_empty):
            return

        # each index is all the times the song changes key.
        for index in range(len(key_change)):
            key_change[index]["mode_chords_and_notes"] = self.parseChord(
                key_change[index]["harmony_piano"], key_change[index]["possible_scales"])
            key_change[index]["mode_triads_and_notes"] = self.parseTriads(
                key_change[index]["harmony_piano"], key_change[index]["possible_scales"])
            # this will contain a graph following the circle of fifths
            key_change[index]["harmony_graph_triads"] = self.create_harmony_graph(
                key_change[index]["mode_triads_and_notes"], key_change[index]["harmony_piano"],
                key_change[index]["possible_scales"]
            )
            key_change[index]['circle_of_fifths'] = self.create_circle_of_fifths(
                key_change[index]["harmony_piano"],
                key_change[index]["possible_scales"]
            )

            if(verbose >= 1):
                print("Circle of fifths: ")
                pprint(key_change[index]['circle_of_fifths'])

        # create the subdivisions for each measure,
        # we are going to create a measure_n that contains b subdivisions, each of them containing
        # a k length array, where b and k are in relation to b*k == measure_n_duration

        #subdivisions = {}
        #print("before, all measures: ")
        # pprint(self.all_measures)
        # self.parseNotes(number, measure_durations, number_of_measures,
        #                time_change, notes, is_empty, subdivisions)
        #print("The result of all measures")
        # pprint(self.all_measures)
    def create_circle_of_fifths(self, harmony_piano, possible_scales: dict):
        # temporary, only creating circle of fifths for major

        # formula for circle of fiths
        formula = [3, 0, 4, 1, 5, 2, 6]
        circle_of_fifths = {}
        for mode in possible_scales.keys():
            circle_of_fifths[mode] = []
            for degree in formula:
                note = ''.join(
                    i for i in possible_scales[mode][degree] if not i.isdigit())
                circle_of_fifths[mode].append(note)
        return circle_of_fifths

    def parseTriads(self, harmony_piano, possible_scales):
        # The harmony_piano will have the notes we are starting with
        # , and the fifth is 7 half steps. but, if dim is present, the fifth
        # is 6 steps

        fifth = 7
        third = 4
        triad_to_send = {}
        for mode in possible_scales:
            triad_to_send[mode] = {
                "triads": {

                },
                "notes": {

                }
            }
            for note in harmony_piano['major']:
                triad_to_send[mode]["notes"][note] = {}
            if(verbose >= 1):
                print("These are the notes inside chords_to_send [notes]")
                pprint(triad_to_send[mode]["notes"])
                print("This is harmony piano: ")
                pprint(harmony_piano)

            for note_scale in possible_scales[mode]:
                #triad_to_send[mode]["notes"][note[0]] = {}
                # index of note in harmony piano
                note = ''.join(i for i in note_scale if not i.isdigit())

                index_of_note = harmony_piano['major'].index(note)

                # index of note in formula
                index_of_formula = possible_scales[mode].index(note_scale)

                formula_to_follow_triad = self.chord_formulas["triads"][mode][index_of_formula]

                formula_to_follow_triad_split = formula_to_follow_triad.split(
                    '-')

                if("dim" in formula_to_follow_triad_split):
                    fifth = 6
                elif("aug" in formula_to_follow_triad_split):
                    fifth = 8
                else:
                    fifth = 7
                if("m" in formula_to_follow_triad_split):
                    third = 3
                elif("M" in formula_to_follow_triad_split):
                    third = 4

                chord_label = note + formula_to_follow_triad

                triad = set()
                triad.add(note)

                third_note = harmony_piano['major'][(
                    (index_of_note+third) % len(harmony_piano['major']))]
                fifth_note = harmony_piano['major'][(
                    (index_of_note+fifth) % len(harmony_piano['major']))]
                triad.add(third_note)
                triad.add(fifth_note)

                if(verbose >= 1):
                    print("CHECKPOINT TRIAD")
                    pprint(triad)
                    print("initial note:", note)
                    print("chord_label", chord_label)

                # should be changed to arrays later on, so that we can have multiple chords in Tone, third etc.
                triad_to_send[mode]["triads"][chord_label] = {
                    # "weight": 0,
                    "chord_notes": triad
                }
                triad_to_send[mode]["notes"][note]["tone"] = {
                    "notes": triad,
                    "label": chord_label,
                    # "weight": 0
                }
                triad_to_send[mode]["notes"][third_note]["third"] = {
                    "notes": triad,
                    "label": chord_label,
                    # "weight": 0
                }
                triad_to_send[mode]["notes"][fifth_note]["fifth"] = {
                    "notes": triad,
                    "label": chord_label,
                    # "weight": 0
                }
        return triad_to_send

    def parseChord(self, harmony_piano, possible_scales):

        # The harmony_piano will have the notes we are starting with
        # , and the fifth is 7 half steps. but, if dim is present, the fifth
        # is 6 steps

        fifth = 7
        third = 4
        chords_to_send = {}

        for mode in possible_scales:
            chords_to_send[mode] = {
                "chords": {

                },
                "notes": {

                }
            }
            for note in harmony_piano['major']:
                chords_to_send[mode]["notes"][note] = {}
            if(verbose >= 1):
                print("These are the notes inside chords_to_send [notes]")
                pprint(chords_to_send[mode]["notes"])
                print("This is harmony piano: ")
                pprint(harmony_piano)
            for note_scale in possible_scales[mode]:
                #triad_to_send[mode]["notes"][note[0]] = {}
                # index of note in harmony piano
                note = ''.join(i for i in note_scale if not i.isdigit())

                index_of_note = harmony_piano['major'].index(note)

                # index of note in formula
                index_of_formula = possible_scales[mode].index(note_scale)

                # not the best code but

                formula_to_follow_chord = self.chord_formulas["sevenths"][mode][index_of_formula]
                formula_to_follow_chord_split = formula_to_follow_chord.split(
                    '-')

                if('m' in formula_to_follow_chord_split):
                    third = 3
                elif("M" in formula_to_follow_chord_split):
                    third = 4
                if('dim' in formula_to_follow_chord_split):
                    fifth = 6
                elif('aug' in formula_to_follow_chord_split):
                    fifth = 8
                else:
                    fifth = 7
                if('maj7' in formula_to_follow_chord_split):
                    seventh = 11
                elif('m7' in formula_to_follow_chord_split or '7' in formula_to_follow_chord_split):
                    seventh = 10
                elif('dim7' in formula_to_follow_chord_split):
                    seventh = 9

                chord_label = note + formula_to_follow_chord
                chord = set()
                third_note = harmony_piano['major'][(
                    (index_of_note+third) % len(harmony_piano['major']))]
                fifth_note = harmony_piano['major'][(
                    (index_of_note+fifth) % len(harmony_piano['major']))]
                seventh_note = harmony_piano['major'][(
                    (index_of_note +
                     seventh) % len(harmony_piano['major'])
                )]
                chord.add(note)
                chord.add(third_note)
                chord.add(fifth_note)
                chord.add(seventh_note)
                chords_to_send[mode]["chords"][chord_label] = {
                    "chord_label": chord_label,
                    # "weight": 0,
                    "chord_notes": chord
                }

                # here we are going to create the note_with_triads and note_with_chords
                #
                if verbose >= 1:
                    print(mode)

                # should be changed to arrays later on, so that we can have multiple chords in Tone, third etc.

                chords_to_send[mode]["notes"][note]["tone"] = {
                    "notes": chord,
                    "label": chord_label,
                    # "weight": 0
                }

                chords_to_send[mode]["notes"][third_note]["third"] = {
                    "notes": chord,
                    "label": chord_label,
                    # "weight": 0
                }

                chords_to_send[mode]["notes"][fifth_note]["fifth"] = {
                    "notes": chord,
                    "label": chord_label,
                    # "weight": 0
                }

                chords_to_send[mode]["notes"][seventh_note]["seventh"] = {
                    "notes": chord,
                    "label": chord_label,
                    # "weight": 0
                }
        return chords_to_send

    def calculate_weight(self, weight, position_array, chord_presence):
        weight_to_mul = copy(weight)
        # if the chord does not have the 1 present, then the "which chord" is biased
        if(position_array[0] == 0):
            weight_to_mul -= (weight/2)

        # if there is a third wit the 1 and 3 of the chord, that there is a higher chance
        if(position_array[0] == 1 and position_array[1] == 1):
            weight_to_mul += (weight/2)

        # If there is a fifth with the 1 and 5, there is a higher chance
        if(position_array[0] and position_array[2]):
            weight_to_mul += (weight/2)

        this_chord_weight = weight_to_mul * (chord_presence)
        return this_chord_weight

    def create_harmony_graph(self, mode_with_triads, harmony_piano, possible_scales):

        # temporary, only going to create the graph following major tones
        # it would make more sense to do for mode in possible_scales
        mode = "major"

        harmony_graph = {}
        degrees_order = []
        for note in possible_scales[mode]:

            # corresponding chord that starts with that note
            note = ''.join(i for i in note if not i.isdigit())
            corresponding_chord = mode_with_triads[mode]["notes"][note]['tone']
            degree = (note, corresponding_chord)

            # elements are [(I, I-triad),(ii, ii-triad)...]
            degrees_order.append(degree)

        # this is ugly code, sorry, just following book

        circle_fifth = 8
        # circle_fifth /1.5
        book_progression = 6
        if(verbose >= 1):
            print("Degree_order")
            print(degrees_order)

        # COMMENTED CODE is the old version, we will use only book references,
        # Eliminated stuff include potential ii-vi progressions, or iii - vii
        # and stuff that i included to fit the circle of fiths, back and foward
        for degree in range(len(degrees_order)):
            chord_label = degrees_order[degree][1]["label"]

            harmony_graph[chord_label] = {}

            # the elements are going to be [(degree: weight),(degree:weight)]
            # based on circle of fifths, and the book. Circle of fifths is going to have
            # weight = 8, and book based resolution is 4
            # for the I
            if degree == 0:

                # debatable, should the tonic be in this array? or if it does not
                # identify any chord CHANGE then we can assume its in the same place?
                each_other_degrees = [(degree, book_progression),  # circle_fifth),
                                      (1, book_progression), (2, book_progression),
                                      (3, circle_fifth),  # book_progression),
                                      (4, circle_fifth),  # book_progression),
                                      (5, book_progression),
                                      (6, book_progression)]

            # for the ii
            elif degree == 1:
                each_other_degrees = [(degree, circle_fifth),  # book_progression),
                                      (4, circle_fifth),
                                      (6, book_progression)]
                # (5, circle_fifth)]

            # for the iii

            elif degree == 2:
                # Maybe its more common for vii - iii progression than iii-vii
                # deprecated ^^
                each_other_degrees = [(degree, circle_fifth),  # book_progression),  #
                                      (3, book_progression), (5, circle_fifth)]  # (6, circle_fifth)]

            # for IV, can go to ii, I, vii-dim, V
            elif degree == 3:
                each_other_degrees = [(degree, circle_fifth),
                                      (0, circle_fifth), (1, book_progression), (6, circle_fifth), (4, book_progression)]

            elif degree == 4:
                # V to vi (deceptive-progression) :should this be recorded??? if this happens, 6 can go anywhere
                # V to ii sounds kinda fake?, or uncommon at least
                # What about V to vii?
                each_other_degrees = [(degree, circle_fifth),
                                      (0, circle_fifth), (5, book_progression)]  # (1, circle_fifth)]

            elif degree == 5:
                each_other_degrees = [(degree, circle_fifth),
                                      (3, book_progression), (1, circle_fifth)]  # (2, circle_fifth)]

            elif degree == 6:
                each_other_degrees = [(degree, circle_fifth),
                                      (0, circle_fifth), (4, book_progression), (2, book_progression)]  # circle_fifth)]

            #
            # if(verbose >= 1):
            #    print("what is going on")
            #    pprint(each_other_degrees)
            for index in range(len(each_other_degrees)):
                each_degree = each_other_degrees[index]
                # this is the chord for the others
                # ["label"]
                other_chord = degrees_order[each_degree[0]][1].copy()
                other_chord["weight"] = each_degree[1]
                # each of them are having 2^n weight, because the 1 can go anywhere,

                harmony_graph[chord_label][other_chord["label"]] = other_chord

        if(verbose >= 1):
            print("This is the harmony graph")
            pprint(harmony_graph)

        return harmony_graph

    def parseNotes(self, number, measure_durations, number_of_measures, time_change, notes: list, is_empty, subdivisions):
        if(is_empty):
            return
        all_notes = notes.copy()

        # reference: self.all_measures [{measure_1:
        #   {part_1: subdivision-1, subdiv-2}
        #
        #
        # },{},{}]

        if(verbose >= 1):
            print("Notes: ")
            pprint(notes)

        for each_time_change in range(len(time_change)):
            starting_measure = time_change[each_time_change]["starting_measure"]

            ending_measure = time_change[each_time_change]["ending_measure"]
            if ending_measure == None:
                ending_measure = number_of_measures
            note_to_be_added = all_notes.pop(0)
            duration = note_to_be_added.duration
            if(verbose >= 1):
                print("starting measure and ending measure: ",
                      starting_measure, ending_measure)
            for i in range(starting_measure, ending_measure, 1):

                measure_dur = measure_durations[i]

                # amount of notes per array according to the duration, so if variable is 8, and i find a note
                # with duration 8, the array is full
                amount_of_notes = int(measure_dur /
                                      time_change[each_time_change]["numbeats"])
                if(verbose >= 1):
                    print("Amount of notes:", amount_of_notes)
                amount_of_arrays = int(measure_dur/amount_of_notes)
                if(verbose >= 1):
                    print("Amount of arrays:", amount_of_arrays)

                for j in range(amount_of_arrays):
                    self.all_measures[i]["measure_" +
                                         str(i)]["part-"+str(number)]["sub-division-"+str(j)] = []
                    counter = 0
                    order_of_notes = 0
                    #note_to_be_added = all_notes.pop(0)
                    while(counter < amount_of_notes):
                        if(note_to_be_added.rest == False and note_to_be_added.pitch_class == None):
                            if(verbose >= 1):
                                print("Not a pitch, nor rest",
                                      note_to_be_added)
                            note_to_be_added = all_notes.pop(0)
                            duration = note_to_be_added.duration
                            continue
                        if(verbose >= 1):
                            print("This is the note on measure-" +
                                  str(i+1)+" on part-"+str(j))
                            print(note_to_be_added)

                        # This means, if the array is still empty enough to fit a duration,
                        # then put it in
                        if(duration <= amount_of_notes - counter):
                            counter += duration
                            self.all_measures[i]["measure_" + str(i)]["part-"+str(number)]["sub-division-"+str(j)].append({
                                "pitch": note_to_be_added.pitch_class,
                                "octave": note_to_be_added.octave,
                                "duration": note_to_be_added.duration,
                                "order_of_notes": order_of_notes,
                                "is_rest": note_to_be_added.rest
                            })
                            order_of_notes += 1
                            note_to_be_added = all_notes.pop(0)
                        # Only part of the note fits
                        elif(duration > amount_of_notes-counter):
                            note_to_be_added.duration -= amount_of_notes - counter
                            counter = amount_of_notes
                            self.all_measures[i]["measure_" + str(i)]["part-"+str(number)]["sub-division-"+str(j)].append({
                                "pitch": note_to_be_added.pitch_class,
                                "octave": note_to_be_added.octave,
                                "duration": amount_of_notes - counter,
                                "order_of_notes": order_of_notes,
                                "is_rest": note_to_be_added.rest
                            })
                            order_of_notes += 1

    def setPartCollection(self, parts, verbose, ending_measure):
        self.partCollection = parts
        threading = []
        self.dictionary_with_parts = {}
        for key in parts.keys():
            new_thread = Thread(target=parseParts, args=(parts[key]['id'], parts[key]['is_empty'], parts[key]
                                                         ['measure_durations'], parts[key]['number'], parts[key]['number_of_measures'], parts[key]['notes'], self.dictionary_with_parts, self.num_divs, self.start_index, ending_measure))
            new_thread.start()
            threading.append(new_thread)
        for i in range(len(threading)):
            threading[i].join()
        if(verbose >= 1):
            print("finished")
            pprint(self.dictionary_with_parts)
            for key in self.dictionary_with_parts.keys():
                print("Part number: ", key)
                print("Length of part: ", len(self.dictionary_with_parts[key]))
                for arr_inside in self.dictionary_with_parts[key]:
                    print('Length: ', len(arr_inside))
                    pprint(arr_inside)
        # temporary, trying the new algorithm
        self.results_for_part_2 = self.harmony_algorithm(
            self.dictionary_with_parts[0])

    def harmony_algorithm(self, divided_measures: list):

        # Temporary, until we figure out what key we in

        mode = "major"

        # temporary, divided by 2,
        division_per_measure = 2
        # harmony_per_measure dictionary

        harmony_dict = {}
        chords = self.constructed_chords[mode].copy()
        # so the plan, traverse the part, and add 2 for tonal chords, but 1 to any other chord
        for measure in range(len(divided_measures)):
            harmony_dict["measure-"+str(measure+1)] = {
                "chords": chords.copy(),
                "sub_beat_winner": {}
            }

            for note_ind in range(len(divided_measures[measure])):

                note = divided_measures[measure][note_ind]
                print("note_dict", note)
                if(note["is_rest"]):
                    harmony_dict["measure-" + str(measure+1)]["sub_beat_winner"][note_ind] = {
                        "sub_beat": note_ind,
                        "chord_winners": []
                    }
                    continue
                pitch = note['pitch']

                # to save writing process
                conditional_dict = self.note_with_chords[mode][pitch]
                a_chord_is_found = False
                chords_found = []

                if("tone" in conditional_dict):
                    chord_label = self.note_with_chords[mode][pitch]["tone"]["label"]
                    harmony_dict["measure-" +
                                 str(measure+1)]["chords"][chord_label]["weight"] += 2
                    a_chord_is_found = True
                    chords_found.append("tone")
                if("third" in conditional_dict):
                    chord_label = self.note_with_chords[mode][pitch]["third"]["label"]
                    harmony_dict["measure-" +
                                 str(measure+1)]["chords"][chord_label]["weight"] += 1
                    a_chord_is_found = True
                    chords_found.append("third")
                if("fifth" in conditional_dict):
                    chord_label = self.note_with_chords[mode][pitch]["fifth"]["label"]
                    harmony_dict["measure-" +
                                 str(measure+1)]["chords"][chord_label]["weight"] += 1
                    a_chord_is_found = True
                    chords_found.append("fifth")
                if("seventh" in conditional_dict):
                    chord_label = self.note_with_chords[mode][pitch]["seventh"]["label"]
                    harmony_dict["measure-" +
                                 str(measure+1)]["chords"][chord_label]["weight"] += 1
                    a_chord_is_found = True
                    chords_found.append("seventh")

                max_weight = 0
                if(a_chord_is_found):
                    for chord in harmony_dict["measure-" + str(measure+1)]["chords"]:
                        temp_weight = harmony_dict["measure-" +
                                                   str(measure+1)]["chords"][chord]["weight"]
                        if(temp_weight > max_weight):
                            harmony_dict["measure-" + str(measure+1)]["sub_beat_winner"][note_ind] = {
                                "sub_beat": note_ind,
                                "chord_winners": [chord]
                            }
                            max_weight = temp_weight
                        elif (temp_weight == max_weight):
                            harmony_dict["measure-" + str(measure+1)]["sub_beat_winner"][note_ind]["chord_winners"].append(
                                chord)
                else:
                    harmony_dict["measure-" + str(measure+1)]["sub_beat_winner"][note_ind] = {
                        "sub_beat": note_ind,
                        "chord_winners": ["Unknown"]
                    }
        if(verbose >= 1):
            #pretty = json.dumps(harmony_dict)
            print('Harmony_dict: ', harmony_dict)
        return harmony_dict
