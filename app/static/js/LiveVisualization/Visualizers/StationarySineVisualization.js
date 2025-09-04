bar_x_scale = null
bar_y_scale = null
hertz_bar_width = null
hertz_bar_height = null


bar_width = null
bar_height=null

top_n_notes = 5




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

    //creating grid for amplitude
    
    // Create a logarithmic scale from 1 to 20
    const logScale = d3.scaleLog()
        .domain([1, max_periods_considered+1])
        .range([bar_height-horizontal_y, horizontal_y]);
    
    // Generate values from 1 to 20 for the lines
    const y_values_for_lines = [];
    for (let i = 1; i <= max_periods_considered+1; i++) {
        y_values_for_lines.push(logScale(i));
    }

    lines_for_amplitude = d3.line().x((d)=>d).y((d)=>d)

    y_values_for_lines.forEach((y, i) => {
        stationary_bar_svg_group.append('line')
            .attr('x1', vertical_x)
            .attr('x2', bar_width)
            .attr('y1', y)
            .attr('y2', y)
            .attr('stroke', 'white')
            .attr('opacity', 0.3)
        
        // Only add labels for certain values to avoid overcrowding
        if (i === 1 || i === 2 || i === 5 || i === 10 || i === 20 || i=== 30 || i===50) {
            stationary_bar_svg_group
                .append('text')
                .attr('class', 'bar_amplitude_text')
                .attr('x', vertical_x/2+2)
                .attr('y', y+3)
                .attr('fill', 'white')
                .attr('font-size', '12px')
                .attr('text-anchor', 'middle')
                .text((i).toString())
        }
    })

    bar_x_scale = d3.scaleLinear().domain([1,2]).range([vertical_x+margin.right, bar_width-margin.right])
    //TODO, change with max_overtones
    bar_y_scale = d3.scaleLinear().domain([1,8]).range([horizontal_y,bar_height-(horizontal_y)])

    // let hertz_text = stationary_bar_svg_group.append('text')
    // .attr('id', 'bar_hertz_text')
    // .attr('x', bar_width/2)
    // .attr('y', bar_height)
    // .text('Hz')
    // .attr('text-anchor', 'middle')
    // .attr('fill', 'white')

}


function preprocess_for_visialization(note_pairs_per_bound,note_information){



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
    return merged

}

function visualize_stationary_bars(note_pairs_per_bound, note_information){
    // console.log('nnpppb',note_pairs_per_bound)
    // console.log('preproc',note_information)


    //mixing into a one dimensional array

    bars_mixed= preprocess_for_visialization(note_pairs_per_bound,note_information)

    console.log(bars_mixed)


    bar_x_scale =  d3.scaleLinear().domain([bars_mixed[0].period,bars_mixed[bars_mixed.length-1].period]).range([vertical_x+margin.right, bar_width-margin.right])

    
    bar_y_scale = d3.scaleLog()
    .domain([1, max_periods_considered+1])
    .range([bar_height-horizontal_y, horizontal_y]);

    let bars = d3.select('#stationary_bar_svg_group')
    .selectAll('rect.t_bars')
    .data(bars_mixed)

    // bars
    // // .append('rect')
    // .attr('class','t_bars')
    // .attr('x', (d)=>bar_x_scale(d.period))
    // .attr('y',(d)=>bar_y_scale(d.cycle))
    // .attr('width', hertz_bar_width)
    // .attr('height', (d)=>bar_y_scale(d.cycle))
    // .attr('fill', 'white')
    // .attr('opacity', 0.5)
    


    bars.enter()
    .append('rect')
    .attr('class','t_bars')
    .attr('x', (d)=>bar_x_scale(d.period))
    .attr('y',(d)=>bar_y_scale(d.cycle+1))
    .attr('width', hertz_bar_width)
    .attr('height',(d)=>bar_y_scale(1)-bar_y_scale(d.cycle+1))
    .attr('fill', 'white')
    .attr('opacity', 0.5)
    .attr('data-cycle', (d)=>d.cycle)

    bars
    .attr('x', (d)=>bar_x_scale(d.period))
    .attr('y',(d)=>bar_y_scale(d.cycle+1))
    // .attr('class', 'bar_hertz')
    .attr('width', hertz_bar_width)
    .transition()
    .duration(duration_transition)
    .attr('height', (d)=>bar_y_scale(1)-bar_y_scale(d.cycle+1))
    // .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    .attr('opacity', 0.5)

    bars.exit().remove()



    bars.exit().remove()


}
