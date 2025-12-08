x_discreet_scale =null
y_discreet_scale = null


note_positions_in_grid={
    "C":0,"G":1,"D":2,"A":3,
    "E":4,"B":5,"F#":6,"Db":7,
    "Ab":8,"Eb":9,"Bb":10,"F":11
}
note_names =Object.keys(note_positions_in_grid)


color_scale_for_tension = d3.scaleLinear().domain([0,1]).range(['white','red'])

// // Weighting measure used for colors, 1st harmonic 1, 2nd harmonic 0.5, 0.33and so on
// weight_equation_for_harmonic = function(value){
//     return 1/value
// }
// max_harmonics defined in HarmonicCalculator
// weight_for_harmonic = d3.scaleLog()
// .domain([1,max_harmonics+1])
// .range([1, one_over_n_scale(max_harmonics+1)])

function calculate_tension_for_grid2(note_1, note_2){

    

   //if note_1 == nnote_2 return 0

   if(note_1[0].hertz == note_2[0].hertz){
    return 0

   }

    //list of ratioed ranges will contain =[none_dis,those_who_fall_in lesser dissonat, more dissonant]
    /*
  
    lessed_dissonant_ranges are = 2^0.125<=ratio<2^0.5,
                                2^2.5<=ratio<2^3.5,
                                2**(7.5/12)<ratio<2**8.5/12 
    dissonant are= 2**(0.5/12)<ratio<2**1.5/12    
                    2**(1.5/12)<ratio<2**2.5/12
                    2**(4.5/12)<ratio<2**5.5/12
    none_so_dis are the rest that fall between 2^0, 2^1
    */
    list_of_ratioed_ranges =[0,0,0]

     //  note1 contains an array of all harmonics
    for (harmonic in note_1){
        harmonic1_info = note_1[harmonic] 
        weight_for_harmonic = weight_equation_for_harmonic(parseInt(harmonic) +1)
        for (harmonic2 in note_2){

            harmonic2_info = note_2[harmonic2]

            delta_f = Math.abs(harmonic1_info.hertz-harmonic2_info.hertz)

            // get substract, if bigger smaller than 170, get punto medio
            if(delta_f>170){
                continue
            }
            middle_point = (harmonic1_info.hertz+harmonic2_info.hertz)/2
            ratio = delta_f/middle_point
            if(ratio >Math.pow(2,11/12)-1){
                continue
            }
            //If it reached here, then it is a delta that can be plotted
            list_of_ratioed_ranges[0] += 1*weight_for_harmonic

            // filtering for lesser dissonance
            // lessed_dissonant_ranges are = 2^0.125<=ratio<2^0.5,
            // 2^2.5<=ratio<2^3.5,
            // 2**(7.5/12)<ratio<2**8.5/12 
            if(Math.pow(2,0.125/12)-1<=ratio && ratio< Math.pow(2,0.5/12)-1 ){
                list_of_ratioed_ranges[1] += 1*weight_for_harmonic
            }
            else if(Math.pow(2,2.5/12)-1<=ratio && ratio< Math.pow(2,3.5/12)-1 ){
                list_of_ratioed_ranges[1] += 1*weight_for_harmonic
            }
            else if(Math.pow(2,7.5/12)-1<=ratio && ratio< Math.pow(2,8.5/12)-1 ){
                list_of_ratioed_ranges[1] += 1*weight_for_harmonic
            }

            //filtering for  more dissonant
            // dissonant are= 2**(0.5/12)<ratio<2**1.5/12    
            // 2**(1.5/12)<ratio<2**2.5/12
            // 2**(4.5/12)<ratio<2**5.5/12
            else if(Math.pow(2,0.5/12)-1<=ratio && ratio< Math.pow(2,2.5/12)-1 ){
                list_of_ratioed_ranges[2] += 1*weight_for_harmonic
            }
            else if(Math.pow(2,4.5/12)-1<=ratio && ratio< Math.pow(2,5.5/12)-1 ){
                list_of_ratioed_ranges[2] += 1*weight_for_harmonic
            }

        }

    }

    let less_dis_score = 0.7
    let dis_score =1
    // now we calculate for the color
    total_tension = ((less_dis_score * list_of_ratioed_ranges[1])+(dis_score*list_of_ratioed_ranges[2]))/list_of_ratioed_ranges[0]
    return total_tension


}

function calculate_tension_for_grid(note_1, note_2){

    //using note to number from HarmonicCalculator.js

    return tension_score_per_interval[Math.abs(((note_to_number[note_1] - note_to_number[note_2])%12))]

    
}

// $(document).ready(function() {

//     build_note_grid()});

function build_note_grid(){

    width_for_note_grid = document.getElementById('note_grid').clientWidth
    height_for_note_grid = document.getElementById('note_grid').clientHeight


let note_grid_svg = d3.select('#note_grid')
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



let text_offset = (x_start/2) -5

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

function create_squares_in_grid2(harmonics_in_hertz){
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
