
//BAD PRACTICE
circle_of_fifth_svg = null

custom_sort_order = [0,7,2,9,4,11,6,1,8,3,10,5]

position_in_grid  = {
    0:0,
    7:1,
    2:2,
    9:3,
    4:4,
    11:5,
    6:6,
    1:7,
    8:8,
    3:9,
    10:10,
    5:11
}

color_wheel_for_tension_sum = null
note_color_wheel =null


// Bass note for color
bass_note=Infinity



tension_score_per_interval ={
    0:1,
    7:2,
    5:3,
    9:4,
    4:5,
    3:6,
    8:7,
    10:8,
    2:9,
    11:10,
    6:11,
    1:12

}

twelve_positions = d3.scaleLinear().domain([0,12]).range([0,360])

group_center_y = null;
group_center_x = null;
cof_bbox = null;
cof_radius = null;



//duration transition
duration_transition = 300


function create_cof_svg(){


    margin = ({top: 10, right: 30, bottom: 10, left: 30})

    const width = document.getElementById('main_viz').clientWidth;
    const height = document.getElementById('main_viz').clientHeight;


    
 
  legend_width=200
  legend_height =400


  //Colors for note representation
    colors = ["#FD4545", "#FC8145", "#FDB441" , "#FBD944", "#FCFA43", "#C2FC45", "#45FC4C", "#46FCEF", "#468EFC", "#8981FB", "#CC80FC", "#F973D4"]
    note_color_wheel = d3.scaleOrdinal().domain(d3.range(0,12)).range(colors)


  //colors for tension sum

  colors_for_sum_tension = ['#FFFFFF', '#303092','#662d92','#932691',"#07b4ce",'#24b14d','#8dc543','#fef305' , '#f9931f', '#f36523','#f1592d','#ee1b22']
  color_wheel_for_tension_sum = d3.scaleOrdinal().domain(d3.range(1,13)).range(colors_for_sum_tension)


  svg = d3.select('#main_viz')
    .append('svg')
      .attr('width', width-margin.left -margin.right)
      .attr('height', height -margin.top -margin.bottom)
      .style('border','1px solid black')
      .style('background-color', 'black');


    circle_of_fifth_svg = build_circle_of_fifths(svg, width, height)

    group_center_y = document.getElementById('circle_of_fifths').getBBox().height/2
    group_center_x = document.getElementById('circle_of_fifths').getBBox().width/2
    cof_bbox = document.getElementById('circle_of_fifths').getBBox()

    cof_radius = (group_center_x + group_center_y) /2

    
    
}



function build_circle_of_fifths(svg, width, height){



    const circle_radius = document.getElementById('main_viz').clientHeight/3,
    circle_margin = 50,
    circle_w = (circle_radius + margin) * 2,
    circle_h = (circle_radius + margin) * 2,
    start = circle_radius,
    hourTickLength = -18,
    radians = Math.PI / 180,
    labelRadius  = circle_radius + 20




    // CHANGE WIDTH 
    let group_of_circle = svg.append("g")
    .attr("class", "circle_of_fifths")
    .attr('id', 'circle_of_fifths')
    .attr("transform", `translate(${(width / 3)+margin.left+margin.right}, ${height / 2})`);

    //construct circle clock

    twelve_positions = d3.scaleLinear().domain([0,12]).range([0,360])

    let circle_of_fifths =group_of_circle
    .selectAll(".note_position")
    .data(d3.range(0, 12))
    .enter()
    .append("circle")
    .attr("class", "note_position")
    .attr("r", 1)
    .attr("cx", 0)
    
    .attr("cy", start)
    
    .attr("stroke", "white")
    .attr("fill", "white")
    .attr("stroke-width", 5)
    .attr("transform", d => `rotate(${twelve_positions(d)}), translate(0, ${0})`);

    //
    circle_notes = ["C","G","D","A","E","B","F#","Db","Ab","Eb","Bb","F"]

    let circle_of_fifths_text =group_of_circle
    .selectAll(".note_position_text")
    .data(d3.range(0,12))
    .enter()
    .append('text')
    
    .attr("class", (d)=> "note_position_text changeable_text "+circle_notes[d]+"_note")
    .attr('text-anchor', 'middle')
    .attr("x", d => labelRadius * Math.sin(twelve_positions(d) * radians))
    .attr(
      "y",
      d => -labelRadius * Math.cos(twelve_positions(d) * radians) 
    )
    .attr("font-size", 32)
    .attr("fill", "white")
    .text(d=>circle_notes[d])

    let circle_of_cof = group_of_circle
    .append("circle")
    .attr("class", "circle_of_cof")
    .attr("r", circle_radius)
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("stroke", "white")
    .attr("fill", "none")

    let lines_of_cof = d3.line()
    .x(function(d){return Math.sin(twelve_positions(d) * radians) * circle_radius})
    .y(function(d){return Math.cos(twelve_positions(d) * radians) * circle_radius})

    
    let circle_striped = group_of_circle

    
    .append('path')
    .attr("class", "circle_striped")
    .attr("stroke", "white")
    .attr('opacity', 0.4)
    .attr("d", lines_of_cof(d3.range(0,13)))

    let circle_lines = group_of_circle
    .selectAll('line')
    .data(d3.range(0,6))
    .enter()
    .append('line')
    .attr("class", "circle_lines")
    .attr('x1', -circle_radius)
    .attr('x2', circle_radius)
    .attr('y1', 0)
    .attr('y2', 0)
    .attr('opacity', 0.6)
    .attr('stroke', 'white')
    .attr('transform', d=>`rotate(${twelve_positions(d)})`)


    

    

    return group_of_circle


    
}

function calculate_sum_of_tension(harmonics_in_modulo_12){
    
    //Structure inside harmonics_in_modulo_12
    //is {note:{harmonics: strongness},
        //     note:{harmonics: strongness}},

    
   let notes_playing_mod_12 = Object.keys(harmonics_in_modulo_12)
   let max_interval_sum = 0
    for(let i =0; i<notes_playing_mod_12.length-1; i++){

        pivot_note_to_compare = notes_playing_mod_12[i]
        pivot_number = note_to_number[pivot_note_to_compare]
        max_interval = 0


        for(let j =i+1; j<notes_playing_mod_12.length; j++){
            note_to_compare = notes_playing_mod_12[j]
            note_number = note_to_number[note_to_compare]

            interval = Math.abs(note_number - pivot_number)
            if(tension_score_per_interval[interval] > tension_score_per_interval[max_interval] ){
                max_interval = interval
            }
            
        }

        console.log('max_interval: ',max_interval)
        console.log('note', notes_playing_mod_12[i])
        max_interval_sum += tension_score_per_interval[max_interval]
        
        

    }
    console.log('max_interval_sum: ',max_interval_sum)
   

    interval_score = Math.ceil(notes_playing_mod_12.length==1 ? max_interval_sum : max_interval_sum/(notes_playing_mod_12.length-1))
   console.log(interval_score)
    return interval_score
}
function create_paths(harmonics_in_modulo_12){

    //TODO, will more colors for paths be available??

    color_for_path = calculate_sum_of_tension(harmonics_in_modulo_12)

    //console.log('harmonics_in_modulo_12: ',harmonics_in_modulo_12)
    //Structure inside harmonics_in_modulo_12
    //is {note:{harmonics: strongness},
        //     note:{harmonics: strongness}},

    //get object keys and values

    paths_to_visualize = {}
    note_keys = Object.keys(harmonics_in_modulo_12)

    //defining x and y offsets
//TODO, make offsets dependant from screen
     x_offset = cof_bbox.width/10
     y_offset = cof_bbox.height/10

    //For each key inside of harmonic_in_modulo_12
    $(note_keys).each(function(index, note){

        
     keys_of_harmonics = Object.keys(harmonics_in_modulo_12[note])
     keys_of_harmonics.sort((a,b)=>position_in_grid[a]-position_in_grid[b])
    //  console.log('keys_of_harmonics: ',keys_of_harmonics)

     harmonics_of_note = harmonics_in_modulo_12[note]
     biggest_key = Object.keys(harmonics_of_note).reduce((a, b) => harmonics_of_note[a] > harmonics_of_note[b] ? a : b);
    //  console.log('biggest_key: ',biggest_key)
// 


        //order svg path by twelve_position value, 
        //smallest rotation goes first, biggest rotation goes last

        paths_to_visualize[note] = {
            path:[],
            color:color_for_path
        }



    // notes_in_harmonics_in_modulo_12 = Object.keys(harmonics_in_modulo_12).map(num=>parseInt(num))


    //

        $(keys_of_harmonics).each(function(index, harmonic){

            x_y_coords =[]
            // console.log('position_in_grid[harmonic]: ',position_in_grid[harmonic])
            rotation = twelve_positions(position_in_grid[harmonic])*(Math.PI/180)
            // console.log('rotation: ',rotation)
            division_factor_for_edge_amplitude = harmonics_of_note[biggest_key]/harmonics_of_note[harmonic]
            // console.log('division_factor_for_edge_amplitude: ',division_factor_for_edge_amplitude)

            let x = Math.sin(rotation) * ((cof_radius-x_offset)/(division_factor_for_edge_amplitude))
            // to make sure positive y is up, we need to multiply by -1     
            let y = (-1)*(Math.cos(rotation ) * ((cof_radius-y_offset)/(division_factor_for_edge_amplitude)))
       

            paths_to_visualize[note]['path'].push({
                x:x,
                y:y,
            

            })


        })



        



        
    })

    //returning paths to visualize, where each key contains one path
    // with their respective x and y coordinates
    // console.log('paths_to_visualize: ',paths_to_visualize)
    return paths_to_visualize
}


function set_bass_note_for_color(current_notes_playing){
    notes = Object.keys(current_notes_playing).map(num=>parseInt(num)).sort((a,b)=>a-b)

    
    bass_note= notes[0]
    
}


function visualize_paths_in_cof(paths_to_visualize, colors){


   

   
    // twelve_positions = d3.scaleLinear().domain([0,12]).range([0,360])

        //Checking where the x and y are
    let circle_of_fifth_svg = d3.select('#circle_of_fifths')




    
   

    if(Object.keys(paths_to_visualize).length == 0){
    let harmonic_paths = circle_of_fifth_svg.selectAll('.harmonic_paths')
        harmonic_paths.remove()
    return
    
    }
 

    // aqui lopear para crear los paths

    
    custom_paths_drawn =[]

    for(let note in paths_to_visualize)


    {
        // console.log('note: ',note)
        path_for_note = paths_to_visualize[note]['path']
        // console.log('path_for_note: ',path_for_note)

        let custom_path = d3.path()
        custom_path.moveTo(path_for_note[0].x, path_for_note[0].y)
        for(let i =1; i<path_for_note.length; i++){
            custom_path.lineTo(path_for_note[i].x, path_for_note[i].y)
        }
        custom_path.closePath()
        custom_paths_drawn.push({custom_path:custom_path, color:paths_to_visualize[note].color})
    

        



    }
    // console.log(custom_paths_drawn)
    


    let arcGenerator = d3.arc()
    .innerRadius(0)      // Inner radius
    .outerRadius(50)    // Outer radius
    .startAngle(0)       // Starting angle
    .endAngle(2 * Math.PI);

    

    let harmonic_paths = circle_of_fifth_svg.selectAll('.harmonic_paths')
    .data(custom_paths_drawn);


    harmonic_paths.enter()
    .append('path')
    .attr('class', 'harmonic_paths')
    .attr('fill', (d,i)=>color_wheel_for_tension_sum(d.color))
   
    .attr('d', arcGenerator())
    .transition()
    .duration(duration_transition)
    .attr('d', d=>d.custom_path.toString());   

    harmonic_paths.transition()
    .duration(duration_transition)

    .attr('d', d=>d.custom_path.toString())
    .attr('fill', (d,i)=>color_wheel_for_tension_sum(d.color))


    harmonic_paths.exit()
    
    
    .remove()
   






}


function change_colors_of_notes(colors_for_text){

    console.log('colors_for_text: ',colors_for_text)
    d3.selectAll('.changeable_text')
    .attr('fill', function(){
        let classes = this.getAttribute("class").split(" ");
        
        // Find the first class that has a color in the classColors object
        for (let cls of classes) {
            if (cls in colors_for_text) {
                return colors_for_text[cls];
            }
        }
        return "white"
    })
    // notes_playing = Object.keys(harmonics_in_hertz)
    // // console.log('notes_playing: ',notes_playing)
    // console.log('harmonics_in_hertz colors: ',harmonics_in_hertz)
    // d3.selectAll('.changeable_text')
    // .attr('fill', 'white')
    // $(notes_playing).each(function(index, note){

    //     note_name = number_to_note[note%12]
    //     // console.log('note: ',note)
    //     // console.log('note_color_wheel(note_to_number[note]): ',note_color_wheel(note_to_number[note]))
    //     d3.selectAll('.'+note_name+'_note')
    //     .attr('fill', note_color_wheel(note%12))
    // })
}

function get_colors_for_text(harmonic_in_modulo_12){
 

    // let notes_playing_mod_12 = Object.keys(harmonic_in_modulo_12)
    // console.log('hm_mod_12: ',notes_playing_mod_12 )
    colors_for_text = {}

    for(note in harmonic_in_modulo_12){
        colors_for_text[note+'_note']=note_color_wheel(position_in_grid[note_to_number[note]])
    }
    return colors_for_text
}

