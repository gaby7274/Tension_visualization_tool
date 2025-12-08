// Global variables for each necessary div

let div_interharmonic_visualization_id= 'interharmonic_visualization'
let div_note_grid_id= 'note_grid_visualization'
let ihm_graph_id = 'interharmonic_modulation_graph'




function create_containers_for_stationary_tension(){
    container_div = $('<div/>',{
        'id':'container',
        'class':'stationary_container containers',
    })
    container_div.appendTo('body');


    //After creating body, divide in two main divs, upper div for visualizations, lower div for controllers.

    div_visualizations = $('<div/>',{
        'class':'display_graphs',
        'id':'display_graphs',
        })
    div_visualizations.appendTo('#container')

    //First append the two divs for visualizations
    div_interharmonic_visualization = $('<div/>',{
        'class':'interharmonic_modulation_visualization',
        'id':div_interharmonic_visualization_id,
    })
    div_interharmonic_visualization.appendTo(div_visualizations)

    div_subharmonic_modulation_visualization = $('<div/>',{
        'class':'subharmonic_modulation_visualization',
        'id':'subharmonic_modulation_visualization',
    })
    div_subharmonic_modulation_visualization.appendTo(div_visualizations)



    // Now create the lower div for controllers
    div_controllers = $('<div/>',{
        'class':'controls_container',
        'id':'controls_container',
    })
    div_controllers.appendTo('#container')

    div_staff = $('<div/>',{
        'class':'staff_visualization',
        'id':'staff_visualization',
    })
    div_staff.appendTo(div_controllers)

    div_information_for_computation = $('<div/>',{
        'class':'information_for_computation',
        'id':'information_for_computation',
    })

    div_information_for_computation.appendTo(div_controllers)

    
    // div_stationary_bars = $('<div/>',{
    //     'id':'stationary_bars',
    //     'class':'stationary_bars',
    // })

    // div_period_controllers = $('<div/>',{
    //     'id':'period_controllers',
    //     'class':'period_controllers',
    // })

    // div_sliders_container = $('<div/>',{
    //     'id':'sliders_container',
    //     'class':'sliders_container',
    // })


    // slider_div =$('<div/>',{
    //     'class':'slider_div',
    // })
    // slider_label = $('<label/>',{
    //     'for':'t_sub_slider',
    // }).text('T <sub>sub</sub> range')
    // input_slider = $('<input/>',{
    //     'type':'range',
    //     'min':10,
    //     'max':200,
    //     'class':'slider',
    //     'id':'t_sub_slider',
    //     'value':100
    // })
    // slider_label.appendTo(slider_div)
    // input_slider.appendTo(slider_div)
    // slider_div.appendTo(div_sliders_container)
   

    //  slider_div =$('<div/>',{
    //     'class':'slider_div',
    // })
    // slider_label = $('<label/>',{
    //     'for':'delta_t_slider',
    // }).text('&#916;t amount')

  
    // input_slider = $('<input/>',{
    //     'type':'range',
    //     'min':10,
    //     'max':200,
    //     'class':'slider',
    //     'id':'delta_t_slider',
    //     'value':100
    // })
    // slider_label.appendTo(slider_div)
    // input_slider.appendTo(slider_div)
    // slider_div.appendTo(div_sliders_container)
    // // input_slider.appendTo(div_sliders_container)
    // div_sliders_container.appendTo(div_period_controllers)


 
    // $('#container').append(div_stationary_bars)
    // $('#container').append(div_period_controllers)


    // // add onchange events to sliders
    // $('#t_sub_slider').on('input', function() {

    //     //TODO change display of value
    //     change_x_sine_scale()
    //     //is it good practice??? sending default for switch case and redraw. 
    //     visualization_pipeline({data:[999]})


    // })

}


function create_interharmonic_visualization(){


    // First thing is build two subdivs  


    div_note_grid = $('<div/>',{
        'id':div_note_grid_id,
        'class':'note_grid_visualization',
    })
    div_note_grid.appendTo('#'+div_interharmonic_visualization_id)

    div_ihm_graph = $('<div/>',{
        'id':ihm_graph_id,
        'class':'interharmonic_modulation_graph',
    })
    div_ihm_graph.appendTo('#'+div_interharmonic_visualization_id)



    build_note_grid(div_note_grid_id)

    build_line_graph_for_interharmonic_modulation(ihm_graph_id)
    // $('#'+ihm_graph_id).css('display','none')

    // now create the two divs for the bars, one in the left downside 
    // and the other in the right downside 

    div_triad_gt_bar_div = $('<div/>',{
        'id':'triad_gt_bar_div',
        'class':'triad_gt_bar_div',
    })
    div_triad_gt_bar_div.appendTo('#'+div_interharmonic_visualization_id)

    div_interval_gt_bar_div = $('<div/>',{
        'id':'interval_gt_bar_div',
        'class':'interval_gt_bar_div',
    })
    div_interval_gt_bar_div.appendTo('#'+div_interharmonic_visualization_id)


    // create_ground_truth_bars_for_stationary_tension('triad_gt_bar_div',ground_truth_triads)
    // create_ground_truth_bars_for_stationary_tension('interval_gt_bar_div',ground_truth_intervals)

}


// Here this will run each time a specific user specification occurs on how to compute final tension score
function compute_tension_for_ground_truth_and_specific_parameters(){
    //TODO each ground_truth interval and ground_truth_triads run


    for(let i=0; i<ground_truth_intervals.length;i++){
        let gt_interval = ground_truth_intervals[i]
        harm_per = calculate_harmonics_for_stationary(gt_interval.midi_numbers)
        harmonics = harm_per.harmonics_in_hertz
        periods = harm_per.note_periods_per_note
        interharmonic_tension_pipeline(harmonics,gt=true,note_combination=gt_interval.note_combination)
    }

    curr_ground_truth_set = ground_truth_triads
      for(let i=0; i<ground_truth_triads.length;i++){
        let gt_triad = ground_truth_triads[i]
        harm_per = calculate_harmonics_for_stationary(gt_triad.midi_numbers)
        harmonics = harm_per.harmonics_in_hertz
        periods = harm_per.note_periods_per_note
        interharmonic_tension_pipeline(harmonics,gt=true,note_combination=gt_triad.note_combination)
    }
}