
// y_scale

// function interharmonic graphs 

function create_ground_truth_bars_for_stationary_tension(div_id,gt_to_use){
        const div = document.getElementById(div_id);
    const width = div.clientWidth;
    const height = div.clientHeight;
    
    // Progress bar dimensions
    const bar_start_x = width / 6;
    const bar_end_x = width - (width / 6);
    const bar_width = bar_end_x - bar_start_x;
    const bar_y = height / 4;
    const bar_height = bar_y ; // Height of the progress bar
    const border_radius = bar_height / 2; // Makes it pill-shaped/circular
    
    // Calculate progress (0 to 1)
    const total_intervals = ground_truth_intervals.length;
    // const progress = current_index / total_intervals;
    // const filled_width = bar_width * progress;
    
    // Select or create SVG
    let svg = d3.select('#' + div_id).select('svg.progress_bar_svg');
    if (svg.empty()) {
        svg = d3.select('#' + div_id)
            .append('svg')
            .attr('class', 'progress_bar_svg')
            .attr('width', width)
            .attr('height', height)
            // .style('position', 'absolute')
            // .style('top', 0)
            // .style('left', 0)
            // .style('pointer-events', 'none'); // Allow clicks to pass through
    }
    
    let progress_group = svg.select('g.progress_group');
    if (progress_group.empty()) {
        progress_group = svg.append('g').attr('class', 'progress_group');
    }
    
    // Background bar (unfilled)
    let background_bar = progress_group.select('rect.progress_background');
    if (background_bar.empty()) {
        background_bar = progress_group.append('rect')
            .attr('class', 'progress_background');
    }
    
    background_bar
        .attr('x', bar_start_x)
        .attr('y', bar_y )
        .attr('width', bar_width)
        .attr('height', bar_height)
        .attr('rx', border_radius) // Rounded corners
        .attr('ry', border_radius)
        .attr('fill', '#333')
        .attr('stroke', 'white')
        .attr('stroke-width',1);
    
    // // Foreground bar (filled/progress)
    // let foreground_bar = progress_group.select('rect.progress_foreground');
    // if (foreground_bar.empty()) {
    //     foreground_bar = progress_group.append('rect')
    //         .attr('class', 'progress_foreground');
    // }
    
    // foreground_bar
    //     .transition()
    //     .duration(500)
    //     .attr('x', bar_start_x)
    //     .attr('y', bar_y - bar_height / 2)
    //     .attr('width', filled_width)
    //     .attr('height', bar_height)
    //     .attr('rx', border_radius)
    //     .attr('ry', border_radius)
    //     .attr('fill', 'lightgreen')
    //     .attr('opacity', 0.8);
    
    // // Progress text
    // let progress_text = progress_group.select('text.progress_text');
    // if (progress_text.empty()) {
    //     progress_text = progress_group.append('text')
    //         .attr('class', 'progress_text');
    // }
    
    // progress_text
    //     .attr('x', bar_start_x + bar_width / 2)
    //     .attr('y', bar_y + 5)
    //     .attr('text-anchor', 'middle')
    //     .attr('fill', 'white')
    //     .attr('font-size', '14px')
    //     .attr('font-weight', 'bold')

        // .text(`Ground Truth Interval: ${gt_to_use}`);
        // .text(`${current_index} / ${total_intervals}`);
    
    // Optional: Add tick marks for each interval
    const tick_positions = ground_truth_intervals.map((d, i) => {
        return bar_start_x + (bar_width * i) / total_intervals;
    });
    
    let ticks = progress_group.selectAll('line.progress_tick')
        .data(tick_positions);
    
    ticks.enter()
        .append('line')
        .attr('class', 'progress_tick')
        .merge(ticks)
        .attr('x1', d => d)
        .attr('x2', d => d)
        .attr('y1', bar_y - bar_height / 2 - 5)
        .attr('y2', bar_y - bar_height / 2)
        .attr('stroke', 'white')
        .attr('stroke-width', 1);
    
    ticks.exit().remove();


}