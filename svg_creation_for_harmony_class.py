
from ctypes import py_object
from pprint import pprint
from ScoreParserClass2 import ScoreParserClass
import HarmonyClass.HarmonyClass as HarmonyClass
import svgwrite

scores_to_graph = [
    "musicxml/BWV846-Fugue-Breitkopf-SATB.musicxml",
    # "musicxml/BWV846-Prelude-Breitkopf-SATB.musicxml",
    # "musicxml/BWV848-Fugue-Breitkopf-SATB.musicxml",
    # "musicxml/BWV848-Prelude-Breitkopf-SATB.musicxml",


]
rainbow_color = [
    svgwrite.rgb(95, 40, 121, '%'),

    svgwrite.rgb(244, 53, 69, '%'),
    svgwrite.rgb(250, 137, 1, '%'),
    svgwrite.rgb(250, 215, 23, '%'),
    svgwrite.rgb(0, 186, 113, '%'),
    svgwrite.rgb(0, 194, 222, '%'),
    svgwrite.rgb(0, 65, 141, '%'),

]

dimensions_for_background = {
    "width": 8000,
    "height": 3000,
}

dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(
    dwg.rect(
        (0, 0), (dimensions_for_background["width"],
                 dimensions_for_background['height']),
        stroke="white", fill="black")
)

height_step_for_part = dimensions_for_background["height"]/4


for score in scores_to_graph:
    sp = ScoreParserClass(
        score, verbose=0)

    harmony_class = sp.harmony_class
    SATB_parts = sp.parts

    for partidx in SATB_parts.keys():
        number_of_measures = SATB_parts[partidx]['number_of_measures']
        results_for_part = harmony_class.harmony_result[partidx]

        rotation_step = 360/number_of_measures

        # temp
        circle_of_fifths = SATB_parts[partidx]["key_change"][0]["circle_of_fifths"]['major']
        print(circle_of_fifths)
        major_notes_connected_to_triads = SATB_parts[partidx][
            "key_change"][0]['mode_triads_and_notes']["major"]['notes']

        rotation_for_cof = 360/len(circle_of_fifths)

        chord_rotation = {}
        # innefficient

        height_for_this_part = 200 + height_step_for_part * int(partidx)

        for noteidx in range(len(circle_of_fifths)):
            note = circle_of_fifths[noteidx]
            chord_label = major_notes_connected_to_triads[note]["tone"]['label']
            # for the first one, to be at a negative rotation.
            formula_for_rotation = (
                rotation_for_cof - (rotation_for_cof*noteidx)) % 360

            chord_rotation[chord_label] = {
                'rotation': formula_for_rotation,
                'color': rainbow_color[noteidx],

            }

        # temp_translate = 2000 / 5
        # for i in range(number_of_measures):
        #    measure_results = results_for_part["measure_"+str(i)]
        #    subdivision_len = len(measure_results)
        #    rotation_for_this_measure = rotation_step * i
        #    for j in range(subdivision_len):
        #        subdivision = measure_results["subdivision_"+str(j)]
        #        for chord_dict in subdivision:
        #            chord_label = chord_dict["label"]
        #            if(chord_label in chord_rotation):
        #                path = dwg.path(d="M0, 0 C30, 20, 30, 60, 0, 80 C-30, 60, -30,20, 0,0",
        #                                stroke=chord_rotation[chord_label]['color'],
        #                                stroke_width=4,
        #                                transform="rotate("+str(
        #                                    chord_rotation[chord_label]["rotation"]+rotation_for_this_measure)+"), translate("+str(temp_translate * j + 300)+", "+str(height_for_this_part)+")", fill="black")
        #                dwg.add(path)

dwg.save()
