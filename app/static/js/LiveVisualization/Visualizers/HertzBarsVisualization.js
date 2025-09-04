bar_x_scale = null
bar_y_scale = null
hertz_bar_width = null
hertz_bar_height = null

function create_bar_axis(){

    margin = {top: 20, right: 20, bottom: 30, left: 40}
    let bar_width = document.getElementById('bar_viz').clientWidth-margin.left-margin.right
    let bar_height = document.getElementById('bar_viz').clientHeight
    let legend_width =bar_width+margin.left+margin.right
    
    bar_svg = d3.select('#bar_viz')
    .append('svg')
    .attr('id', "bar_svg")
    .attr('width', bar_width)
    .attr('height', bar_height)
    .style('background-color', 'black');


    bar_group = bar_svg.append('g')
    .attr('id', 'bar_group')


    vertical_x = bar_width/12
    hertz_bar_width = bar_width/26
    horizontal_y = (bar_height/9)
    hertz_bar_height = bar_height

    y_line = bar_group.append('line')
    .attr('id', 'bar_y_line')
    .attr('x1', vertical_x)
    .attr('x2', vertical_x)
    .attr('y1', horizontal_y)
    .attr('y2', bar_height-horizontal_y)
    .attr('stroke', 'white')

    x_line = bar_group.append('line')
    .attr('id', 'bar_x_line')
    .attr('x1', (vertical_x))
    .attr('x2', bar_width)
    .attr('y1', bar_height-horizontal_y)
    .attr('y2', bar_height-horizontal_y)
    .attr('stroke', 'white')

    //temp

    //creating grid for amplitude

    y_values_for_lines = d3.range(1,9).map(d=>(bar_height) - (d*horizontal_y))

    lines_for_amplitude = d3.line().x((d)=>d).y((d)=>d)

    y_values_for_lines.forEach((y,i)=>{
        bar_group.append('line')
        .attr('x1', vertical_x)
        .attr('x2', bar_width)
        .attr('y1', y)
        .attr('y2', y)
        .attr('stroke', 'white')
        .attr('opacity', 0.3)

        
    bar_group
    .append('text')
    .attr('class', 'bar_amplitude_text')
    .attr('x', vertical_x/2+2)
    .attr('y', y+3)
    .attr('fill', 'white')
    .attr('font-size', '12px')
    .attr('text-anchor', 'middle')
    .text((8-i).toString())


    
    })


    bar_x_scale = d3.scaleLinear().domain([1,2]).range([vertical_x+margin.right, bar_width-margin.right])
    //TODO, change with max_overtones
    bar_y_scale = d3.scaleLinear().domain([1,8]).range([horizontal_y,bar_height-(horizontal_y)])

    // let hertz_text = bar_group.append('text')
    // .attr('id', 'bar_hertz_text')
    // .attr('x', bar_width/2)
    // .attr('y', bar_height)
    // .text('Hz')
    // .attr('text-anchor', 'middle')
    // .attr('fill', 'white')

}

function create_bars(harmonics_in_hertz){
    //structure of harmonics 
    /*
    midi_number:{
        hertz,
        position_in_harmonic,
        name_of_note (note)

    }


    */
    console.log('in bar_create harmonics',harmonics_in_hertz)

    let notes_ordered_in_number = Object.keys(harmonics_in_hertz).sort((a,b)=>a-b)

  

    bars_to_be_created = []

    for(note in harmonics_in_hertz){

        //note is the midi number

        bass_harmonics = harmonics_in_hertz[notes_ordered_in_number[0]]
        
        //getting the fundamental frequency
        pivot_hertz = bass_harmonics[0].hertz

    
        for(harmonic in harmonics_in_hertz[note]){
            bar_x = round_function(harmonics_in_hertz[note][harmonic].hertz/pivot_hertz,3)
            bar_y = harmonics_in_hertz[note][harmonic].position_in_harmonic
            if(bar_x>=2){
                pivot_hertz *=2
                bar_x = round_function(harmonics_in_hertz[note][harmonic].hertz/pivot_hertz,3)
            }
            bars_to_be_created.push({
                x:bar_x,
                y:bar_y,
                note:harmonics_in_hertz[note][harmonic].note,
                fundamental:harmonics_in_hertz[note][harmonic].fundamental
            })

        }
    

    }

    return bars_to_be_created



}


function visualize_hertz_bars(bars_to_be_created){

    console.log(bars_to_be_created)
    let bars = bar_group.selectAll('rect.bar_hertz')
    .data(bars_to_be_created);


    bars
    .enter()
    .append('rect')

    .attr('class', 'bar_hertz')


    .attr('x', (d)=>bar_x_scale(d.x))

    .attr('y', (d)=>bar_y_scale(d.y))
    .attr('width', hertz_bar_width)
    .transition()
    .duration(duration_transition)
    .attr('height', (d)=>(hertz_bar_height-hertz_bar_height/9)-bar_y_scale(d.y))
    .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    .attr('opacity', 0.5)

    bars

    .attr('x', (d)=>bar_x_scale(d.x))

    .attr('y', (d)=>bar_y_scale(d.y))
    .attr('class', 'bar_hertz')
    .attr('width', hertz_bar_width)
    .transition()
    .duration(duration_transition)
    .attr('height', (d)=>(hertz_bar_height-hertz_bar_height/9)-bar_y_scale(d.y))
    .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    .attr('opacity', 0.5)

    bars.exit().remove()


    let bar_note_text = bar_group.selectAll('text.note_names_in_bars')
    .data(bars_to_be_created)
    
    bar_note_text.enter()
    .append('text')
    .attr('class', 'note_names_in_bars')
    .attr('x',(d,i)=>bar_x_scale(d.x))
    .attr('y',hertz_bar_height)
    .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    .attr('text-anchor', 'start')
    .text((d)=>d.note)

    bar_note_text
    .attr('y',hertz_bar_height)
    .attr('fill', (d)=>note_color_wheel(position_in_grid[note_to_number[d.fundamental]]))
    .attr('text-anchor', 'start')
    .text((d)=>d.note)



    bar_note_text.exit().remove()

    // .on('mouseover', function(d){
    //     change_piano_color_on(d.note, true)
    // })
    // .on('mouseout', function(d){
    //     change_piano_color_on(d.note, false)
    // })
}





$(document).ready(function() {
    // create_bar_axis()
});