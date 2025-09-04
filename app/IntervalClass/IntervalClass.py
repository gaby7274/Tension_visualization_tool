import sys
sys.path.insert(0, '../'	)
from ScoreParserClass2.ScoreParserClass2 import ScoreParserClass
from HarmonyClass.HarmonyClass import HarmonyClass as HarmonyClass
from pprint import pprint


class IntervalClass:
    def __init__(self, filename=None, calculate_intervals=True, calculate_harmony=False,verbose=1, parse_harmony_parts=True):
        
        self.score_parser = ScoreParserClass(filename, calculate_harmony=False)
        self.harmony_class = HarmonyClass(self.score_parser.parts,  calculate_harmony_algorithm=calculate_harmony,verbose=verbose, parse_harmony_parts=parse_harmony_parts)
        self.verbose = verbose
        # print("IntervalClass initialized")
        # print(self.score_parser.SKNN)
        # print(self.score_parser.FKNN)

        print('This is parts after parsing')
        pprint(self.harmony_class.parsed_notes_per_measure)


        #defining step formula(semitonos)

        self.step_formula ={
            0: 'U',
            1: 'm2',
            2: 'M2',
            3: 'm3',
            4: 'M3',
            5: 'P4',
            6: 'TT',
            7: 'P5',
            8: 'm6',
            9: 'M6',
            10: 'm7',
            11: 'M7',
        }

        #copy of scoreParserClass intervals
        #whole distance of semitones between notes
        self.revnote_idx = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
                            'Cb': 11, 'B#': 0, 'Db': 1, 'C#': 1, 'Eb': 3, 'D#': 3,
                            'Fb': 4, 'E#': 5, 'Gb': 6, 'F#': 6, 'Ab': 8, 'G#': 8,
                            'Bb': 10, 'A#': 10}
        
        self.is_dissonant ={
            'U': False,
            'm2': True,
            'M2': True,
            'm3': False,
            'M3': False,
            'P4': False,
            'TT': True,
            'P5': False,
            'm6': False,
            'M6': False,
            'm7': True,
            'M7': True,
        }



        if(calculate_intervals):
            self.intervals_in_parts={}
            for parsed_parts in self.harmony_class.parsed_notes_per_measure.items():
                self.intervals_in_parts[parsed_parts[0]] = self.calculate_intervals_in_parsed_parts(self.harmony_class.parsed_notes_per_measure)



             
        

        #smaller_piano SKNN used to calculate intervals

        # self.small_piano_SKNN= self.score_parser.SKNN[3:15]
        # self.small_piano_FKNN= self.score_parser.FKNN[3:15]
        
        # print(self.small_piano_SKNN)

        

    def calculate_interval(self, pivot_note,next_note):

        """
        Notes have these structures:
            'notes_played_in_sub_div': 
                [{'duration': 4,
                'is_rest': False,
                'octave': 3,
                'order_of_notes': 0,
                'pitch': 'F'},
                {'duration': 4,
                'is_rest': False,
                'octave': 3,
                'order_of_notes': 1,
                'pitch': 'A#'}]}],

        """


        # in theory, if we want to talk about dissonance and consonnance,
        # 6m=3M, **7m=2M, 9m=2M, 10m=3M, 11m=4M, 13m=4M** (esos ** fue copilot scary)
        # 4J=5J, 3m=6M, 
        # https://www.earmaster.com/music-theory-online/ch05/chapter-5-3.html
        # adicional, sabemos que queremos usar el root note para los acordes, según 
        # https://www.earmaster.com/music-theory-online/ch05/chapter-5-4.html
        # **entonces, para calcular la disonancia, tenemos que hacer la diferencia entre
        # el root note y la nota que queremos calcular, y luego ver si la diferencia es
        # consonante o disonante** (esos ** fue copilot scary)

        print(pivot_note)
        pivot_pitch= pivot_note['pitch']
        next_pitch= next_note['pitch']

        if(pivot_pitch is None or next_pitch is None):

            #el vacío causa tensión???????
            pprint('This is a Silence')
            return False, False

        semitone_distance_pivot = self.revnote_idx[pivot_pitch]
        semitone_distance_next = self.revnote_idx[next_pitch]

        semitone_distance = abs(semitone_distance_next - semitone_distance_pivot)

        


        #step formula maps semitones to intervals
        interval = self.step_formula[semitone_distance]

        #is_dissonant maps intervals to consonance or dissonance
        is_dissonant = self.is_dissonant[interval]

        return interval, is_dissonant
    

        

    def calculate_intervals_in_parsed_parts(self, parts:dict):
        #create total intervals

        intervals_per_measure_subdivision = {}
        if(self.verbose>=1):
            pprint('What is Paaaarts')
            pprint(parts)
        current_note=None

        
        
        for measures in parts.values():
            if(self.verbose>=1):
                pprint('What is in measures')
                pprint(measures)
            if(measures == None):
                #part is empty??
                continue

            for measure, subdivisions in measures.items():
                if(self.verbose>=1):
                    pprint('What is in measure????')
                    pprint(measure)
            
                intervals_per_measure_subdivision[measure] = {}

                
                for subdivision_name, notes in subdivisions.items():
                    if(self.verbose>=1):
                        pprint('What is in sub and notes?????')
                        pprint(subdivision_name)
                        pprint(notes)
                    intervals_per_measure_subdivision[measure][subdivision_name] = []
                    for note in notes:
                        if(current_note==None):
                            current_note=note
                            continue
                        else:
                            
                            interval, is_dissonant = self.calculate_interval(current_note, note)
                            intervals_per_measure_subdivision[measure][subdivision_name].append({
                                'current_note': current_note,
                                'next_note': note,
                                'interval': interval,
                                'is_dissonant': is_dissonant
                            })
                            current_note=note
                    if(self.verbose>=1):
                        pprint('Result  for this sub')
                        pprint(intervals_per_measure_subdivision[measure][subdivision_name])
        return intervals_per_measure_subdivision










def main():
    ic = IntervalClass(filename='../musicxml/BWV848-Prelude-Breitkopf-SATB.musicxml', calculate_intervals=True)



    pprint(ic.intervals_in_parts)
    

    


main()