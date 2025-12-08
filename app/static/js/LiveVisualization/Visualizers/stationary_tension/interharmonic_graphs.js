
y_scale_for_interharmonic_graph = null;
x_scale_for_interharmonic_graph = null;

let chart_height_line_graph=null
let chart_width_line_graph=null



function build_line_graph_for_interharmonic_modulation(div_id, only_weighted=false){

    $('#'+div_id).empty()

  // Get the div's client height
    chart_height_line_graph = document.getElementById(div_id).clientWidth;   
    chart_width_line_graph = chart_height_line_graph; // Square chart
    
    // Calculate y-axis domain from r_regions_with_weights

    if(only_weighted){
        r_regions_with_weights = r_regions_with_weights.filter(d => d.weight !== null);
    }
    const min_r = Math.min(...r_regions_with_weights.map(d => d.r_lower));
    const max_r = Math.max(...r_regions_with_weights.map(d => d.r_upper));
    


    //to match notegrid

    y_start = chart_height_line_graph/12
    y_end = chart_height_line_graph - y_start
    
    // Create SVG
    const svg = d3.select('#' + div_id)
        .append('svg')
        .attr('width', chart_width_line_graph)
        .attr('height', y_end )
        .attr('transform', `translate(0,${y_start})`)
        .style('background-color', 'black');
    
    // Create main group
    const chart_group = svg.append('g')
        .attr('id', 'r_region_chart_group');


    min_y = 2**(min_r/12)-1
    max_y = 2**(max_r/12)-1 
    
    // Create y-scale
    y_scale_for_interharmonic_graph = d3.scaleLinear()
        .domain([min_y, max_y])
        .range([y_end - y_start, 0]); // Inverted for SVG coordinates
    
    // // Filter regions that have a weight defined (not null)
    // const weighted_regions = r_regions_with_weights.filter(d => d.weight !== null);
    
    x_offset = 40; // Leave space for y-axis labels
    y_offset = 0;
    const chart_width_adjusted = chart_width_line_graph - x_offset;
    // Create background rectangles for weighted regions
    chart_group.selectAll('rect.region_background')
        .data(r_regions_with_weights)
        .enter()
        .append('rect')
        .attr('class', 'region_background')
        .attr('x', x_offset)
        .attr('y', d => y_scale_for_interharmonic_graph(2**(d.r_upper/12)-1) - y_offset) // Higher r value = lower pixel position
        .attr('width', chart_width_adjusted)
        .attr('height', d => y_scale_for_interharmonic_graph(2**(d.r_lower/12)-1) - y_scale_for_interharmonic_graph(2**(d.r_upper/12)-1) -y_offset)
        .attr('fill', d => d.color //{
            // if(d.weight !== null){
            //     return d.color;
            // }
            // return '#353535';
        //})
        )
        .attr('opacity', 0.3)
        // .attr('stroke', 'white')
        // .attr('stroke-width', 1);
    
    // Add y-axis
    const y_axis = d3.axisLeft(y_scale_for_interharmonic_graph);
    chart_group.append('g')
        .attr('class', 'y-axis')
        .attr('transform', `translate(${x_offset}, 0)`)
        .call(y_axis)
        .selectAll('text')
        .attr('fill', 'white');
    
    // Style axis lines
    chart_group.selectAll('.y-axis path, .y-axis line')
        .attr('stroke', 'white');
    
    // // Add labels for regions (optional)
    // chart_group.selectAll('text.region_label')
    //     .data(r_regions_with_weights)
    //     .enter()
    //     .append('text')
    //     .attr('class', 'region_label')
    //     .attr('x', chart_width / 2)
    //     .attr('y', d => (y_scale_for_interharmonic_graph(2**(d.r_lower/12)-1) + y_scale_for_interharmonic_graph(2**(d.r_upper/12)-1)) / 2)
    //     .attr('text-anchor', 'middle')
    //     .attr('fill', 'white')
    //     .attr('font-size', '12px')
    //     .text(d => `${d.label} (${d.weight})`);
    
    // return { svg, y_scale, chart_width, chart_height };


}


function ihm_linechart_pipeline(event){

    //filter the documents

    filtered_data = data_to_plot_interharmonic.filter(d =>
        d.note_combination == event.note_combination)


    // if cap is defined, filter by it
    if(ihm_cap != null || ihm_cap>0){
        filtered_data = filtered_data.filter(d => d.delta_f <= ihm_cap)
    }

      // If no data, clear points and return
    if (filtered_data.length === 0) {
        d3.select('#r_region_chart_group').selectAll('circle.ihm_point').remove();
        return;
    }
    
    x_axis_min = d3.min(filtered_data, d => d.average_f - d.delta_f/2);
    x_axis_max = d3.max(filtered_data, d => d.average_f + d.delta_f/2);

    // Create x-scale
    x_scale_for_interharmonic_graph = d3.scaleLinear()
        .domain([x_axis_min, x_axis_max])
        .range([40, chart_width_line_graph-40]); // Match the x_offset used in the chart

    draw_ihm_points(filtered_data);


    

}

function draw_ihm_points(filtered_data){
    // Select chart group
    const chart_group = d3.select('#r_region_chart_group');
    
    // Bind data to circles with key function for proper enter/update/exit
    const points = chart_group.selectAll('circle.ihm_point')
        .data(filtered_data);
    
    // EXIT: Remove old points
    points.exit()
        .transition()
        .duration(300)
        .attr('r', 0)
        .remove();
    
    // ENTER: Add new points
    points.enter()
        .append('circle')
        .attr('class', 'ihm_point')
        .attr('cx', d => x_scale_for_interharmonic_graph(d.average_f))
        .attr('cy', d => y_scale_for_interharmonic_graph(d.ratio))
        .attr('r', 2)
        .attr('fill', 'blue')
        .attr('opacity', 0.8)
        .attr('stroke', 'lightblue')
        .attr('stroke-width', 1)
        .style('cursor', 'pointer')
        .on('mouseover', function(event, d) {
            // Tooltip or highlight
            d3.select(this)
                .attr('r', 6)
                .attr('stroke-width', 2);
            
            // Optional: Show tooltip
            console.log('Harmonic pair:', event.harm_1_index, event.harm_2_index, 
                       'Notes:', event.note_1, event.note_2,
                       'Delta f:', event.delta_f, 'Avg f:', event.average_f);
        })  
        .on('mouseout', function(event, d) {
            d3.select(this)
                .attr('r', 2)
                .attr('stroke-width', 1);
        })
        .transition()
        .duration(500)
        .attr('r', 2);
    
    // UPDATE: Update existing points
    points
        .transition()
        .duration(500)
        .attr('cx', d => x_scale_for_interharmonic_graph(d.average_f))
        .attr('cy', d => y_scale_for_interharmonic_graph(d.ratio));
    
        
    // Add or update x-axis
    let x_axis_group = chart_group.select('g.x-axis');
    
    if (x_axis_group.empty()) {
        x_axis_group = chart_group.append('g')
            .attr('class', 'x-axis');
    }
    
    const y_end = document.getElementById('interharmonic_modulation_graph').clientWidth;
    const y_start = y_end / 12;
    
    const x_axis = d3.axisBottom(x_scale_for_interharmonic_graph)
        .ticks(5)
        .tickFormat(d3.format('.0f'));
    
    x_axis_group
        .attr('transform', `translate(0, ${y_end - y_start*1.95})`)
        .transition()
        .duration(500)
        .call(x_axis)
        .selectAll('text')
        .attr('fill', 'white');
    
    x_axis_group.selectAll('path, line')
        .attr('stroke', 'white');
    
    // Add x-axis label
    let x_label = chart_group.select('text.x-axis-label');
    if (x_label.empty()) {
        x_label = chart_group.append('text')
            .attr('class', 'x-axis-label')
            .attr('text-anchor', 'middle')
            .attr('fill', 'white')
            .attr('font-size', '12px');
    }
    
    x_label
        .attr('x', x_offset + chart_width_line_graph /  2)
        .attr('y', y_end - y_start )
        .text('Average Frequency (Hz)');
}