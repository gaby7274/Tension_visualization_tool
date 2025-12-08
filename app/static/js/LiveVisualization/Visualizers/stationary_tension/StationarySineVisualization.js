bar_x_scale = null
bar_y_scale = null
hertz_bar_width = null
hertz_bar_height = null

sine_x_scale = null
sine_y_scale = null


vertical_x = null
horizontal_y = null


bar_width = null
bar_height=null

top_n_notes = 5

//temp
note_color_wheel = d3.scaleOrdinal([0,1,2,3,4,5],['magenta','green','cyan','yellow','orange','red'])

/*

    Stationary Sine Visualization
    create container with inputs
    Slider to change x axis
    slider to change amount of rectangles

    create sinewaves, normalize bass to one and others respective to bass
    draw rectangles at t sub points
    create points to y axis that oscilate with sinewave

*/ 




function create_containers_with_inputs(){
    container_div = $('<div/>',{
        'id':'container',
        'class':'stationary_container containers',
    })
    container_div.appendTo('body');
    
    div_stationary_bars = $('<div/>',{
        'id':'stationary_bars',
        'class':'stationary_bars',
    })

    div_period_controllers = $('<div/>',{
        'id':'period_controllers',
        'class':'period_controllers',
    })

    div_sliders_container = $('<div/>',{
        'id':'sliders_container',
        'class':'sliders_container',
    })


    slider_div =$('<div/>',{
        'class':'slider_div',
    })
    slider_label = $('<label/>',{
        'for':'t_sub_slider',
    }).text('T <sub>sub</sub> range')
    input_slider = $('<input/>',{
        'type':'range',
        'min':10,
        'max':200,
        'class':'slider',
        'id':'t_sub_slider',
        'value':100
    })
    slider_label.appendTo(slider_div)
    input_slider.appendTo(slider_div)
    slider_div.appendTo(div_sliders_container)
   

     slider_div =$('<div/>',{
        'class':'slider_div',
    })
    slider_label = $('<label/>',{
        'for':'delta_t_slider',
    }).text('&#916;t amount')

  
    input_slider = $('<input/>',{
        'type':'range',
        'min':10,
        'max':200,
        'class':'slider',
        'id':'delta_t_slider',
        'value':100
    })
    slider_label.appendTo(slider_div)
    input_slider.appendTo(slider_div)
    slider_div.appendTo(div_sliders_container)
    // input_slider.appendTo(div_sliders_container)
    div_sliders_container.appendTo(div_period_controllers)


 
    $('#container').append(div_stationary_bars)
    $('#container').append(div_period_controllers)


    // add onchange events to sliders
    $('#t_sub_slider').on('input', function() {

        //TODO change display of value
        change_x_sine_scale()
        //is it good practice??? sending default for switch case and redraw. 
        visualization_pipeline({data:[999]})


    })

}



function create_stationary_bar_axis(){

    margin = {top: 10, right: 10, bottom: 10, left: 10}
    bar_width = document.getElementById('stationary_bars').clientWidth-margin.left-margin.right
    bar_height = document.getElementById('stationary_bars').clientHeight
    let legend_width =bar_width+margin.left+margin.right
    
    bar_svg = d3.select('#stationary_bars')
    .append('svg')
    .attr('id', "bar_svg")
    .attr('width', bar_width)
    .attr('height', bar_height)
    .style('background-color', 'black');


    stationary_bar_svg_group = bar_svg.append('g')
    .attr('id', 'stationary_bar_svg_group')


    vertical_x = bar_width/12
    hertz_bar_width = bar_width/26
    horizontal_y = (bar_height/9)
    hertz_bar_height = bar_height

    y_line = stationary_bar_svg_group.append('line')
    .attr('id', 'bar_y_line')
    .attr('x1', vertical_x)
    .attr('x2', vertical_x)
    .attr('y1', horizontal_y)
    .attr('y2', bar_height-horizontal_y)
    .attr('stroke', 'white')

    x_line = stationary_bar_svg_group.append('line')
    .attr('id', 'bar_x_line')
    .attr('x1', (vertical_x))
    .attr('x2', bar_width)
    .attr('y1', bar_height-horizontal_y)
    .attr('y2', bar_height-horizontal_y)
    .attr('stroke', 'white')

    //Y text is delta t

    let y_delta_t_text = stationary_bar_svg_group.append('text')
    .attr('id', 'bar_y_delta_t_text')
    .attr('x', vertical_x/2)
    .attr('y', bar_height/2)
    // .attr('transform', `rotate(0, ${vertical_x/2}, ${bar_height/2})`)
    .text('&Delta;t')
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')


    // x scale depends on period_sub
   
    change_x_sine_scale()
    // note_color_wheel



    //creating grid for amplitude
    
    // // Create a logarithmic scale from 1 to 20
    // const logScale = d3.scaleLog()
    //     .domain([1, max_periods_considered+1])
    //     .range([bar_height-horizontal_y, horizontal_y]);
    
    // // Generate values from 1 to 20 for the lines
    // const y_values_for_lines = [];
    // for (let i = 1; i <= max_periods_considered+1; i++) {
    //     y_values_for_lines.push(logScale(i));
    // }

    // lines_for_amplitude = d3.line().x((d)=>d).y((d)=>d)

    // y_values_for_lines.forEach((y, i) => {
    //     stationary_bar_svg_group.append('line')
    //         .attr('x1', vertical_x)
    //         .attr('x2', bar_width)
    //         .attr('y1', y)
    //         .attr('y2', y)
    //         .attr('stroke', 'white')
    //         .attr('opacity', 0.3)
        
    //     // Only add labels for certain values to avoid overcrowding
    //     if (i === 1 || i === 2 || i === 5 || i === 10 || i === 20 || i=== 30 || i===50) {
    //         stationary_bar_svg_group
    //             .append('text')
    //             .attr('class', 'bar_amplitude_text')
    //             .attr('x', vertical_x/2+2)
    //             .attr('y', y+3)
    //             .attr('fill', 'white')
    //             .attr('font-size', '12px')
    //             .attr('text-anchor', 'middle')
    //             .text((i).toString())
    //     }
    // })

    // bar_x_scale = d3.scaleLinear().domain([1,2]).range([vertical_x+margin.right, bar_width-margin.right])
    // //TODO, change with max_overtones
    // bar_y_scale = d3.scaleLinear().domain([1,8]).range([horizontal_y,bar_height-(horizontal_y)])

    // let hertz_text = stationary_bar_svg_group.append('text')
    // .attr('id', 'bar_hertz_text')
    // .attr('x', bar_width/2)
    // .attr('y', bar_height)
    // .text('Hz')
    // .attr('text-anchor', 'middle')
    // .attr('fill', 'white')

}


function change_x_sine_scale(){
    // period_sub_min = parseFloat($('#t_sub_slider').attr('min'))
    
    period_sub_value = parseFloat($('#t_sub_slider').val())
    sine_x_scale = d3.scaleLinear().domain([0, period_sub_value]).range([vertical_x, bar_width])
    sine_y_scale = d3.scaleLinear().domain([-1,1]).range([bar_height-horizontal_y, horizontal_y])
}




function preprocess_for_visualization(note_pairs_per_bound,note_information){

    // console.log('preprocess', 'note_pairs: ',note_pairs_per_bound,
    //     '\n\n note_info: ',note_information)



    merged = [] 

    


 
    for(let index=0; index<note_pairs_per_bound.length; index++){

        for(let note_ind =0;note_ind<note_pairs_per_bound[index].notes_data.length; note_ind++){


            note = note_pairs_per_bound[index].notes_data[note_ind]

            information = {
                cycle: note.cycle,
                period: note.period,
                midi_number: note_information.midi_numbers[note.note_position],
                note_name: note_information.note_names[note.note_position]
            }
            merged.push(information)
        }

    }

    merged.sort((a,b)=> a.period-b.period)

    // console.log('merged',merged)
    return merged

}





function t_sine_data_constructor(note_periods, midi_numbers){



    // New plan, make only 4 points per each note period


    sine_wave_data = []

    //since each note period is the result for 2*pi, 
    // we can divide it into 4 points

    // we multiply period by 1000 to have miliseconds as unit

    // divide period with four points
    let points_to_map = 4
        

    let bass_note_period = note_periods[0][0] //bass note is always first
    for(let note_index=0; note_index<note_periods.length; note_index++){
        let first_period = note_periods[note_index][0] *1000
        //find the four points for each note_period
        for (let period_cycle_num_curr_note=0; period_cycle_num_curr_note<note_periods[note_index].length; period_cycle_num_curr_note++){
        

           
            for(let point_index=0; point_index<points_to_map; point_index++){
               // should yield, pi/2, pi, 3pi/2, 2pi 
                let index_x = (period_cycle_num_curr_note*points_to_map)+point_index
                let x = (index_x*first_period)/points_to_map
                let y = Math.sin((2*Math.PI/points_to_map)*point_index)

                sine_wave_data.push({
                    note_index: note_index,
                    midi_number: midi_numbers[note_index],
                    x: x,
                    y: y,
                    
                })
            }
                
        }
        
        
    
    }

    return sine_wave_data

    
    // // Plan is for each note, create its corresponding sinewave
    // // key points to remember, number of points for bass note depends on width
    // // while other notes depend on their frequency ratio with bass note
    // // therefore, we need to create a data structure that holds all sinewaves
    // // and then we can draw them

    // let sine_wave_data = []

    // let bass_note_period = note_periods[0][0] //bass note is always first
    // let bass_note_freq = 1/bass_note_period

    // let points_in_bass_note = 100

    // //We will change frequency for everynote to be respective to bass note
    // // so that we normalize frequencies. 

    // //temp
    // let amplitude=1

    // for(let note_index=0; note_index<note_periods.length; note_index++){

    //     //frequency of  current note
    
    //     let current_note_period = note_periods[note_index][0]
    //     let current_note_freq = 1/current_note_period

    //     //normalized frequency per each note
    //     normalized_frequency =  current_note_freq/(bass_note_freq/100)


    //     // do point numbers have to change? test
    //     points_to_map = Math.floor(points_in_bass_note *(current_note_freq/bass_note_freq))

    //     for(let point_index=0; point_index<points_to_map; point_index++){
    //         let x = (point_index/(points_to_map-1))*bar_width
    //         let y = Math.sin((normalized_frequency*point_index))
    //         sine_wave_data.push({
    //             note_index: note_index,
    //             midi_number: midi_numbers[note_index],
    //             x: x,
    //             y: amplitude*y,
    //             no_amp_y: y
    //         })
    //     }
    
    // }
    // /*
    // sine_wave_data structure:
    // [
    //     {
    //         note_index: 0,
    //         midi_number: 60,
    //         x: 0,
    //         y: 0,
    //         no_amp_y: 0
    //     },
    // ]
        
    // */ 
    // return sine_wave_data

}

/*

Recieves two structures:
note_pairs_per_bound = [{notes_data: (2) [{…}, {…}]}]
                        t_delta: 0
                        t_max: 0.003822250082178377
                        t_max_cycle: 1
                        t_max_note_position: 1
                        t_min: 0.003822250082178377
                        t_min_cycle: 1
                        t_min_note_position: 0
                        t_sub: 0.003822250082178377
}, ...]

preprocessed_data = {
    midi_numbers: (2) [60, 64]
    note_names: (2) ['C4', 'E4'],
    cycles: [2][1] (20),
    periods: [2][1] (20)

}
*/

//MAIN PIPELINE (UPDATE FUNCTION)

function visualize_stationary_tension(note_pairs_per_bound, preprocessed_data){
   
    //Should returndata information
    // we have one data strucure for sine waves
    // managed by tsine_wave_data_constructor

    //Data structure is [
    //0:[]
    //1:[]
    //]
    // where index is each note, 

    sine_wave_data = t_sine_data_constructor(preprocessed_data.note_periods, preprocessed_data.midi_numbers)


    let sine_lines = d3.select('#stationary_bar_svg_group')
    .selectAll('path.sine_lines')
    .data(sine_wave_data.filter(d=>d.x<=$('#t_sub_slider').val()/1))
    // .data(sine_wave_data.filter(d=>d.x%5==0)) //filtering to reduce amount of points drawn




    line_generator = d3.line()
    .x( d=> sine_x_scale(d.x))
    .y( d=> sine_y_scale(d.y))
    .curve(d3.curveCatmullRom)  // Use curve interpolation for smoother lines 
    
    
    sine_lines.enter()
    .append('path')
    .attr('class','sine_lines')
    .attr('d', (d)=>line_generator(sine_wave_data.filter(dd=>dd.note_index==d.note_index)))
    .attr('stroke', (d)=>note_color_wheel(d.note_index))
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('opacity', 0.5)


    sine_lines
    .attr('d', (d)=>line_generator(sine_wave_data.filter(dd=>dd.note_index==d.note_index)))
    .attr('stroke', (d)=>note_color_wheel(d.note_index))
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('opacity', 0.5)

    sine_lines.exit().remove()


    // bars_mixed= preprocess_for_visualization(note_pairs_per_bound,preprocessed_data)

 


    // bar_x_scale =  d3.scaleLinear().domain([bars_mixed[0].period,bars_mixed[bars_mixed.length-1].period]).range([vertical_x+margin.right, bar_width-margin.right])

    
    // bar_y_scale = d3.scaleLog()
    // .domain([1, max_periods_considered+1])
    // .range([bar_height-horizontal_y, horizontal_y]);

    // let bars = d3.select('#stationary_bar_svg_group')
    // .selectAll('rect.t_bars')
    // .data(bars_mixed)

    


    // bars.enter()
    // .append('rect')
    // .attr('class','t_bars')
    // .attr('x', (d)=>bar_x_scale(d.period))
    // .attr('y',(d)=>bar_y_scale(d.cycle+1))
    // .attr('width', hertz_bar_width)
    // .attr('height',(d)=>bar_y_scale(1)-bar_y_scale(d.cycle+1))
    // .attr('fill', 'white')
    // .attr('opacity', 0.5)
    // .attr('data-cycle', (d)=>d.cycle)

    // bars
    // .attr('x', (d)=>bar_x_scale(d.period))
    // .attr('y',(d)=>bar_y_scale(d.cycle+1))
    // // .attr('class', 'bar_hertz')
    // .attr('width', hertz_bar_width)
    // .transition()
    // .duration(duration_transition)
    // .attr('height', (d)=>bar_y_scale(1)-bar_y_scale(d.cycle+1))
    // // .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    // .attr('opacity', 0.5)

    // bars.exit().remove()



    // bars.exit().remove()


}
