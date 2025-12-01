

vis_type = 'stationary' //default visualization type
function change_visualization(visualization_type){

    vis_type = visualization_type
   $('.containers').remove()
    switch(visualization_type){
        case 'main':

            init_first_visualization()
            break
        case 'stationary':
            init_stationary_visualization()
            break
    }

}




function init_first_visualization(){    
    
    container_div = $('<div/>',{
        'id':'container',
        'class':'hertz_container containers',
    })
    container_div.appendTo('body')

    div = $('<div/>',{
        'id':'main_viz',
        'class':'main_viz',
    })

    $('#container').append(div)
    // div.appendTo('#container')
    controller = $('<div/>',{
        'id':'controllers',
        'class':'controllers',
    })

    row_note_grid = $('<div/>',{
        'id':'note_grid',
        'class':'row_visuals note_grid',
    })
    row_note_grid.appendTo(controller)
    row_bar_viz = $('<div/>',{
        'id':'bar_viz',
        'class':'row_visuals bar_viz',
    })
    row_bar_viz.appendTo(controller)
    row_piano_viz = $('<div/>',{
        'id':'piano_viz',
        'class':'row_visuals piano_viz',
    })
    row_piano_viz.appendTo(controller)



    



    controller.appendTo('#container')

    create_bar_axis()
    build_note_grid()
    create_piano()
    create_cof_svg()


  

}


function init_stationary_visualization(){


    create_containers_with_inputs()

    
    create_stationary_bar_axis()
}








//TODO, add features for visualization
 filter = false

function visualization_pipeline(event){
    six_types_of_harmonics = listen_to_midi(event)
    // console.log(six_types_of_harmonics)
    
    harmonics = six_types_of_harmonics.harmonics
    harmonics_in_modulo_12 = six_types_of_harmonics.harmonics_in_modulo_12
    harmonics_with_names = six_types_of_harmonics.harmonics_with_names
    harmonics_in_hertz_from_midi_numbers = six_types_of_harmonics.harmonics_in_equal_hertz

    // Overtone series in hertz
    harmonics_in_hertz = six_types_of_harmonics.harmonics_in_hertz

    console.log('harmonics_in_hertz: ',harmonics_in_hertz)

    //note_periods for stationary harmony
    note_periods_per_note_per_cycle = six_types_of_harmonics.note_periods_per_note

    /*

    this dataframe looks like this:
    { midi_numebr:{
        periods : [array_of_periods, from 0 to n cycles considered],
        midi_number: midi_number
        cycles: [n cycles],
        note_name: note_name+octave
    }}


    */



    // set_bass_note_for_color(notes_playing)
    // console.log("Harmonics in Hertz: ",harmonics_in_hertz)





    if(filter){
        consonant_and_dissonant_harmonics = calculate_tension_in_harmonicsV2(harmonics_in_hertz_from_midi_numbers)
     return
    }



    switch(vis_type){
        case 'main':

        
            paths_to_visualize = create_paths(harmonics_in_modulo_12)
            
                
                /* {midi_num: {
                        hertz, note_name
                    }, 
                    midi_num:{}
                }

                    */
        

            squares_to_visualize = create_squares_in_grid2(harmonics_in_hertz)

            colors_for_text = get_colors_for_text(harmonics_in_modulo_12)
            // harmonics_in_hertz Struct:


            bars_to_visualize = create_bars(harmonics_in_hertz)

            //BARS TO VISUALIZE?? updated
            
            
            // console.log('squares_to_visualize: ',squares_to_visualize)
            //console.log(paths_to_visualize)

            
            // console.log('Harmonics in Hertz', harmonics_in_hertz)
            
            
            



                visualize_paths_in_cof(paths_to_visualize)
                visualize_squares_in_grid(squares_to_visualize)
                visualize_hertz_bars(bars_to_visualize)
                change_colors_of_notes(colors_for_text)

        break


        case 'stationary':

            // returned_information_from_stationary_tension = manage_stationary_visualization(note_periods_per_note_per_cycle)
            // note_pairs_per_bound = returned_information_from_stationary_tension.note_pairs_per_bound
            // preprocessed_data = returned_information_from_stationary_tension.preprocessed_data
            preprocessed_data = preprocess_data(note_periods_per_note_per_cycle)
            note_pairs_per_bound = []
            visualize_stationary_tension(note_pairs_per_bound,preprocessed_data)
        break
    }
   

    

}




