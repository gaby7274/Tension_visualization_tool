


// Recieves a dictionary where each key is the note, and the value 
// is an object with hertz_values (array of harmonics in hertz), note_name, midi_number
function interharmonic_tension_pipeline(notes,gt=false,note_combination=null){


    //reset all global variables
    data_to_plot_interharmonic = []
    raw_modulations_per_region = []
    harmonics_with_weights_per_region = []
    modulations_with_region_weights = []
    final_tension_score_per_note_combination = []

    //This pipeline 
    console.log('note_harmonics', notes)


    // need to go through each pair

    // notes = Object.keys(note_harmonics)

    // let note_combination=null
    let note_combination_rev=null
    let modulated_dictionaries = null

    for(let i=0; i<notes.length; i++){
        for(let j=i+1; j<notes.length; j++){

            //for each note combination, assign a unique id
            // for plotting purposes
            if(gt==false){
                note_combination= (parseInt(notes[i].midi_number)%12).toString() + '_' + (parseInt(notes[j].midi_number)%12).toString()
                note_combination_rev= (parseInt(notes[j].midi_number)%12).toString() + '_' + (parseInt(notes[i].midi_number)%12).toString()
            }
            else{
                // let note_combination=null;
                note_combination_rev=null;
            }

            // after the two notes are taken, go through the interharmonic modulation

            modulated_dictionaries = counting_interharmonic_modulations_for_each_region(notes[i], notes[j],note_combination,note_combination_rev, gt)

            //after getting combination, we should store tension for said cmobination
            curr_raw_modulations = modulated_dictionaries.raw_modulations
            curr_weighted_harmonics = modulated_dictionaries.weighted_harmonics
            curr_modulations_with_region_weights = modulated_dictionaries.modulations_with_region_weights

            // now compute tension for said interval
            compute_tension_score_combination(notes[i], notes[j],note_combination,note_combination_rev, curr_raw_modulations, curr_weighted_harmonics, curr_modulations_with_region_weights, gt)

        }
    }

    // after going through each combination of notes, we compute a final tension score

    compute_final_interharmonic_tension_score(gt,note_combination)




}


function compute_tension_score_combination(note1, note2,note_combination,note_combination_rev, curr_raw_modulations, curr_weighted_harmonics, curr_modulations_with_region_weights, gt=false){

    //compute tension for said note_combination

    let total_raw_tension =0

    //currently, just sum modulation_with_region_Weights
    //Should be function that depends on user parameters
    for(let i=0; i<curr_modulations_with_region_weights.length; i++){
        total_raw_tension += parseInt(curr_modulations_with_region_weights[i])
    }

    if(gt==false){

        //get normed value by getting max from ground_truth_intervals

        let max_value = Math.max(...ground_truth_intervals.map(item => item.raw_ihm_tension_score));
        let min_value = Math.min(...ground_truth_intervals.map(item => item.raw_ihm_tension_score));

        let normed_tension = (total_raw_tension - min_value) / (max_value - min_value)
        final_tension_score_per_note_combination.push({
            note_combination: note_combination,
            note_combination_rev: note_combination_rev,
            note1: note1.midi_number,
            note2: note2.midi_number,
            note1_name: number_to_note[parseInt(note1.midi_number)%12]+(Math.floor(parseInt(note1.midi_number)/12)-1).toString(),
            note2_name: number_to_note[parseInt(note2.midi_number)%12]+(Math.floor(parseInt(note2.midi_number)/12)-1).toString(),
            total_raw_tension: total_raw_tension,
            normed_tension: normed_tension,
        })
    }

    else{
        // for ground truth, we just store raw tension
        //and update the dictionary of note_combination
        ground_truth_intervals.forEach(function(item){
            if(item.note_combination == note_combination){
                item.raw_ihm_tension_score = total_raw_tension
            }
        })
    }

    // for
}

// Check if value falls in region
function falls_in_region(value, region_start, region_end){

    lower_bound = (2**(region_start/12))-1
    upper_bound = (2**(region_end/12))-1
    return (value >= lower_bound && value < upper_bound)

    
}

// after function call, raw_modulations_per_region and weighted_harmonics_per_region
// will be filled with data for a note combination

/*

modulation arrays will be as follows:
raw_modulations_per_region = [4,0,2] each index is a region, and value is total modulations
weighted_harmonics_per_region = [2.5,0,1.3] each index is a region, and value is total modulations weighted by harmonic position
modulations_with_region_weights = [3.5,0,1.8] each index is a region, and value is total modulations weighted by region weight

//For Chan, the tension is computed by using modulations_with_region_weights
// but only two rgions with weight 1, so the sum is equal to counting only those regions

*/

function counting_interharmonic_modulations_for_each_region(note1_harmonics, note2_harmonics, note_combination,note_combination_rev, gt=false){

    // we create an array for current pair of notes and append it to the global array raw_modulations_per_region

    let current_pair_raw_modulations_per_region = []
    let current_pair_harmonics_with_weights_per_region = []
    let current_pair_weighted_region = []
    let current_bound_to_check=null

    

    
    for(let r=0; r<r_regions_with_weights.length; r++){
        current_bound_to_check = r_regions_with_weights[r]

        region_weight = current_bound_to_check.weight

        // if weight is undefined, we are not considering it for tension score
        
        // if(region_weight == null){
        //     continue
        // }

        let r_low = current_bound_to_check.r_lower
        let r_up = current_bound_to_check.r_upper

        // we are going to count delta f/f_bar ratios that fall in region
        modulations_in_region_bound =0
        weighted_modulation_by_harmonic_position =0
        modulation_with_region_weight =0




        for(let h1_index=0; h1_index<note1_harmonics.hertz_values.length; h1_index++){
            f_1 = note1_harmonics.hertz_values[h1_index]
            for(let h2_index=0; h2_index<note2_harmonics.hertz_values.length; h2_index++){
                f_2 = note2_harmonics.hertz_values[h2_index]

                delta_f = Math.abs(f_2 - f_1)
                f_bar = (f_1 + f_2)/2

                ratio = delta_f / f_bar
                if(falls_in_region(ratio, r_low, r_up)){
                    // we have a modulation in the region that should be plotted

                    // now we add add to raw modulations, and apply weight and add to weighted harmonics
                    if(gt==false){
                    
                    data_to_plot_interharmonic.push({
                        ratio: ratio,
                        harmonic_weight: weight_equation_for_harmonic(h1_index+1)*weight_equation_for_harmonic(h2_index+1),
                        harm_1_index: h1_index+1,
                        harm_2_index: h2_index+1,
                        delta_f: delta_f,
                        average_f: f_bar,
                        note_1: note1_harmonics.note_name,
                        note_2: note2_harmonics.note_name,
                        note_combination: note_combination,
                        note_combination_rev: note_combination_rev,
                    })
                }

                    //if region is counted for tension, then add
                    if(region_weight != null){
                        modulations_in_region_bound +=1
                        weighted_modulation_by_harmonic_position += weight_equation_for_harmonic(h1_index+1) * weight_equation_for_harmonic(h2_index+1)
                        modulation_with_region_weight += region_weight

                    }
                }
            }


        }


        // after finding all harmonic modulations that fall in region, add to global array

        if(modulations_in_region_bound > 0){
            current_pair_raw_modulations_per_region.push(modulations_in_region_bound)
            current_pair_harmonics_with_weights_per_region.push(weighted_modulation_by_harmonic_position) 
            current_pair_weighted_region.push(modulation_with_region_weight) 
        }


    }


    
    raw_modulations_per_region.push(current_pair_raw_modulations_per_region)
    harmonics_with_weights_per_region.push(current_pair_harmonics_with_weights_per_region)
    modulations_with_region_weights.push(current_pair_weighted_region)


    // return current pair for proccessing for each interval
    return {
        raw_modulations: current_pair_raw_modulations_per_region,
        weighted_harmonics: current_pair_harmonics_with_weights_per_region,
        modulations_with_region_weights: current_pair_weighted_region,
    }
}



//compute final tension should depend on parameters 
// specified by user, for now we just sum all modulations with region weights
function compute_final_interharmonic_tension_score(gt=false,note_combination=null){


    //base case, just sum all modulations with region weights

    let total_raw_tension =0
    let total_normed_tension =0

    //array of arrays, each element is an array for a note combination

    for(let i=0; i<modulations_with_region_weights.length; i++){
        let curr_modulations_with_region_weights = modulations_with_region_weights[i]
        for(let j=0; j<curr_modulations_with_region_weights.length; j++){
            total_raw_tension += parseInt(curr_modulations_with_region_weights[j])
        }
    }

    if(gt==false){
        final_ihm_tension_score.raw_tension = total_raw_tension
        

        //now compute normed tension based on current_ground_truth_set

        let max_value = Math.max(...current_ground_truth_set.map(item => item.raw_t_score));
        let min_value = Math.min(...current_ground_truth_set.map(item => item.raw_t_score));

        let normed_tension = (total_raw_tension - min_value) / (max_value - min_value)
        final_ihm_tension_score.normed_tension = normed_tension
        

        //loop through note_harmonic_keys to get note names
        

    }
    else{
        

        if(note_combination.split('_').length ==2){
            // interval
            ground_truth_intervals.forEach(function(item){
                if(item.note_combination == note_combination ){
                    item.raw_ihm_tension_score = total_raw_tension
                }
            })
        }
        else{
        // now for normed tension, get max from current_ground_truth_set
            ground_truth_triads.forEach(function(item){
                if(item.note_combination == note_combination ){
                    item.raw_ihm_tension_score = total_raw_tension
                }
            })
        }
    }

}