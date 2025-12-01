import pandas as pd
from math import log2
import numpy as np
from ..dataframe_functions_for_functionality import *
from json import dumps



# Using Science paper Chan, P. Y., Dong, M., & Li, H. (2019).
# The Science of Harmony: A Psychophysical Basis for Perceptual Tensions and Resolutions in Music. 
# Research, 2019. https://doi.org/10.34133/2019/2369041
# 
# We see that they need to calculate f1-f2/avg(f1,f2)




def chan_tension_calculation(note1, note2, note_df, values_of_r_ranges = [(0.95, 1.1),(1.5,2.8)], apply_weights_to_harmonics=False, limit_delta_frequency=False, include_lower_bound=True, frequency_threshold=170):
    """
    Chan Tension Calculation: Paper Citation: C(Δf/f) referring to the number of interharmonic 
                                modulations that fall within the central region of dissonance
                                region, i iterates through all interharmonic modulations on
                                the plot, n is the total number of modulations considered,
                                Δf1 and f2 refer to the pair of Δf and f that describe the i-th
                                interharmonic modulation, respectively, and r_lower and r_upper
                                define the lower and upper boundaries of the region on the
                                interharmonic plot, respectively.
    Our interpretation of their method: 
                                They have a plot (see Figure 7 in paper) where they plot
                                the difference of two harmonics over their average, and then
                                count how many points fall within certain ranges (dissonant ranges).
                                they define those dissonant ranges as r_upper and r_lower, 
                                and use the default values we define, 0.95, 1.1 and 1.5, 2.8 (see evaluation),
                                sum the two together to calculate interharmonic tension.
                                N is the total number of modulations considered, but they do not specify 
                                how many modulations should be considered.
                                        
    note1, note2: strings that contain the two intervals that are going to be compared. i.E. 'C4', 'E4'
    note_df: dataframe that contains the harmonics of all notes. Created with create_harmonic_dataframe()
    number_of_harmonics: number of harmonics to consider, value is note_df rows.
    values_of_r_ranges: For Chans paper, the default values are [(0.95, 1.1),(1.5,2.8)]
                        these are the dissonance regions they use in their paper.
                        We can modify them to see how it affects the results.
                        List of r_bounds should be in the form of tuples of (r_lower, r_upper)
    no_weights: Boolean, if True, does not apply weights to the harmonics. Weights are defined in
                my approach paper as 1/n, where n is the harmonic number. therefore the first harmonic
                has weight 1, the second 1/2, the third 1/3 and so on, so that the position of harmonic matters.     
    limit_delta_frequency: Boolean, if True, does not apply a limit to the difference between harmonics.
              In Chans paper, the plot caps at 170Hz difference, but they do not consider this limit 
              in their equations or their evaluations. 
    returns: list of counts of interharmonic modulations that fall within the dissonance ranges defined
             by values_of_r_ranges.   
    """
    # first we calculate all the differences between harmonics of note1 and note2
    # then we calculate the average of each pair of harmonics

    differences_of_fs = pd.DataFrame()
    avg_of_fs = pd.DataFrame()

    # N is the total number of modulations considered, from i to n. 
    
    for i in range(0, len(note_df[note1])):
        differences_of_fs[str(i)+'th']=  abs(note_df[note1][i] -note_df[note2]) 
        avg_of_fs[str(i)+'th'] = abs((note_df[note1][i] + note_df[note2])/2)

    #  filtramos por threshold de batimientos??

    if limit_delta_frequency is True:
        differences_of_fs =  differences_of_fs[differences_of_fs <= frequency_threshold]

    # print(differences_of_fs)
    # print(avg_of_fs)

    # return differences_of_fs
    # print(differences_of_fs)
    ratio_df = differences_of_fs/avg_of_fs

    # lets see sum for each upper bound
    dif_ranges = values_of_r_ranges
    ranges_list = []
    offsets= (0.1,0.1)

    # Iterating through dissonance ranges
    ## this is to compute all the modulations that fall higher than lower bound
    ## and then all of the modulations that call lower than the upper bound
    ## and then we to an and operation to get all the modulations that falle between
    ## those two bounds, which is like the paper suggests. 
    ## (see equation 10 in paper)
    ## summ all modulations that fall in 2^(r_lower/12)-1 < (f1-f2)/avg(f1,f2) < 2^(r_upper/12)-1
    for i in range(0,len(dif_ranges)):

        r_bound = dif_ranges[i]

        if include_lower_bound is False:
            lower_bound = ratio_df > 2**((r_bound[0])/12)-1
        else:
            lower_bound = ratio_df >= 2**((r_bound[0])/12)-1
        upper_bound = ratio_df < 2**((r_bound[1])/12)-1


        ## if no weights is true, then all weights are 1 and we only
        #  sum the amount of modulations that fall in those boundaries. 
        # We create an array of weights that is the same length as the 
        # number of modulations that fall in those boundaries
        if(apply_weights_to_harmonics is False):
            weights = np.array([1] *len((lower_bound & upper_bound).sum()))
        
        ## else, we apply weights to the harmonics, where the weight is 1/n
        # where n is the harmonic number. therefore the first harmonic
        # has weight 1, the second 1/2, the third 1/3 and so on, so that the position of harmonic matters.

        else:

             weights = np.array([len((lower_bound & upper_bound).sum())] *len((lower_bound & upper_bound).sum())) / ((np.array(range(1, len((lower_bound & upper_bound).sum())+1)))*10)
      
        #  this sum() yields amount of modulations in each harmonic
        harmonic_modulations = (lower_bound & upper_bound).sum()

      
        # then we apply the weights for each of the modulations 
        weighted = harmonic_modulations *weights
        
        
    


        
       
        
        

        #for purposes, the second.sum() calculates total modulation in each boundary within that interval

        
        ranges_list.append(weighted.sum())

    return ranges_list


## Attempt to print tension list for all intervals in an octave

def tension_df_print(tension_list, values_of_r_ranges):

    ranges_dataframe = pd.DataFrame()
    ranges_dataframe['interval']=['U', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', '8v']
    df_ten = pd.DataFrame(tension_list)
    # print("printing ", df_ten)
    for i in range(0,len(values_of_r_ranges)):
        r_bound = values_of_r_ranges[i]
        ranges_dataframe[f'2**({r_bound[0]}/12)<ratio<2**{r_bound[1]}/12'] = df_ten[i//2]

    return ranges_dataframe.T


def modified_chan_tension_calculation(note1, 
                                      note2,
                                      note_df,
                                      values_of_r_ranges = [(0.95, 1.1),(1.5,2.8)],
                                      weights_for_regions={
                                            'red_region': 1,
                                            'orange_region': 0.70,
                                            'yellow_region': 0,
                                            'green_region': 0
                                        },
                                      apply_weights_to_individual_harmonic=False,
                                      
                                        limit_delta_frequency=False, 
                                        frequency_threshold=170,
                                        include_lower_bound=True,
                                        tension_list_for_each_range_in_two_notes = []):
    """
    ## Modified Chan Tension Calculation: 
    This is a modified version of Chan Tension Calculation. We here consider varios r_ranges, 
    and computed weights for each dissonance region, where we consider the most dissonant regions
    which are red, to have a higher weight, and the less dissonant regions, which are yellow, to have a lower weight.
    (see Figure 7)
    
    We then give weights to each dissonance region depending on values given as parameters.
    We then sum all the modulations that fall within each dissonance region, multiply them by their respective weights,
    and then sum all the weighted modulations to get a final tension value.

    Default weights are {
        'red_region': 1,
        'orange_region': 0.70,
        'yellow_region': 0,
        'green_region': 0
    }

    Weights can be modified by changing the values in the weights dictionary, as a parameter.

    note1, note2: strings that contain the two intervals that are going to be compared. i.E. 'C4', 'E4'

    note_df: dataframe that contains the harmonics of all notes. Created with create_harmonic_dataframe()

    number_of_harmonics: number of harmonics to consider, value is note_df rows.

    values_of_r_ranges: For Chans paper, the default values are [(0.95, 1.1),(1.5,2.8)]
                        these are the dissonance regions they use in their paper.
                        We can modify them to see how it affects the results.
                        List of r_bounds should be in the form of tuples of (r_lower, r_upper)

    apply_weights_to_individual_harmonic: Boolean, if False, does not apply weights to the harmonics. Weights are defined in
                my approach paper as 1/n, where n is the harmonic number. therefore the first harmonic
                has weight 1, the second 1/2, the third 1/3 and so on, so that the position of harmonic matters.

    limit_delta_frequency: Boolean, if True, does not apply a limit to the difference between harmonics.
              In Chans paper, the plot caps at 170Hz difference, but they do not consider this limit 
              in their equations or their evaluations. 

    ## Returns: Sum of normalized weighted values, All weighted points that fall in each dissonance region,
                All points that fall in each dissonance region before weighting, 
                Weights applied to each dissonance region.
    """

    if( len(tension_list_for_each_range_in_two_notes)==0):
        tension_list_for_each_range_in_two_notes = chan_tension_calculation(note1, 
                                                                        note2, 
                                                                        note_df, 
                                                                        values_of_r_ranges, 
                                                                        apply_weights_to_harmonics=apply_weights_to_individual_harmonic, 
                                                                        limit_delta_frequency=limit_delta_frequency,
                                                                        frequency_threshold=frequency_threshold, 
                                                                        include_lower_bound=include_lower_bound)

    weights_for_each_index_in_tense_array = []
    # Iterating through dissonance ranges
    # based on hardcoding regions and looking at figure 7
    ## this is to compute the regions of all the modulations 
    for i in range(0,len(values_of_r_ranges)):
        r_bound = values_of_r_ranges[i]
        r_lower = r_bound[0]
        r_upper = r_bound[1]

        ## has no effect and no points found
        if r_lower >= 8.5:
            weights_for_each_index_in_tense_array.append(0)

        #  2^7.5  <= f < 2^8.5    === falls in orange region
        elif r_lower >= 7.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['orange_region'])

        # 2^6.5  <= f < 2^7.5    === falls in yellow region  
        elif r_lower >= 6.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['yellow_region'])
        # 2^5.5  <= f < 2^6.5    === falls in yellow region
        elif r_lower >= 5.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['yellow_region'])

        # 2^4.5   <= f < 2^5.5   === falls in red region
        elif r_lower >= 4.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['red_region'])

        # 2^3.5   <= f < 2^4.5   === falls in yellow region
        elif r_lower >= 3.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['yellow_region'])

        # 2^2.5   <= f < 2^3.5   === falls in orange region
        elif r_lower >= 2.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['orange_region'])

        # 2^1.5   <= f < 2^2.5   === falls in red region
        elif r_lower >= 1.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['red_region'])

        # 2^0.5   <= f < 2^1.5   === falls in red region
        elif r_lower >= 0.5:
            weights_for_each_index_in_tense_array.append(weights_for_regions['red_region'])
        
        # 2^0.25  <= f < 2^0.5   === orange region
        elif r_lower >= 0.25:
            weights_for_each_index_in_tense_array.append(weights_for_regions['orange_region'])

        # 2^0.125 <= f < 2^0.25  === orange region
        elif r_lower >= 0.125:
            weights_for_each_index_in_tense_array.append(weights_for_regions['orange_region'])

        else:
        # 2^0     <= f < 2^0.125 === green region
            weights_for_each_index_in_tense_array.append(weights_for_regions['green_region'])


    # now that we have the weights for each region, we multiply them by the tension list
    tension_list_weighted = [tension_list_for_each_range_in_two_notes[i] * weights_for_each_index_in_tense_array[i] for i in range(0,len(tension_list_for_each_range_in_two_notes))]

    # finally we sum all the weighted tensions to get a final tension value
    final_tension_value = sum(tension_list_weighted)

    # we also give a normalized tension value, where we divide
    # the weighted values by the total amount of modulations
    # the closer to 1, the more dissonant the interval is
    # the closer to 0, the more consonant the interval is

    normalized_tension_value = final_tension_value / sum(tension_list_for_each_range_in_two_notes) if sum(tension_list_for_each_range_in_two_notes) != 0 else 0

    return normalized_tension_value,tension_list_weighted, tension_list_for_each_range_in_two_notes,weights_for_each_index_in_tense_array

        

    
    
def calculate_tension_score2(list_of_values):
    consonant_ratio = 0
    somewhat_dis = 1
    moreDis = 0.7
    Dissonant =1

    # # so we say that the first index is consonant, and the [6]
    # #consonancy 
    # tension_score = consonant_ratio *(list_of_values[0] )
    # #somewhat_dis
    # tension_score+= (somewhat_dis * (list_of_values[6]+ list_of_values[8])+  list_of_values[9]) #+ list_of_values[6] + list_of_values[8]))
    # # moreDis
    tension_score= (moreDis *(list_of_values[1] +list_of_values[2]+ list_of_values[5]+list_of_values[10]))#+list_of_values[10] +list_of_values[5]))
    tension_score += (Dissonant *(list_of_values[3]+ list_of_values[4]+list_of_values[7]))
    
    tension_score /= sum(list_of_values)
    return tension_score


def generalized_chan_method_calculation(note_array_to_compute, note_df, distributive=False, values_of_r_ranges = [(0.95, 1.1),(1.5,2.8)], apply_weights_to_harmonics=False, limit_delta_frequency=False, include_lower_bound=True, frequency_threshold=170):
    """
    This method is a generalized version of chans calculation that works for  more than one note
    For example, if this method recieves ['C4','E4','G4'], it will compute the tension
    usinginterharmonic modulation. <br>
    How it computes it depends on the distributive parameter. <br>
    if it is distributive it computes C4, with E4, then C4 with G4, and E4 with G4. 
    If it is not distributive, it only compares with the first note. 
    

    This case, they do not consider total modulations found, only modulations found in r ranges<br>
    ### Returns, list of lists, where each list represent a modulation of two notes at every indexed region
    
    """
    
    ## we create a list that hold the information for each region
    ## each index of this list isa permutation of thenotes. Example, if
    ## c4 e4 g4, and distributive is on, the returned object will be an array of arrays. 
    ## each array inside contains modulations for each r_range. 
    tension_list_for_combinations_per_region =[]

    # print("we are in generalized chan method calculation")
    # print(f"note_array_to_compute: {note_array_to_compute}")

    if distributive:
        for note_index in range(0,len(note_array_to_compute)-1):
            for compared_note in range(1,len(note_array_to_compute)):
                primary_note = note_array_to_compute[note_index]
                secondary_note = note_array_to_compute[compared_note]
                
                tension_list_for_combinations_per_region.append(chan_tension_calculation(note1=primary_note,note2=secondary_note,note_df=note_df, 
                                                                                         values_of_r_ranges=values_of_r_ranges,
                                                                                         apply_weights_to_harmonics=apply_weights_to_harmonics,
                                                                                         limit_delta_frequency=limit_delta_frequency,
                                                                                         include_lower_bound=include_lower_bound,
                                                                                         frequency_threshold=frequency_threshold))
    else:
        for compared_note in range(0,len(note_array_to_compute)-1):
            primary_note = note_array_to_compute[compared_note]
            secondary_note = note_array_to_compute[compared_note+1]
            tension_list_for_combinations_per_region.append(chan_tension_calculation(note1=primary_note,note2=secondary_note,note_df=note_df, 
                                                                                        values_of_r_ranges=values_of_r_ranges,
                                                                                        apply_weights_to_harmonics=apply_weights_to_harmonics,
                                                                                        limit_delta_frequency=limit_delta_frequency,
                                                                                        include_lower_bound=include_lower_bound,
                                                                                        frequency_threshold=frequency_threshold))

    # print(tension_list_for_combinations_per_region)      
    return tension_list_for_combinations_per_region


def normalized_interharmonic_modulations_pipeline(note_combinations_array,
                                                  chord_labels_array,
                                                  harmonics_considered=10,
                                                  values_of_r_ranges = [(0.95, 1.1),(1.5,2.8)],
                                                  apply_weights_to_individual_harmonic=False,
                                                  limit_delta_frequency=False,
                                                  frequency_threshold=170,
                                                  include_lower_bound=True,
                                                  distributive=False,
                                                  apply_weights_to_region=False,
                                                  weights_for_regions={
                                                        'red_region': 1,
                                                        'orange_region': 0.70,
                                                        'yellow_region': 0,
                                                        'green_region': 0
                                                    },
                                                    ):
    """
    This is the final version of the evaluation step at Chan's paper. <br>
    This should compute T_delta_f|f normalized, with different methods
    Exampleof usage. <br>
    Define array of combinations of notes [['G4','B4','D5'],['B4','D5','F#5']]<br>
    Input parameters for different methods <br>
    <b>note_combinations_array</b>: Array of arrays, where each array contains a combination of notes to analyze <br>
    <b>chord_labels_array</b>: Array of strings, where each string is the label of the corresponding combination of notes <br>
    <b>harmonics_considered</b>: Number of harmonics to consider in the analysis (default: 10) <br>
    <b>values_of_r_ranges</b>: List of tuples representing the ranges of r values to consider (default: [(0.95, 1.1),(1.5,2.8)]) <br>
    <b>apply_weights_to_individual_harmonic</b>: Boolean indicating whether to apply weights to the harmonics. if False, does not apply weights to the harmonics. Weights are defined in
                my approach paper as 1/n, where n is the harmonic number. therefore the first harmonic
                has weight 1, the second 1/2, the third 1/3 and so on, so that the position of harmonic matters. (default: False) <br>
    <b>limit_delta_frequency</b>: Boolean indicating whether to apply a frequency limit in delta. If we want to consider
     all delta f in harmonics (default: False) <br>
    <b>frequency_threshold</b>: delta Frequency limit or threshold, only used if limit_delta_frequency is False (default: None) <br>
    <b>include_lower_bound</b>: Boolean indicating whether to include the lower bound in the analysis (default: False) <br>
    <b>distributive</b>: Boolean indicating whether to use distributive method, i.e. if all note combinations should be considered (TRUE), or only the first note against the rest (FALSE) (default: False) <br>
    <b>apply_weights_to_region</b>: Boolean indicating whether to apply weights to the dissonance regions (default: False) <br>
    <b>weights_for_regions</b>: Dictionary containing weights for each dissonance region (default: {'red_region': 1, 'orange_region': 0.70, 'yellow_region': 0, 'green_region': 0}) <br>

    ## Returns, Dataframe with normalized tension values, raw values per combination, weighted values per region if applied, note_combinations, raw_tension_score_summed

    """
    # Create harmonic dataframe
    df = create_harmonic_dataframe(harmonics_considered=harmonics_considered)

    # Calculate tension for each combination of notes
    ## For each combination of notes,  it will yieldan array of arrays
    ## where each array inside contains modulations for each r_range.

    big_dataframe_with_all_combinations = pd.DataFrame()

    for note_combination in note_combinations_array:
        # print(note_combination)

        # Creating dataframe for each combination to later compute normalized tension score for 
        # stationary values
        temp_df = pd.DataFrame()
        temp_df['note_combination'] = [','.join(note_combination)]
        temp_df['chord_label'] = chord_labels_array[note_combinations_array.index(note_combination)]
        # print(temp_df)
 
       

        ## This is total of blue dots of modulations per region considered
        array_of_modulations_per_region =  generalized_chan_method_calculation(note_array_to_compute=note_combination,
                                                                               note_df=df,
                                                                               distributive=distributive,
                                                                               values_of_r_ranges=values_of_r_ranges,
                                                                               apply_weights_to_harmonics=apply_weights_to_individual_harmonic,
                                                                               limit_delta_frequency=limit_delta_frequency,
                                                                               include_lower_bound=include_lower_bound,
                                                                               frequency_threshold=frequency_threshold)
        # print("array_of_modulations_per_region", array_of_modulations_per_region)

        temp_df['raw_values_per_combination'] = [array_of_modulations_per_region]

        if apply_weights_to_region is True:

            ## This one will store (the total blue dots of figure 7 per region) * ( weight of region) per combination
            ## This is is a list of lists, where each list is a combination of notes
            ## and each index of the list is the weighted modulations per region

            weighted_modulations_per_region_in_note_combinations = []

            ## This one will store the final normalized tension value per combination
            ## which is computed from the previous list, it is sumof all weighted modulations, divided by the total amount of modulations per permutation
            weighted_modulation_sum_per_region_per_combination_normalized_tension_value=[]

            for modulation_array in array_of_modulations_per_region:
                normalized_tension_value, tension_list_weighted, tension_list_for_each_range_in_two_notes, weights_for_each_index_in_tense_array = modified_chan_tension_calculation(note1=note_combination[0],
                                                                                                                                                                        note2=note_combination[1],
                                                                                                                                                                        note_df=df,
                                                                                                                                                                        values_of_r_ranges=values_of_r_ranges,
                                                                                                                                                                        weights_for_regions=weights_for_regions,
                                                                                                                                                                        apply_weights_to_individual_harmonic=apply_weights_to_individual_harmonic,
                                                                                                                                                                        limit_delta_frequency=limit_delta_frequency,
                                                                                                                                                                        frequency_threshold=frequency_threshold,
                                                                                                                                                                        include_lower_bound=include_lower_bound,
                                                                                                                                                                        tension_list_for_each_range_in_two_notes=modulation_array)
                weighted_modulation_sum_per_region_per_combination_normalized_tension_value.append( normalized_tension_value if not np.isnan(normalized_tension_value) else 0)
                weighted_modulations_per_region_in_note_combinations.append(tension_list_weighted)

            ## now we compute the raw tension score, using the sum of the combinations
            ## of normalized tension values per region
            ## so if triad, we have the sum of 3 normalized tension values (if distributive is True)
            raw_tension_score_for_combination_using_weighted_normalized_value = sum(weighted_modulation_sum_per_region_per_combination_normalized_tension_value)
            
            ## This one computes the raw tension score using the sum of all weighted modulations
            ## so each (the total blue dots of figure 7 per region) * ( weight of region) per combination is then summed
            raw_tension_score_for_combination_using_weighted_modulations_no_norm = sum([sum(x) for x in weighted_modulations_per_region_in_note_combinations])
            
        
        else:
            weighted_per_region_normalized_tension_value = None
            weighted_modulations_per_region = None
            raw_tension_score_for_combination_using_weighted_normalized_value= None
            raw_tension_score_for_combination_using_weighted_modulations_no_norm = None

        ## This one computes the raw tension score using the sum of all modulations found per combination
        raw_tension_score_for_combination_summing_modulations = sum([sum(x) for x in array_of_modulations_per_region])
        # print("raw values per combination", raw_values_per_combination)


        temp_df['weighted_modulations_per_region_in_note_combinations'] = [weighted_modulations_per_region_in_note_combinations] if apply_weights_to_region is True else None
        temp_df['weighted_sum_per_region_normalized_tension_value'] = [weighted_modulation_sum_per_region_per_combination_normalized_tension_value] if apply_weights_to_region is True else None
        temp_df['raw_t_score_summed_only_modulations'] = [raw_tension_score_for_combination_summing_modulations]
        temp_df['raw_t_score_summed_using_weighted_normalized_value'] = [raw_tension_score_for_combination_using_weighted_normalized_value] if apply_weights_to_region is True else None
        temp_df['raw_t_score_summed_using_weighted_modulations_no_norm'] = [raw_tension_score_for_combination_using_weighted_modulations_no_norm] if apply_weights_to_region is True else None
        big_dataframe_with_all_combinations = pd.concat([big_dataframe_with_all_combinations, temp_df], ignore_index=True)
    
    #  after this, we need to compute normalized tension value, so from raw values for each combination
    # we do this by getting minimum raw value from category, and maximum raw value from category
    # and then we normalize the values between 0 and 1
    # normalized_value = (value - min) / (max - min)

    

    ## getting minimum value from raw values only using raw value from modulations

    minimum_value = big_dataframe_with_all_combinations['raw_t_score_summed_only_modulations'].min()
    maximum_value = big_dataframe_with_all_combinations['raw_t_score_summed_only_modulations'].max()

    # now lets  sort big dataframe  with raw_t_score_summed_only, so when we apply the formula
    ## using lists, we can just assign. 
    big_dataframe_with_all_combinations = big_dataframe_with_all_combinations.sort_values('raw_t_score_summed_only_modulations')

    raw_values = big_dataframe_with_all_combinations['raw_t_score_summed_only_modulations']


# if this if is true, it means either an error, or that the values were so small that no modulation was found
    if (maximum_value - minimum_value != 0):
        # normalizing values
        normed_vals = []
        for r_v in raw_values:
            # print(r_v)
            norm_val = ((r_v-minimum_value)/(maximum_value-minimum_value)  )
            normed_vals.append(norm_val)
    else:
        normed_vals = [0] * len(raw_values)

    big_dataframe_with_all_combinations['normed_values_only_modulations']=normed_vals

    if apply_weights_to_region is True:

        ## apply same mechanic for weighted modulations, and normed weighted sum

        min_val = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_normalized_value'].min()
        max_val = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_normalized_value'].max()

        normed_vals = []
        big_dataframe_with_all_combinations = big_dataframe_with_all_combinations.sort_values('raw_t_score_summed_using_weighted_normalized_value')

        raw_values = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_normalized_value']
        
        # if this if is true, it means either an error, or that the values were so small that no modulation was found
        if (maximum_value - minimum_value != 0):
            for r_v in raw_values:
                norm_val = (r_v-min_val)/(max_val-min_val)
                normed_vals.append(norm_val)
        else:
            normed_vals = [0] * len(raw_values)
        
        big_dataframe_with_all_combinations['normed_values_normed_weighted_modulations'] = normed_vals


        ## now with  raw_t_score_summed_using_weighted_modulations_no_norm
        min_val = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_modulations_no_norm'].min()
        max_val = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_modulations_no_norm'].max()

        normed_vals = []
        big_dataframe_with_all_combinations = big_dataframe_with_all_combinations.sort_values('raw_t_score_summed_using_weighted_modulations_no_norm')

        raw_values = big_dataframe_with_all_combinations['raw_t_score_summed_using_weighted_modulations_no_norm']
        
        
        # if this if is true, it means either an error, or that the values were so small that no modulation was found
        if (maximum_value - minimum_value != 0):
            for r_v in raw_values:
                norm_val = (r_v-min_val)/(max_val-min_val)
                normed_vals.append(norm_val)

        else:
            normed_vals = [0] * len(raw_values)


        big_dataframe_with_all_combinations['normed_values_weighted_modulations_only'] = normed_vals

        


    else:
        big_dataframe_with_all_combinations['normed_values_weighted_modulations_only'] = None
        big_dataframe_with_all_combinations['normed_values_normed_weighted_modulations'] =  None

    return big_dataframe_with_all_combinations

        

        
    


normed_values_columns = ['normed_values_only_modulations','normed_values_weighted_modulations_only','normed_values_normed_weighted_modulations']


def pipeline_for_interharmonic_normalized_tension_scores(note_combinations_array, 
                                                         chord_labels_array, 
                                                         r_ranges=[[(0.95, 1.1), (1.5, 2.8)]],
                                                         r_range_names=['Chan\'s Vanilla'], 
                                                         distributive=[True, False],
                                                         weights_for_regions={
                                                            'red_region': 1,
                                                            'orange_region': 0.7,
                                                            'yellow_region': 0,
                                                            'green_region': 0
                                                        },
                                                         file_path='./overall_interharmonic_normalized_tension_scores_all_methods.csv'):
    """
    This function is to compute the different methods for interharmonic modulations
    and save them in a csv file. <br>
    If you use intervals, no distributive will be used. 

    Description of parameters: <br>
    note_combinations_array: Array of arrays, where each array contains a combination of notes to analyze <br>
    chord_labels_array: Array of strings, where each string is the label of the corresponding combination of notes <br>
    r_ranges: List of lists of tuples representing the ranges of r values to consider for each method:<br>
    \t Default: [[(0.95, 1.1), (1.5, 2.8)]] for Chan method only, or add other list of tuples like [(0.25, 0.5), (0.5, 1.5), (1.5, 2.5)] <br>
    r_range_names: List of strings representing the names of the methods corresponding to each r_ranges list.<br>
    \t Default: ["Chan's Vanilla"] <br>
    distributive: List of booleans indicating whether to use distributive method for each method in r_ranges.<br>
    \t Default: [True, False] <br>
    weights_for_regions: Dictionary containing weights for each dissonance region (default: {'red_region': 1, 'orange_region': 0.70, 'yellow_region': 0, 'green_region': 0}) <br>
    file_path: String representing the path to save the resulting CSV file.<br>
    
    """


        # defining number of harmonics to consider
    harmonics_considered = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

    #define ranges for r_lower, r_upper
    # values_of_r_ranges = [0.0,0.125,0.25,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]
    # # values_of_r_ranges = [0.25,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]


    # double_r_ranges = [(values_of_r_ranges[i], values_of_r_ranges[i+1]) for i in range(len(values_of_r_ranges)-1)]

    # # Chan's method vanilla
    # r_ranges = [(0.95, 1.1), (1.5, 2.8)]

    # defining caps
    # caps = [0,170,80]
    caps = [0]


    # defining if we want weights for each harmonic
    weights_on_harmonic =[True, False]

    # defining if we want weights for each region
    weights_on_region = [True, False]

    ## biggest df with all methods: with raw values
    biggest_df = pd.DataFrame()

    process_string = 'triads'

    if(len(note_combinations_array[0])==2):
        print('Now processing intervals')
        process_string= 'intervals'
        distributive = [True]


    ## df for correlation with method
    corr_df = pd.DataFrame()
    for harmonics in harmonics_considered:
        print(f'Now processing {harmonics} harmonics')



        ## Now loop for each array of ranges

        for r_bound_arr, r_range_name in zip(r_ranges, r_range_names):

            print(f'Now processing {r_bound_arr} with ranges {r_range_name}')



        
        

            # loop for each cap
            for cap in caps:
                for distributive_option in distributive:

                    ## if theres more than two tuples of ranges, then its experimental method
                    if len(r_bound_arr)==2:

                        df_for_method = normalized_interharmonic_modulations_pipeline(
                            note_combinations_array=note_combinations_array,
                            chord_labels_array=chord_labels_array,
                            harmonics_considered=harmonics,
                            values_of_r_ranges=r_bound_arr,
                            
                            apply_weights_to_individual_harmonic=False,
                            limit_delta_frequency=True if cap != 0 else False,
                            frequency_threshold=cap,
                            distributive=distributive_option,
                            apply_weights_to_region=False,
                            weights_for_regions=weights_for_regions,
                        )
                        df_for_method['method'] = f"Chan's method Vanilla"
                        df_for_method['r_ranges_used'] = json.dumps(r_bound_arr)
                        df_for_method['r_names_used'] = r_range_name
                        df_for_method['distributive'] = distributive_option
                        df_for_method['harmonics_considered'] = harmonics
                        df_for_method['weights_on_harmonics'] = False
                        df_for_method['weights_on_regions'] = False
                        df_for_method['weights_for_regions'] = None
                        
                        biggest_df = pd.concat([biggest_df, df_for_method], ignore_index=True)
                    
                    else:

                        ## Now loop if weights
                        for weights_harmonic in weights_on_harmonic:
                            for weights_region in weights_on_region:
                                df_for_method = normalized_interharmonic_modulations_pipeline(
                                    note_combinations_array=note_combinations_array,
                                    chord_labels_array=chord_labels_array,
                                    harmonics_considered=harmonics,
                                    values_of_r_ranges=r_bound_arr,
                                    
                                    apply_weights_to_individual_harmonic=weights_harmonic,
                                    limit_delta_frequency=True if cap != 0 else False,
                                    frequency_threshold=cap,
                                    distributive=distributive_option,
                                    apply_weights_to_region=weights_region,
                                    weights_for_regions=weights_for_regions)
                                method_name = f"Experimental_methods "
                                df_for_method['method'] = method_name
                                df_for_method['r_ranges_used'] = json.dumps(r_bound_arr)
                                df_for_method['r_names_used'] = r_range_name
                                df_for_method['distributive'] = distributive_option

                                df_for_method['harmonics_considered'] = harmonics
                                df_for_method['weights_on_harmonics'] = weights_harmonic
                                df_for_method['weights_on_regions'] = weights_region
                                df_for_method['weights_for_regions'] = str(weights_for_regions) if weights_region is True else None
                                biggest_df = pd.concat([biggest_df, df_for_method], ignore_index=True)

    biggest_df.to_csv(file_path, index=False)
    return biggest_df
            

            
    





def main():

    # Example usage
    # Create harmonic dataframe

    df = create_harmonic_dataframe(harmonics_considered=10)

    # Define notes to analyze
    notes_to_analyze = ['G3','G#3','A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4','G4']

    #define ranges for r_lower, r_upper
    values_of_r_ranges = [(0.95, 1.1),(1.5,2.8)]
    
    # Parameters for chan_tension_calculation
    no_weights = True
    limit_delta_frequency = True
    include_lower_bound = False

    tension_list =[chan_tension_calculation('G3',note, df, values_of_r_ranges,apply_weights_to_harmonics=no_weights,limit_delta_frequency=limit_delta_frequency,include_lower_bound=include_lower_bound) for note in notes_to_analyze]
    print(tension_df_print(tension_list, values_of_r_ranges))

# main()
    

