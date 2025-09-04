//Global variables 
//TODO, make variables changeable interface. 

//to store the current notes played, in modulo 12
notes_playing = {}

//Harmonics of the notes played
harmonics = {}


// After applying harmonic algorithm present
remaining_harmonics = {}

// Up to how many  harmonics to  take in account

max_harmonics = 7


// max periods considered
max_periods_considered = 20


round_function_precision =3

// turn on only if tension works even after releasing a note
after_tension = false


// number to note hash
number_to_note = {0:"C",1:"Db",2:"D",3:"Eb",4:"E",5:"F",6:"F#",7:"G",8:"Ab",9:"A",10:"Bb",11:"B"}

note_to_number = {"C":0,"Db":1,"D":2,"Eb":3,"E":4,"F":5,"F#":6,"G":7,"Ab":8,"A":9,"Bb":10,"B":11}

// random generated chords, 0,4,7 major triad
random_generated_root = 0
third_note = 4
fifth_note = 7



// if(navigator.requestMIDIAccess){
//     onMIDIFailure()
// }



round_function = function(n, decimal_places){
    return Math.round(n*10**decimal_places)/10**decimal_places

}
equal_temperted_hertz_function = function(n){

    exp = (n-69)/12
    return 440 * Math.pow(2,exp)
}


hertz_function= function(original_note, position_in_overtone_series){

    return equal_temperted_hertz_function(original_note) * (position_in_overtone_series+1)
}





// Function is called for each note to calculate the nth harmonics

function calculate_harmonics(note_playing){
    
    /*
    explaining the numbers:
    12: octave
    19: perfect fifth
    24: double octave
    28: major third
    31: minor third
    34: minor seventh
    36: octave
    38: major second
    40: major second (majorthird from octave)
    42: tritone (major second)
    43: perfect fifth
    */

    // To calculate  the herts this is the equation
    // hertz = 440* (2**((n-69)/12))







    the_notes_above =[0, 12, 19, 24, 28, 31, 34, 36, 38, 40, 42, 43] //45, 46, 48, 49, 50, 52, 53, 54, 55, 56, 57]
    //Calculate the harmonics of the notes playing
    note_harmonics = {}

    //In modulo12, structure would be like this  (=> means %12):
    // 60=>0: 4,

    // 64=>4: 1
    // 67=>7: 2
    // 70=>10: 1 and so on
    note_harmonics_in_modulo_12 = {}
    note_harmonics_with_names = {}

    note_harmonics_in_equal_hertz = {}


    //Actual overtone series
    note_harmonics_in_hertz = {}
    //note = note_playing[0]

    note_periods_per_note = {}



   
    for(let note of note_playing)
    {

        note_harmonics[number_to_note[note%12]] = [note]
        note_harmonics_in_modulo_12[number_to_note[note%12]] ={}
        note_harmonics_with_names[number_to_note[note%12]]= {} 
        note_harmonics_in_equal_hertz[number_to_note[note%12]]  = {}  
        note_harmonics_in_hertz[note] = []


        // this is new table, periods.
        // note_periods_per_note[note] = {}
        // calculating harmonics, with names, modular numbers and real numbers  
            for (i = 0; i <=max_harmonics; i++){


                //Current overtone
                overtone = note+the_notes_above[i]
                note_harmonics[number_to_note[note%12]].push(overtone)



                equal_hertz_of_overtone = round_function(equal_temperted_hertz_function(overtone),round_function_precision)
                hertz_of_overtone = round_function(hertz_function(note, i),round_function_precision)

                if(note_harmonics_in_modulo_12[number_to_note[note%12]][overtone%12] == undefined){
                    note_harmonics_in_modulo_12[number_to_note[note%12]][overtone%12] = 0
                }
                note_harmonics_in_modulo_12[number_to_note[note%12]][overtone%12]+=1

                if(note_harmonics_with_names[number_to_note[note%12]][number_to_note[overtone%12]] == undefined){
                    note_harmonics_with_names[number_to_note[note%12]][number_to_note[overtone%12]] = 0
                }
                note_harmonics_with_names[number_to_note[note%12]][number_to_note[overtone%12]]+=1

                note_harmonics_in_equal_hertz[number_to_note[note%12]][overtone] = {
                    hertz:equal_hertz_of_overtone,
                    note: number_to_note[overtone%12],
                    position_in_harmonic: i+1,
                    fundamental: note,
                }

                note_harmonics_in_hertz[note].push({
                    hertz:hertz_of_overtone,
                    note: number_to_note[overtone%12],
                    position_in_harmonic: i+1,
                    fundamental: number_to_note[note%12],
                })

               
            
        }

        hertz_of_note =  round_function(equal_temperted_hertz_function(note),round_function_precision)
        // periods per notes

        periods_of_note = []
        cycle_numbers = []
        for (i=0; i<max_periods_considered;i++){

            

            period = (1/(hertz_of_note)) * (i+1)
            periods_of_note.push(period)
            cycle_numbers.push(i+1)
           
        }
        note_periods_per_note[note] = {
            periods: periods_of_note,
            cycle_numbers: cycle_numbers,
            midi_number:note,
            note_name: number_to_note[note%12] + ((Math.floor(note/12))-1)
        }

        
        

    }
    //console.log(harmonics)
    
    return {harmonics: note_harmonics, harmonics_in_modulo_12: note_harmonics_in_modulo_12, harmonics_with_names: note_harmonics_with_names,
     harmonics_in_equal_hertz: note_harmonics_in_equal_hertz, harmonics_in_hertz: note_harmonics_in_hertz,
    note_periods_per_note: note_periods_per_note}

}


// Function is called to take the current notes played, and calculate the harmonics in the current notes. 

//DEPRECATED
// function calculate_remaining_harmonics(current_harmonics,harmonics_in_modulo_12, harmonics_with_names){

//     // takes current harmonics, and applies algorithm of removing the repeated notes
//     // between each harmonics and create an object of the remaining harmonics



    
//     //console.log("HARMONICS: ",harmonics_with_names)
// //  console.log("CURRENT HARMONICS: ",current_harmonics)
//     //console.log("HARMONICS IN MODULO 12: ",harmonics_in_modulo_12)

//     //This is first draft
//     // I will take the values in harmonics_in_modulo_12 that should be a dictionary
//     // with {note: number of times it appears, note2: number of times it appears...}
//     // then take the keys as an array, sort it 


//     // after sorting, i will take the array of current harmonics keys, sort them and then
//     // check which has less length to adjust the iteration, and then substract the indices
    
//     //The indices that contain common notes, will contain 0 and they will not be added to the remaining harmonics

//     harmonics_values = Object.values(harmonics_in_modulo_12)[0]
//     harmonics_keys = Object.keys(harmonics_values)
//     current_harmonics_keys = Object.keys(current_harmonics)

//     //attempt#2, use hash

//     temp_remaining_harmonics = {...current_harmonics}

//     for (i=0; i<harmonics_keys.length; i++){
//         if(current_harmonics[harmonics_keys[i]] != undefined){
//             delete temp_remaining_harmonics[harmonics_keys[i]]
//         }
//         else{
//             temp_remaining_harmonics[harmonics_keys[i]] = harmonics_values[harmonics_keys[i]]
//         }
//     }


    
//     //maybe useless, lets use HASH INSTEAD


//     // console.log(harmonics_keys)

//     // sorted_harmonics_keys = harmonics_keys.map(num=>parseInt(num)).sort((a,b)=>a-b)

//     // current_harmonics_keys = Object.keys(current_harmonics)


//     // sorted_current_harmonics_keys = current_harmonics_keys.map(num=>parseInt(num)).sort((a,b)=>a-b)

//     // console.log("sortedHarmonics: ",sorted_harmonics_keys)
//     // console.log('sortedCurrent: ', sorted_current_harmonics_keys)
//     // min_length = Math.min(sorted_harmonics_keys.length, sorted_current_harmonics_keys.length)

//     // temp_remaining_harmonics={... current_harmonics, ...harmonics_values}

//     // for( i =0; i<min_length; i++){
//     //     //this means that they are the same note, they have a common overtone
//     //     if(sorted_harmonics_keys[i] - sorted_current_harmonics_keys[i] == 0){
//     //         delete temp_remaining_harmonics[sorted_harmonics_keys[i]] 
//     //         //remaining_harmonics[sorted_current_harmonics_keys[i]] = current_harmonics[sorted_current_harmonics_keys[i]]
//     //     }
//     // }
//     // console.log("REMAINING HARMONICS: ",temp_remaining_harmonics)
// return temp_remaining_harmonics


    


// }

//DEPRECATED
// function calculate_tension_in_harmonics(harmonics_in_hertz){



//     //Maybe deprecated as well, we will see


//     //ALGORITHM IS AS FOLLOWS:
//     /*
//     1. For the n arrays, take the first array and check which notes
//     is divisible in that hertz, For example,
    
//         A. in arrays
//         A= [100,200,300,400,500,600,700,800], 
//         B=[125, 250, 375, 500, 625, 750, 875, 1000]
//         C=[150, 300, 450, 600, 750, 900, 1050, 1200]

//         if B[i]%A[0]===0, then B[i] is a harmonic of A[0], and so,
//         the harmonics shared in A are B[i]/A[0] = integer, 
//         Choice A:
//         harmonics = range(integer, length of A, integer)

//         or  we take i, and the harmonics indeces shared are
//         Choice B:
//         harmonics = range(i, length of B, i+1)

//     2. After  having the shared harmonics we can calculate the not shared harmonics
//     by substracting the shared harmonics from the original harmonics
    
//     3.  


//     */

//     if(Object.keys(harmonics_in_hertz).length == 0){
//         return {
//             consonant_harmonics: {},
//             dissonant_harmonics: {},
//         }
//     }
//     else if(Object.keys(harmonics_in_hertz).length == 1){

//         consonant_harmonics = {}

//         console.log('only_one_note')
//         // all the harmonics of that note are consonant
//         note = Object.keys(harmonics_in_hertz)[0]
//         consonant_harmonics[note] ={}
//         for(let key in harmonics_in_hertz[note]){
//             consonant_harmonics[note][key] ={
//                 note: harmonics_in_hertz[note][key].note,
//                 hertz: harmonics_in_hertz[note][key].hertz,
//             }
//         }
//         return {
//             consonant_harmonics: harmonics_in_hertz[Object.keys(harmonics_in_hertz)[0]],
//             dissonant_harmonics: {},
//         }
//     }

//     consonant_harmonics = {}
//     dissonant_harmonics = {}
//     console.log('two_notes')
//     // Notes that are played
//     notes_present = Object.keys(harmonics_in_hertz)

//     for (let i = 0; i < notes_present.length-1; i++) {
        
//         //We take the pivot array and pivot hertz, the generator of the harmonics
//         pivot_harmonic_array = Object.values(harmonics_in_hertz[notes_present[i]])

//         // Up to here, if we have an array of [100,200...], this will be 100
//         pivot_hertz = pivot_harmonic_array[0].hertz

//         for (let j = i+1; j < notes_present.length; j++) {
//             //we compare that herts with this array

//             consonnance_found_in_compared = false
//             shared_intervals_indeces = []
//             shared_intervals_information ={}
//             unshared_intervals_indeces = []
//             unshared_intervals_information = {}
            
//             //We then compare to each other array




//             compared_harmonic_array = Object.values(harmonics_in_hertz[notes_present[j]])
//             compared_harmonic_array_keys = new Set(Object.keys(harmonics_in_hertz[notes_present[j]]))
//             for(let k = 0; k < compared_harmonic_array.length; k++){


//                 //If the hertz is divisible by the pivot hertz, then it is a shared harmonic
//                 modulo_result=compared_harmonic_array[k].hertz % pivot_hertz 

//                 if(modulo_result == 0){

//                     //CHANGE HERE DEPENDING IF CHOICE A OR B
//                     consonnance_found_in_compared = true
//                     shared_intervals_indeces = d3.range(k, compared_harmonic_array.length, k+1)

//                     unshared_intervals_indeces =d3.range(0, compared_harmonic_array.length, 1)
//                     shared_in_set = new Set(shared_intervals_indeces)
//                     unshared_intervals_indeces = unshared_intervals_indeces.filter(x => !shared_in_set.has(x))

//                     delete shared_in_set
                    

//                     for (let l = 0; l<shared_intervals_in_hertz_indeces.length; l++){
                    
//                         shared_intervals_information[compared_harmonic_array_keys[l]] = {}
//                         shared_intervals_information[compared_harmonic_array_keys[l]]['note']= compared_harmonic_array[shared_intervals_indeces[l]].note
//                         shared_intervals_information[compared_harmonic_array_keys[l]]['hertz']= compared_harmonic_array[shared_intervals_indeces[l]].hertz
//                     }
//                     for (let l = 0; l<unshared_intervals.length; l++){
//                         unshared_intervals_information[compared_harmonic_array_keys[l]] = {}
//                         unshared_intervals_information[compared_harmonic_array_keys[l]]['note']= compared_harmonic_array[unshared_intervals_indeces[l]].note
//                         unshared_intervals_information[compared_harmonic_array_keys[l]]['hertz']= compared_harmonic_array[unshared_intervals_indeces[l]].hertz
    
//                     }
                    

//                     break
                
//                 }
                
                   
//         }

//         // If this is true there is some consonant-ish interval
//         if(consonnance_found_in_compared){
//             consonant_harmonics[notes_present[i]] = shared_intervals_information
//             dissonant_harmonics[notes_present[i]] = unshared_intervals_information
//             }
//         }
//     }

//     return {
//         consonant_harmonics: consonant_harmonics,
//         dissonant_harmonics: dissonant_harmonics,
//     }




    

// }


function calculate_tension_in_harmonicsV2(harmonics_in_hertz){

    // In here we are going to construct a hash of intervals and their harmonics
    // For example

    /*
    C E G events will calculate
    {|60-67 %12|: {
        shared_notes:[(Note_shared (G), [(position_in_harmonic (1), fundamental (60)),(position_in_harmonic (2), note(67))])],
        unshared_notes:[(note_not_shared, [(position_in_note (0), note(60),  position_in_note)]
    },


    //THESE WERE  below GENERATED NOT NECESSARILY is true
    |60-64 %12|: {
        shared_notes:[(Note_shared (E), [(position_in_harmonic (1), fundamental (60)),(position_in_harmonic (2), note(64))])],
        unshared_notes:[(note_not_shared, [(position_in_note (0), note(60),  position_in_note)]
    },
    |64-67 %12|: {
        shared_notes:[(Note_shared (C), [(position_in_harmonic (1), fundamental (60)),(position_in_harmonic (2), note(64))])],
        unshared_notes:[(note_not_shared, [(position_in_note (0), note(60),  position_in_note)]
    },


    */

    //if there are no notes playing, return nothing
    //return nothing if there are no notes playing
    
    if(Object.keys(harmonics_in_hertz).length == 0){
        return {
            harmonics_in_intervals:{}
        }
    }
    // if there is only one note playing, return the note harmonics since they are all consonant
    //return the note harmonics since they are all consonant
    else if(Object.keys(harmonics_in_hertz).length == 1){

        consonant_harmonics = {}

        // console.log('only_one_note')
        // all the harmonics of that note are consonant
        // note = Object.keys(harmonics_in_hertz)[0]
        // consonant_harmonics[note] ={}
        // for(let key in harmonics_in_hertz[note]){
        //     consonant_harmonics[note][key] ={
                 
        //     }
        // }

        return {
           harmonics_in_intervals: {
            0:{
                shared_notes:harmonics_in_hertz,
                unshared_notes:{}
            }
           },
           
        }
    }

    harmonics_in_intervals = {}
    // console.log('two_notes')
    // Notes that are played
    notes_present = Object.keys(harmonics_in_hertz)

    for (let i = 0; i < notes_present.length-1; i++) {
        
        pivot_note_harmonics =  harmonics_in_hertz[notes_present[i]]
        // pivot_harmonic_keys = Object.keys(harmonics_in_hertz[notes_present[i]])
        // // pivot_harmonic_keys_set = new Set(pivot_harmonic_keys)


        for (let j = i+1; j < notes_present.length; j++) {
            //we compare that herts with this array
            // with the ones after it, so we follow a consecutive order
            // if we have 3 notes, we compare 1 with 2, 1 with 3, 2 with 3

            consonnance_found_in_compared = false


            shared_notes =[]
            shared_intervals_indeces = []
            shared_intervals_information ={}
            unshared_intervals_indeces = []
            unshared_intervals_information = {}
            
            //We then compare to each other array


            compared_note_harmonics = harmonics_in_hertz[notes_present[j]]
            compared_harmonic_keys = Object.keys(harmonics_in_hertz[notes_present[j]])
       for(let k = 0; k < compared_harmonic_keys.length; k++){


                //Check if note is inside the pivot_harmonic_keys

                key_to_check = compared_harmonic_keys[k]

                //Example if, key_to_check = 64, then we check if 64 is inside the pivot_harmonic_keys {


                // this means they share a note
                if(pivot_note_harmonics[key_to_check]!= undefined){
                     
                    shared_notes.push(key_to_check)
                    consonnance_found_in_compared = true


                    

                    //Here since we are going to /*

                    /*

                    get the  shared and unshared harmonics of the first note, and the same for the second,
                    we will get the shared and unshared in the second one 

                    */

                    //CHANGE HERE DEPENDING IF CHOICE A OR B
                    // consonnance_found_in_compared = true
                    // shared_intervals_indeces = d3.range(k, pivot_harmonic_array.length, k+1)

                    // unshared_intervals_indeces =d3.range(0, compared_harmonic_array.length, 1)
                    // shared_in_set = new Set(shared_intervals_indeces)
                    // unshared_intervals_indeces = unshared_intervals_indeces.filter(x => !shared_in_set.has(x))

                    // delete shared_in_set
                    

                    // for (let l = 0; l<shared_intervals_indeces.length; l++){
                    
                    //     shared_intervals_information[compared_harmonic_array_keys[l]] = {}
                    //     shared_intervals_information[compared_harmonic_array_keys[l]]['note']= compared_harmonic_array[shared_intervals_indeces[l]].note
                    //     shared_intervals_information[compared_harmonic_array_keys[l]]['hertz']= compared_harmonic_array[shared_intervals_indeces[l]].hertz
                    // }
                    // for (let l = 0; l<unshared_intervals_indeces.length; l++){
                    //     unshared_intervals_information[compared_harmonic_array_keys[l]] = {}
                    //     unshared_intervals_information[compared_harmonic_array_keys[l]]['note']= compared_harmonic_array[unshared_intervals_indeces[l]].note
                    //     unshared_intervals_information[compared_harmonic_array_keys[l]]['hertz']= compared_harmonic_array[unshared_intervals_indeces[l]].hertz
    
                    // }
                    

                    // break


                
                }
                
                   
        }

        // If this is true there is some consonant-ish interval
        if(consonnance_found_in_compared){
            pivot_note_to_number = note_to_number[notes_present[i]]
            compared_note_to_number = note_to_number[notes_present[j]]
            interval = Math.abs(pivot_note_to_number - compared_note_to_number)

            shared_notes_set = new Set(shared_notes)

            //going to  get subdictionaries from notes they do not share

            let unshared_subdictionary_from_pivot = Object.keys(pivot_note_harmonics).reduce((obj, key) => {
            if(!shared_notes_set.has(key)){

                obj[key] = [pivot_note_harmonics[key]]
                
            }
            return obj
            }, {})
            let unshared_subdictionary_from_compared = Object.keys(compared_note_harmonics).reduce((obj, key) => {
                if(!shared_notes_set.has(key)){
                    obj[key] = [compared_note_harmonics[key]]
                   
                }
                return obj
                }, {})

            let shared_subdictionary_from_pivot = Object.keys(pivot_note_harmonics).reduce((obj, key) => {
                if(shared_notes_set.has(key)){
                    obj[key] = [pivot_note_harmonics[key], compared_note_harmonics[key]]
                }
            return obj
            }, {})

            
             
                harmonics_in_intervals[interval] =
                {
                    shared_notes: shared_subdictionary_from_pivot,
                    unshared_notes: {...unshared_subdictionary_from_pivot, ...unshared_subdictionary_from_compared}
                }


                    
        }
    }
}
    // console.log('harmonics_in_intervals: ',harmonics_in_intervals)
    return {
        harmonics_in_intervals: harmonics_in_intervals,
    }




}

function calculate_per_worker(current_notes_playing){
    // Getting all notes present
   
    five_types_of_harmonics = calculate_harmonics(Object.keys(current_notes_playing).map(num=>parseInt(num) ))

    

    harmonics = five_types_of_harmonics.harmonics
    harmonics_in_modulo_12 = five_types_of_harmonics.harmonics_in_modulo_12
    harmonics_with_names = five_types_of_harmonics.harmonics_with_names
    harmonics_in_equal_hertz = five_types_of_harmonics.harmonics_in_equal_hertz

    harmonics_in_hertz = five_types_of_harmonics.harmonics_in_hertz

    // console.log("Harmonics in Hertz: ",harmonics_in_hertz)




    
    consonant_and_dissonant_harmonics = calculate_tension_in_harmonicsV2(harmonics_in_equal_hertz)

    return consonant_and_dissonant_harmonics
}

// MAIN FUNCTION that calculates stuff and calls the visualization
function listen_to_midi(event){


    //Check if the note is already playing
    //Each time a note is played, we need to recalculate the harmonics for the notes that are currently played

    //Future work, let user decide if he wants to visualize when removing a note or not

    //event Data is an array, first element is the type of event, second is the note, third is the velocity
    // data[0 ] is 144 (note on) or 128 note off

    switch (event.data[0]){

        case 128:
            //Note off
            // console.log('borraré')
            delete notes_playing[event.data[1]]
            
            // set_bass_note_for_color(null)
            
            break;
        case 144:
            //Note on, key is note, value is velocity
            notes_playing[event.data[1]] = event.data[2]
            break;
        default:
            break;
        
    }



    




    
    // Getting all notes present
   
    // five_types_of_harmonics = calculate_harmonics(Object.keys(notes_playing).map(num=>parseInt(num) ))

    

   return calculate_harmonics(Object.keys(notes_playing).map(num=>parseInt(num) ))







}



//Use for polling

pressed_r = false

function onMIDIFailure(){

    return
}

function onMIDISuccess(midiAccess){
    //console.log('pa')
    // midiAccess.addEventListener('statechange', updateMidiDevices)
    
    var inputs = midiAccess.inputs;
    inputs.forEach(function(port){
        port.addEventListener('midimessage', listen_to_midi) 
    })
    // var outputs = midiAccess.outputs;
    // for(var input of midiAccess.inputs.values()){
    //     input.onmidimessage = getMIDIMessage;
    // }
}
