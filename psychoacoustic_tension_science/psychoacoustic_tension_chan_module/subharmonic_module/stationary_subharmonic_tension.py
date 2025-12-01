
from ..dataframe_functions_for_functionality import *
import pandas as pd

def finding_min_difference_with_lower_upper_bound(period_df, sort_bounds_by='ratio'):
    '''
    This function will assume that the first and last note are the lower and upper bounds
    Since bass is the first note, and it oscillates less, than the last note

    Algorithm goes as follows:
    loop until last note max index is reached

    then, for each note, we will take the difference between the last note and the bass note
    and divide by the mean of the two notes. We will store, the keys, the division and 
    then sort by division results. 

    each time the difference of last-bass is positive we will increment the bass,
    then when the difference is negative, we will increment the last note
    '''
    notes = period_df.columns
    range_to_consider = len(period_df[notes[0]].values)

    ## bass
    bass =  period_df[notes[0]].values

    last_note = period_df[notes[-1]].values

    ## algorithm
    i, j = 0,0

    ## array to store all dicts info
    ratio_dicts = []


    ## What we do here is, we loop through both arrays and compare
    ## the values in each index. If different is positive, we increment bass index
    ## if difference is negative, we increment last note index

    while i < range_to_consider and j < range_to_consider:
        bass_note = bass[i]
        last_note_value = last_note[j]

        difference = last_note_value - bass_note
        mean = (last_note_value + bass_note) / 2
        ratio = abs(difference/mean)
        ratio_dicts.append({
            'bass': i,
            'last_note': j,
            'difference': difference,
            'mean': mean,
            'ratio': ratio,
            'bass_value':bass_note,
            'last_note_value':last_note_value
        })

        if difference > 0:
            i += 1
        else:
            j += 1

    return pd.DataFrame(sorted(ratio_dicts, key=lambda x: x[sort_bounds_by] ))


def binary_search_with_bounds(period_df,lower_bound,upper_bound,mean_bound):
    

    """
    this binary search goes as follows:
    1. We first take a pivot, which is between lower and upper bound,
    2. we then substract period against mean. 
    3. we compare if that is the lowest, if it is, take pivot as candidate
    4. if positive, we go to right leaf, if negative we go to left
    5. at the end return candidate for each 

    At the end we have candidates that have a minimum difference with mean. i.e. 
    smallest period difference with bass and last note period mean.

    ### Returns two lists of dicts, one with all found differences for each note,
    ### and one with the chosen candidates for each note.
    """

    notes = period_df.columns
    ## only take medium ones
    notes = notes[ 1 : -1]

    chosen_winners = []
    all_found = []
    for note in notes:

        ### here we begin binary loop

        low = lower_bound
        upper = upper_bound
        
        candidate_index = 0
        candidate_difference = 1000
        candidate_value = 10000
        # updated= True
        note_values = period_df[note].values
        # print(note_values)


        complete_note_differences = []

        while low<=upper:
            # updated = False

            middle = (low + upper) // 2

            difference = mean_bound - note_values[middle]

            ## We update candidate if difference is smaller than previous candidate
            if(candidate_difference>abs(difference)):
                candidate_difference =  abs(difference)
                candidate_index = middle
                candidate_value = note_values[middle]
            complete_note_differences.append({
                'index':middle,
                'value': note_values[middle],
                'abs_difference': abs(difference),
                'difference':difference
            })


            ## update middle
            if difference >0:
                low=middle+1
            else:
                upper = middle-1

        #### now we store the necessary information, the chosen one and everything
        all_found.append(
            {'note': note,
             'values':complete_note_differences}
        )
        chosen_winners.append(
            {'note': note,
             'candidate_index': candidate_index,
             'candidate_difference':candidate_difference,
             'candidate_value': candidate_value}
        )
    return all_found,chosen_winners

            
            
        

def choosing_bounds_binary_search(period_df, bounds_df):

    """
    This function takes the period df and bounds df

    For each bound pair, it does a binary search with the remaining notes. 
    Using mean value as the number to substract against (this is to find the minimum difference from the other notes)
    It assures that the remaining notes must be within the bound values.
    (MAYBE TODO, compare with other algorithm if better results to choose numbers)
    (MAYBE TODO, add flags to return only relevant information)

    After every pair is found we store the notes of interest, the possible notes that align the best,
    and store them in an observable_metrics dictionary. 

    ### Return an array that contains, all possible differences, chosen_winners and observable_metrics for each bound. 
    """
    
    # notes in period_df to get bass and last
    notes = period_df.columns
   
    each_pair_values = []
    for i,row in bounds_df.iterrows():
        bass_value = int(row['bass'])
        last_note_value = int(row['last_note'])
        mean_bound = row['mean']
        all_found, chosen_winners = binary_search_with_bounds(period_df,bass_value,last_note_value, mean_bound)
        

        ## Here we store the values of interest (base, note_1, note_2... last_note)
        # and their indeces
        
        values=[row['bass_value']]
         ## indeces
        indices_to_observe=[row['bass']]
        for d in chosen_winners:
            values.append(d['candidate_value'])
            indices_to_observe.append(d['candidate_index'])
        indices_to_observe.append(row['last_note'])
        values.append(row['last_note_value'])


       


        ## normalizing, and calculating standard deviation and mean
        

        minimum = min(values)
        maximum = max(values)
        mean_vals = sum(values)/len(values)

        ##normalizing
        norm_vals = []
        # for v in values:
        #     normed = (v-minimum)/(maximum-minimum)
        #     norm_vals.append(normed)
        # std_= statistics.stdev(norm_vals)

        observable_metrics = {
            't_values':values,
            'mean_t_sub': mean_vals,
            # 'std_normed':std_,
            'indices':indices_to_observe,
            'difference_(delta_t)':maximum-minimum,
            'difference_ratio_(delta_t_hat)': (maximum-minimum)/mean_vals,
        }

        




        each_pair_values.append({
            "all_found":all_found,
            'chosen_winners':chosen_winners,
            'observable_metrics':observable_metrics
            
        }
        )
        
    return each_pair_values



def compute_all_delta_t_sub_possible_pipeline(note_names,periods_considered=10,sort_bound_by='ratio',only_observable_metric=True):

    """
    Main pipeline to get all delta_t_sub_values
    Steps:
    1. Create period dataframe based on notes desired (to get proper results please order by midi number)
    2. Get period bounds, or, the  cycle_number*period for bass and for last note, where the difference is the minimum. 
    3. For each bound, do a binary search with the remaining notes to find the cycles for each note that minimizes
      the difference between the minimum and maximum periods. i.e. find the point where all notes coincide the best (T_sub with minimum delta_t).
    4. Store relevant information such as chosen cycles, their cycle * period value, their  mean(t_sub) (Equation 16), their
    delta_t (difference between min cycle * period and max cycle * period (this is Equation 17 )) and delta_t_hat (delta_t/mean(t_sub) (Equation 18))

    <i>note_names</i>: names of the notes to consider<br>
    
    <i>periods_considered</i>: amount of periods to consider for algorithm, default is 10<br>
    <i>sort_bound_by</i>: has minimum effect, sort bounds by ratio to perform computation. <br>
    <i>only_observable_metric</i>: if false, get raw information, i.e, all possible differences for each bound,
    chosen winners, for each bound and observable metrics for each bound. 
    if true, only get the observable metrics (which contains the most relevant information for the tension computation.)

    ### Returns relevant dataframe for the stationary_tension (t_sub, deltat)
    """
    periods_df = create_period_dataframe(note_names, periods_considered=periods_considered)
    # print('Periods df:', periods_df)

    bounds_df = finding_min_difference_with_lower_upper_bound(periods_df,sort_bounds_by=sort_bound_by)

    ## now get all corresponding tsubs to each bound
    raw_information = choosing_bounds_binary_search(periods_df,bounds_df)

    if not only_observable_metric:
        return raw_information
    
        ## we will see if our method seems ok????
    observable_metrics=[]
    for item in raw_information:
        observable_metrics.append(item['observable_metrics'])

    

    return create_observable_metrics_df(observable_metrics)


def get_different_observable_df(observable_metrics,
                                sort_by='difference_(delta_t)',
                                top_n=3,
                                top_m=5,
                                filter_top_3_by='t_sub_mean'):

    """
    This function takes the observable metrics generated by the inner functions
    This df contains these columns:<br>
    't_values': array with period values times cycle number for each note,<br>
    'mean_t_sub': mean of the t_values,<br>
    'indices': cero index cycle number  for each period <br>
    'difference_(delta_t)': difference between max and min t_values <br>,
    'difference_ratio_(delta_t_hat)': delta_t/mean_t_sub <br><br>

    This function contains the necessary elements to compute Equation 21. 
    By default, returns our interpretation of m-5 elements (5 smallest delta t values)
    and from those 5, the 3 smallest T_sub values.
    """



    # observable_metrics = compute_all_delta_t_sub_possible_pipeline(note_names, periods_considered=periods_considered, only_observable_metric=True)
    obs_df = create_observable_metrics_df(observable_metrics)

    ## after having the obs_df, we now choose the top_m_elements by sort_by
    ## and if filter_top_3 is not None then we take top_n based on smallest filter_top_3_by

    top_m_df = obs_df.nsmallest(top_m, sort_by)

    if filter_top_3_by is not None:
        top_n_df = top_m_df.nsmallest(top_n, filter_top_3_by)
        return top_n_df
    
    return top_m_df


def equation_21_stationary_tension(delta_t_sub_pairs_df, c=2.6, threshhold_negative_exp=3):
    """
    Implementation of Equation 21 from Chan's paper, where it returns the sum of
    delta_t^c over t_sub. 
    The equation looks like this:
    n * ((1/sum((delta_t_i)^c / t_sub_i))**(1/c))

    threshold_negative_exp is to make sure the denominator part of equation is not too close to zero.    

    where n is the number of elements in the dataframe, delta_t_i is the difference between max and min t_sub
    """

    n = len(delta_t_sub_pairs_df)
    sum_t_pairs = 0

    for i,row in delta_t_sub_pairs_df.iterrows():
        delta_t = row['difference_(delta_t)']
        t_sub = row['mean_t_sub']
        sum_t_pairs += (delta_t**c)/t_sub
    # print(sum_t_pairs)
    if(sum_t_pairs <10**(-threshhold_negative_exp)):
        return 0
    tension = n * ((1/sum_t_pairs)**(1/c))
    return tension



def generate_subharmonic_tension_for_each_possible_case(note_names, periods_considered=10,top_n=3, top_m=5,threshold_neg_exp_for_equation_21=3, max_t_sub=None):

    '''
    Generating subharmonic tension based on Equation 21 from Chan's paper, 
    where Top_n and Top_m default to the values used in the paper (3 and 5 respectively)
    This function returns a dataframe with all the cases computed for the given notes.


    Each case grouped by different methods. case 1-3 are delta t based, case 4-6 are t_sub based, case 7-9 are our ratio based.
    Cases are:<br>
        'Smallest_delta_t_and_filter_by_smallest_t_sub_(Chan\'s_method?)': 'Method A',<br>
        'Smallest_delta_t_and_choose_top_3_delta_t': 'Method B',<br>
        'Smallest_delta_t_and_filter_by_smallest_ratio': 'Method C',<br>

        'Smallest_t_sub_and_choose_top_3_t_sub': 'Method D',<br>
        'Smallest_t_sub_and_filter_by_smallest_delta_t': 'Method E',<br>
        'Smallest_t_sub_and_filter_by_smallest_ratio': 'Method F',<br>

        'Smallest_ratio_and_filter_by_smallest_t_sub': 'Method G',<br>
        "Smallest_ratio_and_filter_by_smallest_delta_t": 'Method H',<br>
        'Smallest_ratio_and_choose_top_3_ratio': 'Method I',<br><br>
        we want to choose the points where the delta t is the smallest with respective to the tsub. So it is balanced as t sub increases<br>
    Each case will have a tension score computed by Equation 21 from Chan's paper. The evaluation considers to use the square of the final evaluation.

    <br> This function receives the following parameters:<br>
    <i>note_names</i>: names of the notes to consider in an array Ex. [C3, E3, G3]<br>
    <i>periods_considered</i>: amount of periods to consider for algorithm, default is 10<br>
    <i>top_m</i>: top m elements to consider for each case, default is 5<br>
    <i>top_n</i>: Out of the topM, consider the top n elements for each case, default is 3<br>
    <i>threshold_neg_exp_for_equation_21</i>: threshold to avoid division by zero (or close to) in Equation 21 computation, default is 3<br>
    <i>max_t_sub</i>: maximum mean t_sub to consider for observables, default is None (no limit)<br>

    '''

    big_df = pd.DataFrame()
    # print('Generating cases for notes:', note_names)
    observable_metrics_df = compute_all_delta_t_sub_possible_pipeline(note_names, periods_considered=periods_considered, only_observable_metric=True)


    ## new feat, now drop all rows that have a mean_t_sub greater than max_t_sub

    # print(f"Before filtering by max_t_sub={max_t_sub}, number of possible observables:", len(observable_metrics_df)
    #       )
    if max_t_sub is not None:
        observable_metrics_df = observable_metrics_df[observable_metrics_df['mean_t_sub']<=max_t_sub]

    # print(f"After filtering by max_t_sub={max_t_sub}, number of possible observables:", len(observable_metrics_df)
    #       )
    
    ## these are the cases, 1 to 3 is delta t based, 4 to 6 is t_sub based, 7 to 9 is our ratio based

    # first  case 1: Smallest_delta_t and filter by smallest t_sub Method A
    case_1 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_(delta_t)', filter_top_3_by='mean_t_sub')
    case_1['case'] = 'Smallest_delta_t_and_filter_by_smallest_t_sub_(Chan\'s_method?)'
    case_1['tension_score']= (equation_21_stationary_tension(case_1,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_1], ignore_index=True)

    # Case 2 Method B
    case_2 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_(delta_t)', filter_top_3_by='difference_(delta_t)')
    case_2['case'] = 'Smallest_delta_t_and_choose_top_3_delta_t'
    case_2['tension_score']= (equation_21_stationary_tension(case_2,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_2], ignore_index=True)

    # case 3 Method C
    case_3 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_(delta_t)', filter_top_3_by='difference_ratio_(delta_t_hat)')
    case_3['case'] = 'Smallest_delta_t_and_filter_by_smallest_ratio'
    case_3['tension_score']= (equation_21_stationary_tension(case_3,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_3], ignore_index=True)

    # Case 4 Method D

    case_4 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='mean_t_sub', filter_top_3_by='mean_t_sub')
    case_4['case'] = 'Smallest_t_sub_and_choose_top_3_t_sub'
    case_4['tension_score']= (equation_21_stationary_tension(case_4,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_4], ignore_index=True)

    # Case 5 Method E
    case_5 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='mean_t_sub', filter_top_3_by='difference_(delta_t)')
    case_5['case'] = 'Smallest_t_sub_and_filter_by_smallest_delta_t'
    case_5['tension_score']= (equation_21_stationary_tension(case_5,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_5], ignore_index=True)

    # Case 6 Method F
    case_6 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='mean_t_sub', filter_top_3_by='difference_ratio_(delta_t_hat)')
    case_6['case'] = 'Smallest_t_sub_and_filter_by_smallest_ratio'
    case_6['tension_score']= (equation_21_stationary_tension(case_6,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_6], ignore_index=True)

    # Case 7 Method G
    case_7 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='mean_t_sub')
    case_7['case'] = 'Smallest_ratio_and_filter_by_smallest_t_sub'
    case_7['tension_score']= (equation_21_stationary_tension(case_7,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_7], ignore_index=True)

    # Case 8 Method H
    case_8 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_(delta_t)')
    case_8['case'] = 'Smallest_ratio_and_filter_by_smallest_delta_t'
    case_8['tension_score']= (equation_21_stationary_tension(case_8,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_8], ignore_index=True)

    # Case 9 Method I
    case_9 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_ratio_(delta_t_hat)')
    case_9['case'] = 'Smallest_ratio_and_choose_top_3_ratio'
    case_9['tension_score']= (equation_21_stationary_tension(case_9,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    big_df = pd.concat([big_df, case_9], ignore_index=True)

    # # #then case 1: Smallest_t_sub and choose top 3 delta_t

    # # case_1 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='mean_t_sub', filter_top_3_by='mean_t_sub')
    # # case_1['case'] = 'Smallest_t_sub_and_choose_top_3_t_sub'
    # # case_1['tension_score']= (equation_21_stationary_tension(case_1,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # # big_df = pd.concat([big_df, case_1], ignore_index=True)

    # # case 2: Smallest_delta_t and choose top 3 delta_t
    # case_2 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_(delta_t)', filter_top_3_by='difference_(delta_t)')
    # case_2['case'] = 'Smallest_delta_t_and_choose_top_3_delta_t'
    # case_2['tension_score']= (equation_21_stationary_tension(case_2,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_2], ignore_index=True)

    # # case 3: Smallest_delta_t and filter by smallest t_sub
    # case_3 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_(delta_t)', filter_top_3_by='mean_t_sub')
    # case_3['case'] = 'Smallest_delta_t_and_filter_by_smallest_t_sub_(Chan\'s_method?)'
    # case_3['tension_score']= (equation_21_stationary_tension(case_3,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_3], ignore_index=True)

    # # case 4: Smallest_t_sub and filter by smallest delta_t
    # case_4 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='mean_t_sub', filter_top_3_by='difference_(delta_t)')
    # case_4['case'] = 'Smallest_t_sub_and_filter_by_smallest_delta_t'
    # case_4['tension_score']= (equation_21_stationary_tension(case_4,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_4], ignore_index=True)


    # # our case to study
    # case_5 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='mean_t_sub')
    # case_5['case'] = 'Smallest_ratio_and_filter_by_smallest_t_sub'
    # case_5['tension_score']= (equation_21_stationary_tension(case_5,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_5], ignore_index=True)

    # # our case to study 2

    # case_6 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='mean_t_sub')
    # case_6['case'] = 'Smallest_ratio_and_filter_by_smallest_t_sub_without_square'
    # case_6['tension_score']= (equation_21_stationary_tension(case_6,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))
    # big_df = pd.concat([big_df, case_6], ignore_index=True)

    # # our  case to study 3:
    # # Only top 3 ratios

    # case_7 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_ratio_(delta_t_hat)')
    # case_7['case'] = 'Smallest_ratio_and_choose_top_3_ratio'
    # case_7['tension_score']= (equation_21_stationary_tension(case_7,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_7], ignore_index=True)

    # case_8 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_ratio_(delta_t_hat)')
    # case_8['case'] = 'Smallest_ratio_and_choose_top_3_ratio_without_square'
    # case_8['tension_score']= (equation_21_stationary_tension(case_8,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))
    # big_df = pd.concat([big_df, case_8], ignore_index=True)

    # ## case 9 : smallest ratio filter by delta t
    # case_9 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_(delta_t)')
    # case_9['case'] = 'Smallest_ratio_and_filter_by_smallest_delta_t'
    # case_9['tension_score']= (equation_21_stationary_tension(case_9,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))**2
    # big_df = pd.concat([big_df, case_9], ignore_index=True)

    # case_10 = get_different_observable_df(observable_metrics_df, top_n=top_n, top_m=top_m, sort_by='difference_ratio_(delta_t_hat)', filter_top_3_by='difference_(delta_t)')
    # case_10['case'] = 'Smallest_ratio_and_filter_by_smallest_delta_t_without_square'
    # case_10['tension_score']= (equation_21_stationary_tension(case_10,c=2.1,threshhold_negative_exp=threshold_neg_exp_for_equation_21))
    # big_df = pd.concat([big_df, case_10], ignore_index=True)
    return big_df



def compute_subharmonic_tension_for_each_note_array(note_names,chord_labels,periods_considered=10, threshold_neg_exp_for_equation_21=3, max_t_sub=0.01):

    """
    Computes subharmonic tension for each note array given.
    Returns a big dataframe with all the cases computed for each note array.
    Note names should be array of arrays, where each array is a chord/note set
    e.g. [['C3','E3','G3'], ['D3','F#3','A3']]
    """
    big_df_for_notes = pd.DataFrame()
    for notes_index in range(len(note_names)):
        notes=note_names[notes_index]
        chord_label = chord_labels[notes_index]
        big_df = generate_subharmonic_tension_for_each_possible_case(notes, periods_considered=periods_considered, threshold_neg_exp_for_equation_21=threshold_neg_exp_for_equation_21, max_t_sub=max_t_sub)
        big_df['note_names'] = ','.join(notes)
        big_df['chord_label'] = chord_label
        big_df_for_notes = pd.concat([big_df_for_notes, big_df], ignore_index=True)
    


    return big_df_for_notes

def compute_normalized_subharmonic_tension_for_each_case(big_df_for_notes):
    '''
    Computes normalized tension for each case in the big dataframe
    Returns a normalized score per note_names based on case. 

    '''

    big_df_for_notes['normalized_tension_score'] = 0.0

    ## for each case loop and compute the normalized tension
    for case in big_df_for_notes['case'].unique():
        case_df = big_df_for_notes[big_df_for_notes['case']==case]
        max_tension = case_df['tension_score'].max()
        min_tension = case_df['tension_score'].min()
        normed_values = []
        for i,row in case_df.iterrows():
            tension = row['tension_score']
            if max_tension - min_tension == 0:
                normed = 0
            else:
                normed = (tension - min_tension) / (max_tension - min_tension)
            normed_values.append(normed)
        big_df_for_notes.loc[big_df_for_notes['case']==case, 'normalized_tension_score'] = normed_values

    return big_df_for_notes


def correlation_line_point_chart(data_frame,x_axis='periods_considered',y_axis='correlation',color='subharmonic_method'):
    line_chart = alt.Chart(data_frame).mark_line(
    opacity=0.5
    ).encode(
    x=alt.X(x_axis, title='Periods considered to compute Subharmonic Modulation'),
    y=alt.Y(y_axis),
    color=alt.Color(color,legend=None)

    )

    point_chart = alt.Chart(data_frame).mark_point().encode(
      x=alt.X(x_axis, title='Periods considered to compute Subharmonic Modulation',scale=alt.Scale(domain=[4,32])),
    y=alt.Y(y_axis),
    color=alt.Color(color,legend=alt.Legend(title='Different Methods used',titleAnchor='middle',symbolSize=100)),
       shape=alt.Shape(color,legend=alt.Legend(title='Different Methods used',titleAnchor='middle',symbolSize=100)),

    )
    return point_chart, line_chart

def main():
    
    # Example usage

    note_names = ['C3', 'E3', 'G3', 'C4']
    observable_metrics = compute_all_delta_t_sub_possible_pipeline(note_names,periods_considered=10,only_observable_metric=True)
    print('Observable metrics:', create_observable_metrics_df(observable_metrics, note_names))

