
## defining multiple functions to handle tension dataframes
import pandas as pd
from math import log2
import numpy as np
from scipy import stats
import altair as alt
import json


## Function definitions, equations for converting between hertz and midi number

#hz is the number
def equation_for_midi_number(hz):
    """
    Converts hertz to midi number using the inverse of the hertz to midi number formula
    440* 2**((n-69)/12) = hz
    """
    return 12*log2(hz/440) +69
    

# N is the midi number

def equation_for_hertz(n):
    """
    Converts midi number to hertz using the formula
    440* 2**((n-69)/12) = hz
    where n is the midi number
    """
    return 440* 2**((n-69)/12)




def equation_for_harmonics(number_of_harmonics, midi_number):
    """
     Returns a list of harmonics for a given midi number,
       given the number of harmonics considered. 
    """

    all_harmonics = []
    hertz = equation_for_hertz(midi_number)
    for i in range(number_of_harmonics):
        
        all_harmonics.append((i+1)*hertz)
    
    return all_harmonics
        
def create_harmonic_dataframe(harmonics_considered=10):
    """
    Function to create a dataframe with n harmonics_considered
    Default value is 10 harmonics
    88 keys of a piano, from A0 to C8

    Returns a dataframe with note names as columns and harmonics as rows
    88 columns, and harmonics_considered rows
    """
    note_df = pd.DataFrame()

    # Piano range computes the midi numbers for a standard 88 key piano

    piano_range = range(21, 109)
    piano_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    piano_octave = [str(i) for i in range(0, 9)]

    ##populating dataframe columns
    piano_note_index = 0
    piano_octave_index = 0
    for midi_number in piano_range:

        # Per each octave reached, add the corresponding number. Starts at A0, and to reach C1 we need to use mod12==3
        if piano_note_index %12 == 3:
            piano_octave_index += 1
        
        ## Naming notes with corresponding note and octave
        note_name = piano_notes[piano_note_index % 12] + piano_octave[piano_octave_index]

        # Populate rows for each column with the harmonics. 
        note_df[note_name]= equation_for_harmonics(harmonics_considered,midi_number)
        
        piano_note_index += 1

    return note_df


def return_compared_chord_label_with_empirical_ranking(chord_label_ordered_by_rank, empirical_ranking):
    """
    This function recieves a chord label orered by ranking, and then returns
    An array of positions based on empirical ranking. Example, 
    if array of 0,1,2,3,4,5,6... is returned, then the chord_label_ordered_by_rank
    corresponds to the empirical_ranking array.

    Returns the ordered array, plus correlation and pvalue

    """
    empirical_ranking_index = range(len(empirical_ranking))

    #list of index ordered by rank
    ranked_based_emp = [] 
    for item in chord_label_ordered_by_rank:
        ranked_based_emp.append(empirical_ranking.index(item))

    correlation,p_value = stats.pearsonr(ranked_based_emp,empirical_ranking_index)

    return ranked_based_emp,correlation,p_value

## function to sort tension ranking and return a list containing the rank for each index

def sort_and_add_indexes(tension_ranking, interval_labels=['U', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', '8v']):
    
    """

    ### Returns a dataframe with the interval labels (soon to change for triads as well) 
    ###  and the sum of tension scores for each interval.
    tension_ranking is a list of lists, where:
        each sublist is the number of points that fall in a specific interharmonic region.
        Each of these regions is the index of the sublist.

    interval_labels is a list of strings, where each string is the label for the corresponding index in tension_ranking.
         default is the list of interval names for an octave.
    

    
    })"""
    ## sum of tension schores for each region.  
    tension_ranking_summed = [sum(tension) for tension in tension_ranking]

    ## dataframe of interval labels and tension scores, pairing interval and tension score
    score_for_labels =pd.DataFrame({
        'interval': interval_labels,
        'tension_ranking_sum': tension_ranking_summed
    })

   


    return score_for_labels



def return_tension_ranking_df(tension_list,number_of_harmonics,method_name='unweighted',interval_labels=['U', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', '8v'],empirical_ranking=[]):
    """
    ### Returns df with ranking based on sum of points that fall in dissonance region
    tension_list is a list of lists, where:
        each sublist is the number of points that fall in a specific interharmonic region.
        Each of these regions is the index of the sublist.

    number_of_harmonics is an integer, the number of harmonics considered for the tension calculation, 
    i.e. how many harmonics were used to create the dataframe.

    """
    tension_ranking_df = sort_and_add_indexes(tension_list, interval_labels=interval_labels)
    # print('Tension ranking df:\n', tension_ranking_df)
    
    
    ## adding number of harmonics column
    tension_ranking_df['number_of_harmonics'] = number_of_harmonics

    ## adding index to df as a column after sorting, (so index is ranking)

    sorted_tension_ranking = tension_ranking_df.sort_values(by='tension_ranking_sum', ascending=True).reset_index(drop=True)

    # adding index as ranking
    sorted_tension_ranking['tension_ranking'] = sorted_tension_ranking.index


    sorted_tension_ranking['method']= method_name if 'method_name' in locals() else 'unweighted'
    
    
    return sorted_tension_ranking


def return_subharmonic_tension_ranking(big_df_for_notes, case_column='case', tension_column='tension_ranking', chord_label_column='chord_label'):
    """
    Returns a dataframe with subharmonic tension ranking for each chord label and case.
    big_df_for_notes is a dataframe with columns for chord_label, case, and tension_ranking.
    case_column is the name of the column in big_df_for_notes that contains the case information.
    tension_column is the name of the column in big_df_for_notes that contains the tension ranking information.
    chord_label_column is the name of the column in big_df_for_notes that contains the chord label information.

    The function groups the dataframe by chord_label and case, and computes the mean tension ranking for each group.
    It then sorts the resulting dataframe by chord_label and mean tension ranking, and adds a ranking column.

    Returns a dataframe with columns for chord_label, case, mean_tension_ranking, and ranking.
    """
   


    grouped = big_df_for_notes.groupby([case_column, chord_label_column]).agg({
        'tension_score': 'mean'
    }).reset_index()

    # Rank chord labels by tension score within each case
    for case in grouped['case'].unique():
        case_mask = grouped['case'] == case
        grouped.loc[case_mask, 'rank'] = grouped.loc[case_mask, 'tension_score'].rank(method='min')

    return grouped.sort_values(by=['case', 'rank'])



def return_correlation_df(tension_list,number_of_harmonics,empirical_ranking, interval_labels=['U', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', '8v']):
    """
    
        ## returns a df with correlation between empirical ranking and computed ranking
        TODO: add option for many type of modulation and array of number_of_harmonics.
        list of number of harmonics, and list of tension_lists,
    """
    tension_ranking_df = sort_and_add_indexes(tension_list)
    empirical_ranking_number = np.arange(0,len(empirical_ranking))

    # print('Printing for debugging purposes:')
    # print(empirical_ranking_number)
    sorted_tension_ranking = tension_ranking_df.sort_values(by='tension_ranking_sum', ascending=True).reset_index(drop=True)


    ## after having df, sort by tension ranking sum to get ranking
    interval_tension_ranking = sorted_tension_ranking['interval'].tolist()
    print('Interval tension ranking:', interval_tension_ranking)

    ## now that i have the two labels, find the index of empirical ranking in computed ranking
    tension_ranking = [interval_tension_ranking.index(label) for label in empirical_ranking]
    

    correlation_coefficient = stats.pearsonr(tension_ranking, empirical_ranking_number)[0]
    corr_df = {
        'number_of_harmonics':[number_of_harmonics],
        'correlation_coefficient':[correlation_coefficient],
        'type_of_modulation':['unweighted']
    }
    return pd.DataFrame(corr_df)



def create_correlation_df(dataframe, ranking_column='tension_ranking',empirical_ranking=[],column_to_compare_with_emp_rank='interval'):
    """
    Returns a dataframe with correlation coefficients between computed rankings and empirical rankings

    dataframe should contain a column for ranking.
    Empirical ranking should be ordered from least to most tense.
    ranking_columns should be the column of tension rankings to compare against empirical ranking.
    1. Extract tension rankings from dataframe
    2. Compare with empirical ranking
    3. Compute correlation coefficient
    """

    if len(empirical_ranking) == 0:
        raise ValueError("Empirical ranking list is empty. Please provide a valid empirical ranking.")
    correlation_df = pd.DataFrame()
  
    # sort by ranking
    df = dataframe.copy().sort_values(by=ranking_column, ascending=True)

    #get the ranking as list

    tension_ranking= df[column_to_compare_with_emp_rank].tolist()

    #get index of empirical ranking in tension ranking order.
    # this means, if tension ranking is equal to empirical ranking, the index will be 0,1,2,3...
    # if there are orders switched thn the index will be different. It is necessary

    ranking_compared_to_empirical = [empirical_ranking.index(item) for item in tension_ranking]

    # compute correlation

    correlation_value, p_value = stats.pearsonr(range(len(ranking_compared_to_empirical)), ranking_compared_to_empirical)

    # populate df
    correlation_df['correlation_coefficient'] = [correlation_value]
    correlation_df['p_value'] = [p_value]
    correlation_df['tension_ranking'] = str(tension_ranking) 
    correlation_df['empirical_ranking'] = str(empirical_ranking)

    return correlation_df


##############################################################
#
# Functions for subharmonic modulation
#
##############################################################

def create_period_dataframe(note_names,periods_considered=10):
    """
    Function to create a dataframe with n periods_considered
    Default value is 10 periods
    only on the note_names considered. 

    Returns a dataframe with note names as columns and periods as rows
    len(note_names), and periods_considered rows
    """

    ## Create period dataframe from fundamental period
    fundamental_df = create_harmonic_dataframe(1)

    

    fundamental_df = fundamental_df[note_names]

    ## case where there are unisons

    ## if there are columns with the same name, then
    ## adda _<index> to the column names
    if fundamental_df.columns.duplicated().any():

        fundamental_df.columns = [f"{col}_{i}" if list(fundamental_df.columns).count(col) > 1 else col for i, col in enumerate(fundamental_df.columns)]


    ## create a dataframe with the first period, then subsequent periods
    df = pd.DataFrame()
    for note_name in fundamental_df.columns:
        df[note_name]= 1/fundamental_df[note_name]

    ## calculating period
    for i in range(1,periods_considered):
        list_of_periods = []
        for note_name in fundamental_df.columns:
            list_of_periods.append((1/(fundamental_df[note_name][0]))*(i+1))

        df.loc[i] = list_of_periods
   

    
    return df




def create_observable_metrics_df(observable_metrics):
    """
    Create a dataframe from observable_metrics, with note names
    Watch OUT not in tidy_data.


    therefore somecolumns contain arrays
    ### Returns a dataframe with note names, t_values, cycles_or_t*k, difference_(delta_t), difference_ratio_(delta_t_hat),mean_(t_sub)
    """


    obs_df = pd.DataFrame(observable_metrics)
    return obs_df


def take_period_def_extract_winners(period_df,observable_metrics):

    """
    Extract winners from observable metrics and return a dataframe with note names, t_values, cycle_or_t, winner_num
    ### Returns a dataframe with note names, t_values, cycle_or_t, winner_num
    """
    note_names = period_df.columns
    new_df = {
        'note_name':[],
        't_values':[],
        # 't_value_in_met':[],
        'cycle_or_t':[],
        'winner_num':[],
    }
    count=0
    for item in observable_metrics:
        # print(item)
        indices = item['indices']
        # print('indices:', indices)
        count+=1
        
        values = item['t_values']
        # print('values:', values)
        for i in range(len(indices)):
            note_name = note_names[i]
            new_df['note_name'].append(note_name)
            new_df['t_values'].append(values[i])
            new_df['cycle_or_t'].append(indices[i])
            new_df['winner_num'].append(count)
            # new_df['t_value_in_met'].append(values[i])
    return pd.DataFrame(new_df)

def create_corr_heatmap(corr_df, corr_column='correlation_coefficient', p_value_column='p_value', x='number_of_harmonics', y='type_of_modulation',min_x=2, max_x=26):
    

    # grid rectangle plot
    corr_chart = alt.Chart(corr_df).mark_rect().encode(
        x=alt.X(x+':O', title='Number of Harmonics'),# scale=alt.Scale(domain=[min_x, max_x])),

        y=alt.Y(y+':O', title='Type of Modulation'),
        color=alt.Color(corr_column+':Q', title='Correlation Coefficient', scale=alt.Scale(scheme='viridis')),
        tooltip=[x, y, corr_column, p_value_column]
    ).properties(
        title='Correlation between Empirical and Computed Tension Rankings',
    )

    text_chart = alt.Chart(corr_df).mark_text(baseline='middle', color='black').encode(
        x=alt.X(x+':O', title='Number of Harmonics'), #scale=alt.Scale(domain=[min_x, max_x])),
        y=y+':N',
        text=alt.Text(corr_column+':Q', format='.3f')
    )
    return corr_chart, text_chart



def get_correlation_between_empirical_and_method(empirical_ranking, df_with_rankings, numbered_ranking=None,chord_label_column='chord_label', column_to_compare_with_emp='raw_t_score_summed_only_modulations'):
    ## first normalize empirical ranking

    empirical_ranking_numbered = range(0, len(empirical_ranking))

    if numbered_ranking is None:
        normalized_values = [x / max(empirical_ranking_numbered) for x in empirical_ranking_numbered]
    else:
        mininum = min(numbered_ranking) 
        maximum = max(numbered_ranking)
        normalized_values = [(x - mininum) / (maximum - mininum) for x in numbered_ranking]

    ## we are going to create a dictionary with the chord labels
    # with their respective scores. The plan is to see how correlated they are. 
    keys_for_dict = df_with_rankings[chord_label_column].tolist()
    
    ranked_df = {}
    for key in keys_for_dict:
        ranked_df[key] = df_with_rankings[df_with_rankings[chord_label_column] == key][column_to_compare_with_emp].values[0]
    
    ## now we are going to construct a list based on the empirical ranking 
    # using this dictionary

    for chord in empirical_ranking:
        if chord not in ranked_df.keys():
            print(f'Warning: chord {chord} not found in the dataframe keys')
            continue
    values_to_correlate = [ranked_df[chord] for chord in empirical_ranking]

    # get correlation
    corr, p_value = stats.pearsonr(normalized_values, values_to_correlate)

    return corr, p_value, values_to_correlate



def convert_correlation_df_to_a_line_chart_df(df_to_convert, empirical_ranking_names, column_to_convert='final_ranking_correlate', group_by_methods_array=None):
    '''
    This function converts the normalized values in a df to another df having individual,
    ranking for each chord label. 
    Then we can compare how each method ranking compares to  empirical ranking.

    So we take normalized values, and match it with the respective chord_label.

    the column to convert is an array that contains normalized values for each chord label<br>
    then we take empirical ranking names to match each value with its chord label.

    Group by methods is an array of methods we want to include per each chord label<br>

    example, if a row contains a method with harmonics, and from that row we derive the 13 intervals
    we want to keep track of which method produced which interval. So if group_by_methods_array contains 'harmonics_considered' and 'clean_method_name'
    each chord label will contain those two columns with the respective values.
    
    '''


    df_for_each_empirical_ranked = pd.DataFrame()
    ## loop  for  each value, we are going to break df
    for i,row in df_to_convert.iterrows():
        ## extract  array of each normalized value
        normalized_values_for_each_rank = json.loads(row[column_to_convert])
        
        print('Normalized values for each rank:', normalized_values_for_each_rank)
        if len(normalized_values_for_each_rank) != len(empirical_ranking_names):
            raise ValueError(f'Length of normalized values {len(normalized_values_for_each_rank)} does not match length of empirical ranking names {len(empirical_ranking_names)}')
        small_df = pd.DataFrame({
            'chord_label': empirical_ranking_names,
            'normalized_value': normalized_values_for_each_rank
        })        

        # add aditional columns
        if group_by_methods_array is not None:
            for method in group_by_methods_array:
                small_df[method] = row[method]

        

        df_for_each_empirical_ranked = pd.concat([df_for_each_empirical_ranked, small_df], ignore_index=True)

    return df_for_each_empirical_ranked

# main()