x_discreet_scale =null
y_discreet_scale = null





note_positions_in_grid={
    "C":0,"G":1,"D":2,"A":3,
    "E":4,"B":5,"F#":6,"Db":7,
    "Ab":8,"Eb":9,"Bb":10,"F":11
}

reverse_note_positions_in_grid = Object.fromEntries(
    Object.entries(note_positions_in_grid).map(([key, value]) => [value, key])
);
note_names =Object.keys(note_positions_in_grid)


color_scale_for_tension = d3.scaleLinear().domain([0,0.4,0.7,1]).range(['lightgreen','yellow','orange','red'])

// // Weighting measure used for colors, 1st harmonic 1, 2nd harmonic 0.5, 0.33and so on
// weight_equation_for_harmonic = function(value){
//     return 1/value
// }
// max_harmonics defined in HarmonicCalculator
// weight_for_harmonic = d3.scaleLog()
// .domain([1,max_harmonics+1])
// .range([1, one_over_n_scale(max_harmonics+1)])



// $(document).ready(function() {

//     build_note_grid()});

function build_note_grid(div_id){

    // squares in grid that is why both client width and height are the same
    width_for_note_grid = document.getElementById(div_id).clientWidth
    height_for_note_grid = document.getElementById(div_id).clientWidth

    let note_grid_svg = d3.select('#'+div_id)
    .append('svg')
    .attr('width',width_for_note_grid)
    .attr('height',height_for_note_grid)
    .style('background-color', 'black')

    let note_grid = note_grid_svg.append('g')
    .attr('id','note_grid_group')

    // for each note, place a point in the grid

    y_start=  height_for_note_grid/12
    y_end =height_for_note_grid-(height_for_note_grid/24)
    x_start = width_for_note_grid/12
    x_end = width_for_note_grid-(width_for_note_grid/24)

    x_discreet_scale = d3.scaleLinear().domain([0,13]).range([x_start,x_end])
    y_discreet_scale = d3.scaleLinear().domain([0,13]).range([y_start,y_end])

    let twelve_notes = d3.range(0,13)
    let grid_coordinates = []

    let y_offset= y_end

    let vertical_grid_lines = note_grid.selectAll('line.vertical_grid_line')
    .data(twelve_notes)
    .enter()
    .append('line')
    .attr('class', 'grid_line')
    .attr('x1', (d,i)=>x_discreet_scale(d+1))
    .attr('x2', (d,i)=>x_discreet_scale(d+1))
    .attr('y1', y_start)
    .attr('y2',y_offset)
    .attr('stroke','white')
    .attr('opacity', 0.3)

    let horizontal_grid_lines = note_grid.selectAll('line.horizontal_grid_line')
    .data(twelve_notes)
    .enter()
    .append('line')
    .attr('class', 'grid_line')
    .attr('x1', x_start)
    .attr('x2', x_end)
    .attr('y1', (d,i)=>y_discreet_scale(d))
    .attr('y2', (d,i)=>y_discreet_scale(d))
    .attr('stroke','white')
    .attr('opacity', 0.3)



    let text_offset = (x_start/2) 

    let note_names_horizontal_text = note_grid.selectAll('text.note_names_horizontal_in_grid')
    .data(note_names)
    .enter()
    .append('text')
    .attr('class',(d)=> 'note_names_in_grid changeable_text '+d+"_note")
    .attr('x', (d,i)=>x_discreet_scale(i+1)+text_offset)
    .attr('y', y_offset)
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .text((d)=>d)

    let note_names_vertical_text = note_grid.selectAll('text.note_names_vertical_in_grid')
    .data(note_names)
    .enter()
    .append('text')
    .attr('class',(d)=> 'note_names_in_grid changeable_text  '+d+"_note")
    .attr('x', x_start*1.5 )
    .attr('y', (d,i)=>y_discreet_scale(i)+text_offset)
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .text((d)=>d)
        

}

function create_squares_in_stationary_tension_grid(harmonics_in_hertz){
    list_of_squares = []

    for(key in harmonics_in_hertz){
        x = note_positions_in_grid[harmonics_in_hertz[key][0].note]
        for(key2 in harmonics_in_hertz){
            y = note_positions_in_grid[harmonics_in_hertz[key2][0].note]
            color_for_square = calculate_tension_for_grid2(harmonics_in_hertz[key], harmonics_in_hertz[key2])
            console.log('tension_score', color_for_square)
            list_of_squares.push({x:x,y:y, color:color_for_square})
        }
    }

    return list_of_squares
}

function create_squares_in_grid(harmonics_in_modulo_12){
    
    list_of_squares = []

    for(key in harmonics_in_modulo_12){
        x = note_positions_in_grid[key]
        for(key2 in harmonics_in_modulo_12){
            y = note_positions_in_grid[key2]
            color_for_square = calculate_tension_for_grid(key, key2)
            list_of_squares.push({x:x,y:y, color:color_for_square})
        }
    }

    return list_of_squares
}


function visualize_squares_in_stationary_tension_grid(final_tension_score_per_note_combination){
       // Create symmetric data: for each document, create two squares (x,y) and (y,x)
    let symmetric_squares = [];
    
    final_tension_score_per_note_combination.forEach(doc => {
        // Original position
        let result = doc.note1_name.slice(0, -1);
        let note_num_mod12_2 = doc.note2_name.slice(0, -1);
        doc.x = note_positions_in_grid[result]
        doc.y = note_positions_in_grid[note_num_mod12_2]

        symmetric_squares.push({
            ...doc,
            position_x: doc.x,
            position_y: doc.y,
            is_symmetric: false
        });
        
        // Symmetric position (unless x === y, to avoid duplicates on diagonal)
        if (doc.x !== doc.y) {
            symmetric_squares.push({
                ...doc,
                position_x: doc.y,
                position_y: doc.x,
                is_symmetric: true
            });
        }
    });

    console.log('symmetric_squares:', symmetric_squares);
    
    let note_grid = d3.select('#note_grid_group');
    let squares = note_grid.selectAll('rect.clickable_square')
        .data(symmetric_squares);

    
    // Enter new squares
    squares
        .enter()
        .append('rect')
        .attr('class', 'clickable_square')
        .attr('x', d => x_discreet_scale(d.position_x + 1))
        .attr('y', d => y_discreet_scale(d.position_y))
        .attr('width', (x_end - x_start) / 13)
        .attr('height', (y_end - y_start) / 13)
        .attr('fill', d =>  color_scale_for_tension(d.normed_tension ))
        .attr('opacity', 0.8)
        .attr('stroke', d=> color_scale_for_tension(d.normed_tension ))
        .attr('stroke-width', 1)
        .style('cursor', 'pointer')  // Change cursor on hover
        .on('click', function(event, d,x) {
            // console.log(event)
            // console.log(d)
            // console.log(x)
            // // Handle click event
            // console.log('Clicked square:', d);


            
            
            // Highlight clicked square
            d3.selectAll('rect.clickable_square')
                .attr('stroke', d=> color_scale_for_tension(d.normed_tension ))
                .attr('stroke-width', 1);
            
            d3.select(this)
                .attr('stroke', 'white')
                .attr('stroke-width', 3);
            
            ihm_linechart_pipeline(event)
            // // Call the callback with document data
            // console.log('Document data for clicked square:', d);
        })
        .on('mouseover', function(event, d) {
            // Optional: Add hover effect
            d3.select(this)
                .attr('opacity', 1)
                .attr('stroke-width', 2);
        })
        .on('mouseout', function(event, d) {
            // Optional: Remove hover effect
            d3.select(this)
                .attr('opacity', 0.8)
                .attr('stroke-width', function() {
                    // Keep highlight if selected
                    return d3.select(this).attr('stroke') === 'yellow' ? 3 : 1;
                });
        });
    
    // Update existing squares
    squares
        .attr('x', d => x_discreet_scale(d.position_x + 1))
        .attr('y', d => y_discreet_scale(d.position_y))
        .attr('width', (x_end - x_start) / 13)
        .attr('height', (y_end - y_start) / 13)
        .attr('fill', d => color_scale_for_tension(d.normed_tension))
        .attr('opacity', 0.8);
    
    // Remove old squares
    squares.exit().remove();
}
function visualize_squares_in_grid(list_of_squares_with_color){

    note_grid = d3.select('#note_grid_group')
    let squares = note_grid.selectAll('rect.square')
    .data(list_of_squares_with_color)

    squares
    .enter()
    .append('rect')
    .attr('class', 'square')
    .attr('x', (d,i)=>x_discreet_scale(d.x+1))
    .attr('y', (d,i)=>y_discreet_scale(d.y))
    .attr('width', (x_end-x_start)/13)
    .attr('height', (y_end-y_start)/13)
    .attr('fill',(d)=>color_scale_for_tension(d.color))
    .attr('opacity', 1)

    squares.attr('x', (d,i)=>x_discreet_scale(d.x+1))
    .attr('y', (d,i)=>y_discreet_scale(d.y))
    .attr('width', (x_end-x_start)/13)
    .attr('height', (y_end-y_start)/13)
    .attr('fill',(d)=>color_scale_for_tension(d.color))
    .attr('opacity', 1)
    
    squares.exit().remove()



    
   
}
