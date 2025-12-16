// TODO slider to set harmonics

let max_harmonics = 14
let ihm_cap=null
let max_periods_considered = 20


let current_weight_function = null

let round_function_precision =3

// R_regions with weights
//Default
let r_regions_with_weights = [
    {r_lower:0, r_upper:0.125, weight: null, label:'consonant_region',color:'lightgreen'},
    {r_lower:0.125, r_upper:0.5, weight: null, label:'less_dissonant_region',color:'orange'},
    {r_lower:0.5, r_upper:0.95, weight: null, label:'dissonant_region',color:'red'},
    //Chan weights r_l = 0.95 to r_u=1.1 and r_l=1.5 to r_u 2.8
    {r_lower:0.95, r_upper:1.1, weight: 1, label:'dissonant_region',color:'red'},
    {r_lower:1.1 , r_upper:1.5, weight: null, label:'dissonant_region',color:'red'},
    {r_lower:1.5 , r_upper:2.8, weight: 1, label:'dissonant_region',color:'red'},
    {r_lower:2.8 , r_upper: 3.5, weight: null, label:'less_dissonant_region',color:'orange'},
    {r_lower:3.5 , r_upper: 4.5, weight: null, label:'consonant_region',color:'green'},
    {r_lower:4.5 , r_upper: 5.5, weight: null, label:'dissonant_region',color:'red'},
    {r_lower:5.5 , r_upper: 7.5, weight: null, label:'consonant_region',color:'green'},
    {r_lower:7.5 , r_upper: 8.5, weight: null, label:'less_dissonant_region',color:'orange'},
    {r_lower:8.5 , r_upper: 12.5, weight: null, label:'consonant_region',color:'green'},
]   


//This will store the blue points for modulation.. maybe more info will be added. 
//will contain objects  {ratio(y_axis/region), harmonic_weight, harm_1_index, harm_2_index, delta_f,average_f, note_1, note_2}
data_to_plot_interharmonic = []

// raw modulations for each region
// will be a 2d array where each element is an array of modulations in region
// for a specific note combination

raw_modulations_per_region = []

//weigthed harmonics per region
// same as raw modulations if weight function is 1
harmonics_with_weights_per_region = []

// modulations with weights per region applied. 
// for chan we expect that the sum is the same as only counting
// their two regions with weight 1 
// computed by multiplying the weight of the region by the
// number inside the same index in harmonics_with_weights_per_region

modulations_with_region_weights = []


//should be final tension for each note combination played
//contains two objects, normed tension per interval, and raw tension score
final_tension_score_per_note_combination =[]

// final tension score for all notes is the sum of the above
final_ihm_tension_score  = {
    normed_tension: null,
    raw_tension: null,
}

// question about groundtruth later will be answered. 

// ground truth intervals ordered by expected ranking 
ground_truth_intervals = [
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 1,explicit_rating:null,name:'U',notes:['C4','C4'],   note_combination:'0_0',midi_numbers:[60,60]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 2,explicit_rating:null,name:'P8',notes:['C4','C5'],  note_combination:'0_12',midi_numbers:[60,72]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 3,explicit_rating:null,name:'P5',notes:['C4','G4'],  note_combination:'0_7',midi_numbers:[60,67]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 4,explicit_rating:null,name:'P4',notes:['C4','F4'],  note_combination:'0_5',midi_numbers:[60,65]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 5,explicit_rating:null,name:'M3',notes:['C4','E4'],  note_combination:'0_4',midi_numbers:[60,64]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 6,explicit_rating:null,name:'M6',notes:['C4','A4'],  note_combination:'0_9',midi_numbers:[60,69]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 7,explicit_rating:null,name:'m6',notes:['C4','G#4'], note_combination:'0_8',midi_numbers:[60,68]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 8,explicit_rating:null,name:'m3',notes:['C4','D#4'], note_combination:'0_3',midi_numbers:[60,63]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 9,explicit_rating:null,name:'TT',notes:['C4','F#4'], note_combination:'0_6',midi_numbers:[60,66]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 10,explicit_rating:null,name:'m7',notes:['C4','A#4'],note_combination:'0_10',midi_numbers:[60,70]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 11,explicit_rating:null,name:'M2',notes:['C4','D4'], note_combination:'0_2',midi_numbers:[60,62]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 12,explicit_rating:null,name:'M7',notes:['C4','B4'], note_combination:'0_11',midi_numbers:[60,71]},
    {tension_score_for_method:null,raw_ihm_tension_score:null,ranking: 13,explicit_rating:null,name:'m2',notes:['C4','C#4'],note_combination:'0_1',midi_numbers:[60,61]},
]

// ground truth chords ordered by expected ranking
ground_truth_triads = [
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:1.667,ranking: 1,name:'CM' ,notes:['C4', 'E4', 'G4'], note_combination:'0_4_7' ,midi_numbers:[60,64,67]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:2.407,ranking: 2,name:'Cm' ,notes:['C4', 'D#4','G4'], note_combination:'0_3_7' , midi_numbers:[60,63,67]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:2.741,ranking: 3,name:'FMinv2' ,notes:['C4', 'F4', 'A4'], note_combination:'0_5_9' , midi_numbers:[60,65,69]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:2.852,ranking: 4,name:'Fsus4inv2' ,notes:['C4', 'F4','A#4'],  note_combination:'0_5_10' , midi_numbers:[60,65,70]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:2.889,ranking: 5,name:'G#Minv1' ,notes:['C4', 'D#4','G#4'], note_combination:'0_3_8' , midi_numbers:[60,63,68]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.111,ranking: 6,name:'Csus2' ,notes:['C4', 'D4','G4'], note_combination:'0_2_7'  , midi_numbers:[60,62,67]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.148,ranking: 7,name:'Csus4' ,notes:['C4', 'F4','G4'], note_combination:'0_5_7',   midi_numbers:[60,65,67]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.481,ranking: 8,name:'Fminv2' ,notes:['C4', 'F4','G#4'], note_combination:'0_5_8',  midi_numbers:[60,65,68]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.519,ranking: 9,name:'Adiminv1' ,notes:['C4', 'D#4','A4'], note_combination:'0_3_9', midi_numbers:[60,63,69]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.593,ranking: 10,name:'Aminv1' ,notes:['C4', 'E4', 'A4'], note_combination:'0_4_9', midi_numbers:[60,64,69]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.667,ranking: 11,name:'F#diminv2' ,notes:['C4', 'F#4','A4'], note_combination:'0_6_9', midi_numbers:[60,66,69]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:3.889,ranking: 12,name:'Cdim' ,notes:['C4', 'D#4','F#4'], note_combination:'0_3_6', midi_numbers:[60,63,66]},
    {tension_score_for_method:null, raw_ihm_tension_score:null,explicit_rating:5.259,ranking: 13,name:'Caug' ,notes:['C4', 'E4','G#4'], note_combination:'0_4_8' , midi_numbers:[60,64,68]},

]

current_ground_truth_set = ground_truth_intervals

    
