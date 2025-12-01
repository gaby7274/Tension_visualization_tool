
/*
TODO: 
1. Given note_periods_per_note_per_cycle, preprocess into a json object that contains
    a. midi_numbers: [midi_number1, midi_number2, ...]
    b. note_periods: [[t_1c1, t_1c2, ...], [t_2c1, t_2c2, ...], ...]
    c. cycles: [[c1, c2, ...], [c1, c2, ...], ...]
    d. note_names: [note_name1, note_name2, ...]

    FUNCTION preprocess_data(note_periods_per_note_per_cycle)

2. Find min max bounds

    Find bounds (or cycle number bounds) with minimum distances from the bass note and the highest note.

    FUNCTION find_min_max_bounds(note_periods, cycles)

    returns a list of bounds, each bound contains:
            useful_information_of_each_bound_pair.push({
            highest_note_cycle: j+1,
            bass_note_cycle:i+1,
            mean: mid_point,
            bass_note_period: bass_periods[i],
            highest_note_period: highest_note_periods[j],
            distance:distance,
            ratio:ratio,
            abs_distance: Math.abs(distance)
        })

3. For each bound, find the closest pair of notes for each note in between

    From the bounds, we will do a binary search from the complete table of note_periods
    being played, and find the closest pair of notes for each note in between the bass and highest note.



    FUNCTION binary_search_with_bounds(start_bound_index, end_bound_index, mean, other_note_periods)

    returns a list that contains this information for each note       
        chosen_winners.push({
            cycle: candidate_cycle,
            period: candidate_period,
            difference: candidate_difference,
            note_position:parseInt(i)+1,
        })


4. Extract useful information from the candidates

    /**
     * 
     * the returned object will look like this:
     *      t_min:
     *      t_max:
     *      t_sub:
     *      t_delta:
     *      t_min_cycle:
     *     t_min_note_position:
     *      t_max_cycle:
     *      t_max_note_position:
     *      notes_data:[
     *        {cycle: , period: , note_position: },
     *       {cycle: , period: , note_position: },...]
     *     
     

    FUNCTION extract_useful_information_from_candidates(bound_information, candidates_in_bound)

5. Choose best n candidates (sorted by t_delta???)


*/

function preprocess_data(note_periods_per_note_per_cycle){

    midi_numbers =  Object.keys(note_periods_per_note_per_cycle).sort((a,b)=>a-b)
    note_periods = midi_numbers.map((midi_number)=>note_periods_per_note_per_cycle[midi_number].periods)

    cycles = midi_numbers.map((midi_number)=>note_periods_per_note_per_cycle[midi_number].cycle_numbers)
    note_names = midi_numbers.map((midi_number)=>note_periods_per_note_per_cycle[midi_number].note_name)
    return {
        midi_numbers:midi_numbers,
        note_periods:note_periods,
        cycles:cycles,
        note_names:note_names
    }
}


/* 

 This function will find the min max bounds,

 consider a table of two columns, each row is period* number_of_row,
 then look through the table and find the minimum distance between two points
 left - right and if negative then increment left, else increment right,
 
 At the end, sort by ratio and get the bounds with lowest differences/middle_point

*/


function find_min_max_bounds(note_periods, cycles){
    /*returns a list of bounds, each bound contains:
                highest_note_cycle: j+1,
            bass_note_cycle:i+1,
            mean: mid_point,
            bass_note_period: bass_periods[i],
            highest_note_period: highest_note_periods[j],
            distance:distance,
            ratio:ratio,
            abs_distance: Math.abs(distance)

            */



    // only consider first and last elements each note_period

    

  
    
    bass_periods = note_periods[0]
    bass_cycles = cycles[0]


    highest_note_periods = note_periods[note_periods.length-1]
    highest_cycles = cycles[cycles.length-1]

    // Key information, ratio is the distance between the two points
    // relative to its middle point.
    // When the ratio is small, it means they are close together. 
    // Dividing by middle point normalizes comparisons between different periods. 


    // by default we assume it is ordered. 
    // Since we are starting from smallest to largest, we insert the same way

    useful_information_of_each_bound_pair = []

    let i=0, j=0
    while (i < bass_periods.length && j< highest_note_periods.length){

        // calculating distance, mid point, ratio
        distance = bass_periods[i] - highest_note_periods[j]
        mid_point = (bass_periods[i] + highest_note_periods[j])/2
        ratio = Math.abs(distance)/mid_point

        useful_information_of_each_bound_pair.push({
            highest_note_cycle: j+1,
            bass_note_cycle:i+1,
            mean: mid_point,
            bass_note_period: bass_periods[i],
            highest_note_period: highest_note_periods[j],
            distance:distance,
            ratio:ratio,
            abs_distance: Math.abs(distance)
        })

        // if distance is less than 0 this means if j increases we will get higher absolute(differences)
        // in our case we are looking for smallest differences, therefore increment i, else increment j

        if(distance <0){
            i++
        }
        else{
            j++
        }

        
        // useful_information_of_each_bound_pair.push({distance:distance, mid_point:mid_point, ratio:ratio})
        
    }


    // sort by ratio, this means normalizing differences and comparing respective to its center. 
    // example, if we compare dif1=0.5, and dif2= 1, we will obviously get 0.5 as smallest difference,
    // even if mean1 is 2, and mean2 is 2.5. if we were to compare using ratio instead, we will get that
    // smallest delta t respective to the t_mean_sub is 1/2.5 instead of 0.5/2. 
    // although... this only works if we want to find smallest delta t's instead smallest tsubs with a delta t.
    
    useful_information_of_each_bound_pair.sort((a, b) => a.ratio-b.ratio)
    return useful_information_of_each_bound_pair

}



/*

    For each bound, we will do a binary search from the complete table of note_periods  (without bass and highest)
    being played, and find the closest pair of notes for each note in between.


    returns a list that contains this information from each note       
        chosen_winners.push({
            cycle: candidate_cycle,
            period: candidate_period,
            difference: candidate_difference,
            note_position:parseInt(i)+1,
        })
        
*/


function binary_search_with_bounds(start_bound_index, end_bound_index, mean, other_note_periods){

    // this will look for the smallest cycle candidates for each note within given bound,
    // and return the smallest pair of cycles for each note.
    
    chosen_winners = []
    for(i in other_note_periods){
        note_periods = other_note_periods[i]


        l = start_bound_index,
        r = end_bound_index
        candidate_cycle = 0
        candidate_difference = Infinity
        candidate_period = Infinity
        while (l<=r){
            mid = Math.floor((l+r)/2)
            difference = mean - note_periods[mid]

            // if this is true, there is a cycle c that t_ic_i is closer to the mean 
            if(candidate_difference> Math.abs(difference)){

                candidate_difference = Math.abs(difference)
                candidate_cycle = mid
                candidate_period = note_periods[mid]
            }
            if(difference<0){
                r = mid-1
            }
            else{
                l = mid+1
            }
            

        }
        chosen_winners.push({
            cycle: candidate_cycle,
            period: candidate_period,
            difference: candidate_difference,
            note_position:parseInt(i)+1,
        })
        
    }
    return chosen_winners

}


//TODO what happens if onlye one note is played?
function extract_useful_information_from_candidates(bound_information, candidates_in_bound){

    // console.log('extracting from candidates',bound_information, candidates_in_bound)
    
    // Here we mix bound_info and the candidates_per_bound
    //Bound information contains:
    /*
                
        abs_distance:  0.00010311388289876641
        bass_note_cycle:  3
        bass_note_period:  0.01146675024653513
        distance:  0.00010311388289876641
        highest_note_cycle:  5
        highest_note_period:  0.011363636363636364
        mean:  0.011415193305085747
        ratio:  0.009033038700520881
    
    */

    // candidates_in_bound is a list that contains
    /*
    
        0:
            cycle:3
            difference:0.0007196981483102022
            note_position:1
            period:0.01213489145339595
        1:
            cycle:3
            difference:0.0012109815166700781
            note_position:2
            period:0.010204211788415669
    */

    object_to_return = {
        notes_data:[]
    }

    t_min_candidate = bound_information.bass_note_period

    t_max_candidate = bound_information.highest_note_period
    t_min_candidate_cycle = bound_information.bass_note_cycle
    t_max_candidate_cycle = bound_information.highest_note_cycle


    //question mark TODO
    t_min_candidate_note_position = 0
    t_max_candidate_note_position = candidates_in_bound.length+1

    object_to_return.notes_data.push({
        cycle:bound_information.bass_note_cycle,
        period:bound_information.bass_note_period,
        note_position:0,

    }) 

    // inserting to notes_data for each note, and finding min max
    for (let i = 0; i < candidates_in_bound.length; i++) {
        note_candidate = candidates_in_bound[i]

        //fixing if there is a new min or max
        if (note_candidate.period<t_min_candidate){
            t_min_candidate = note_candidate.period
            t_min_candidate_cycle = note_candidate.cycle
            t_min_candidate_note_position = note_candidate.note_position
        }
        if (note_candidate.period>t_max_candidate){
            t_max_candidate = note_candidate.period
            t_max_candidate_cycle = note_candidate.cycle
            t_max_candidate_note_position = note_candidate.note_position
        }

        // pushing the note candidate to the notes_data
        object_to_return.notes_data.push({
            cycle:note_candidate.cycle,
            period:note_candidate.period,
            note_position:note_candidate.note_position,
        })
        
    }

    
    object_to_return.notes_data.push({
        cycle:bound_information.highest_note_cycle,
        period:bound_information.highest_note_period,
        note_position:candidates_in_bound.length+1,
    })

    // now with min max, calculate t_sub, t_delta

    t_delta = t_max_candidate - t_min_candidate
    t_sub = (t_max_candidate + t_min_candidate)/2

    object_to_return.t_min = t_min_candidate
    object_to_return.t_max = t_max_candidate
    object_to_return.t_sub = t_sub
    object_to_return.t_delta = t_delta
    object_to_return.t_min_cycle = t_min_candidate_cycle
    object_to_return.t_max_cycle = t_max_candidate_cycle
    object_to_return.t_min_note_position = t_min_candidate_note_position
    object_to_return.t_max_note_position = t_max_candidate_note_position



    //
    /**
     * 
     * the returned object will look like this:
     *      t_min:
     *      t_max:
     *      t_sub:
     *      t_delta:
     *      t_min_cycle:
     *     t_min_note_position:
     *      t_max_cycle:
     *      t_max_note_position:
     *      notes_data:[]
     *     
     */
    return object_to_return
    

}




function manage_stationary_visualization(note_periods_per_note_per_cycle){

    // preprocess data into array of arrays ordered by midi_number
    // console.log('note_periods_per_note_per_cycle', note_periods_per_note_per_cycle)



    preprocessed_data = preprocess_data(note_periods_per_note_per_cycle)
    // console.log('preprocessed data',preprocessed_data)

    
    
    //WHAT HAPPENS IF ONLY ONE NOTE IS PLAYED?????????

    //now that everything is sorted, we can get min, max bounds

    list_of_bounds = find_min_max_bounds(preprocessed_data.note_periods, preprocessed_data.cycles)
    // console.log('list_of_bounds',list_of_bounds)
    

    // this contains n-2 arrays, which notes are from [1,n-1]
    other_note_periods = preprocessed_data.note_periods
    other_note_periods = note_periods.slice(1, other_note_periods.length-1) 

    note_pairs_per_bound = []
    for(i in list_of_bounds){
        
        //bound information is
        /*
            {
                highest_note_cycle: c1,
                bass_note_cycle: cn,
                mean: (t1c1+tncn)/2
                distance: tncn-t1c1
                ratio : difference/mean
                abs_distance: abs(distance)
                highest_period: t1c1
                bass_period: tncn
            }
        */
       bound_information = list_of_bounds[i]

       /*
        start_bound_index : is always less or equal than the ci, where 0<i<n
                            and i is the cycle for the next n array, or n notes
        end_bound_index   : is always more or equal than the ci 

       */
       start_bound_index = bound_information.bass_note_cycle
       end_bound_index   = bound_information.highest_note_cycle
       mean              = bound_information.mean
       ratio             = bound_information.ratio

       // per min max bound, get smallest pair of n notes. 
       candidates_in_bound = binary_search_with_bounds(start_bound_index, end_bound_index, mean, other_note_periods )
       note_pairs_in_bound = extract_useful_information_from_candidates(bound_information, candidates_in_bound,)

       note_pairs_per_bound.push(note_pairs_in_bound)
    }
    // console.log('nppb',note_pairs_per_bound)

    // now here we get top n candidates for tension, 
    // and we will use this to create the bar graph.
    // these n notes will be sorted by differece



    //TODO: Sort by variable
    note_pairs_per_bound.sort((a,b)=>a.t_delta-b.t_delta)

    // console.log('sorted note pairs per bound', note_pairs_per_bound)


    // now we will get the top n notes, and create the bar graph




    return {
        note_pairs_per_bound:note_pairs_per_bound,
        preprocessed_data:preprocessed_data,
    }
    visualize_stationary_tension(note_pairs_per_bound.slice(0,top_n_notes),preprocessed_data)
    

    




}


    /**
     * 
     * the returned object will look like this:
     *      t_min:
     *      t_max:
     *      t_sub:
     *      t_delta:
     *      t_min_cycle:
     *     t_min_note_position:
     *      t_max_cycle:
     *      t_max_note_position:
     *      notes_data:[]
     *     
     */





function calculate_stationary_tension(){

}
