
from ctypes import py_object
from pprint import pprint
from ScoreParserClass2 import ScoreParserClass
from HarmonyClass import HarmonyClass


sp = ScoreParserClass(
    "musicxml/BWV846-Fugue-Breitkopf-SATB.musicxml", verbose=1)


# attempt to know which are the scales we can be in

print(list(sp.FKNN.keys()))

pprint(sp.parts)

possible_keys = {
    "major": [],
    "natural_minor": [],
    "harmonic_minor": [],
    "melodic_minor": []
}

sp.initial_key = 4

# this means its flat
if sp.initial_key < 0:
    allKeys = list(sp.FKNN.keys())

    # first index_of_note means the tone


# else is sharp
else:
    allKeys = list(sp.SKNN.keys())


# assuming it will always be in order


allKeys.pop(0)
allKeys.pop(0)
allKeys.pop(0)

index_of_c = allKeys.index("C1")
pprint(allKeys)

# first value is the key note
index_of_note = (index_of_c + 7 * (sp.initial_key)) % len(allKeys)

# possible keys are with their respective formulas, TTSTTTS, or WWHWWWH
formulas = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "natural_minor": [2, 1, 2, 2, 1, 2, 2],
    "harmonic_minor": [2, 1, 2, 2, 1, 3, 1],
    "melodic_minor": [2, 1, 2, 2, 1, 1, 1, 1, 1]
}

# then it will change to 3 after major
relative_minor = 0
for form in formulas.keys():

    for i in range(len(formulas[form])):
        possible_keys[form].append(allKeys[index_of_note])
        index_of_note = (index_of_note + formulas[form][i]) % len(allKeys)
    if form == "major":

        # after the first form, now the relative minors come along
        index_of_note -= 3
print(possible_keys)
