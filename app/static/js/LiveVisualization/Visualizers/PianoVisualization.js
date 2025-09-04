audio_ctx = null
audio_enabled = false

notes_playing_keyboard ={}

keyboard_notes ={
    'q':'C',
    'w':'D',
    'e':'E',
    'r':'F',
    't':'G',
    'y':'A',
    'u':'B',
    '2':'Db',
    '3':'Eb',
    '5':'Gb',
    '6':'Ab',
    '7':'Bb',
    'z':'C2',
    'x':'D2',
    'c':'E2',
    'v':'F2',
    'b':'G2',
    'n':'A2',
    'm':'B2',
    's':'Db2',
    'd':'Eb2',
    'g':'Gb2',
    'h':'Ab2',
    'j':'Bb2',
    ',':'C3'

}

document.addEventListener('midimessage', visualization_pipeline)

//Note to midi global variable

key_note_to_midi ={
    'C':{
        midi_number:60,
    color:'white'},
    'D':{
        midi_number:62,
    color:'white'},
    'E':{
        midi_number:64,
    color:'white'},
    'F':{
        midi_number:65,
    color:'white'},
    'G':{
        midi_number:67,
    color:'white'},
    'A':{
        midi_number:69,
    color:'white'},
    'B':{
        midi_number:71,
    color:'white'},
    'C2':{
        midi_number:72,
    color:'white'
    },
    'D2':{
        midi_number:74,
    color:'white'},
    'E2':{
        midi_number:76,
    color:'white'},
    'F2':{
        midi_number:77,
    color:'white'},
    'G2':{
        midi_number:79,
    color:'white'},
    'A2':{
        midi_number:81,
    color:'white'},
    'B2':{
        midi_number:83,
    color:'white'},
    'Db':{
        midi_number:61,
    color:'black'},
    'Eb':{
        midi_number:63,
    color:'black'},
    'Gb':{
        midi_number:66,
    color:'black'},
    'Ab':{
        midi_number:68,
    color:'black'},
    'Bb':{
        midi_number:70,
    color:'black'},
    'Db2':{
        midi_number:73,
    color:'black'},
    'Eb2':{
        midi_number:75,
    color:'black'},
    'Gb2':{
        midi_number:78,
    color:'black'},
    'Ab2':{
        midi_number:80,
    color:'black'},
    'Bb2':{
        midi_number:82,
    color:'black'},
    'C3':{
        midi_number:84,
    color:'white'}



}
function change_piano_color_on(note_played, on=true){
 
   
    midi_note = key_note_to_midi[note_played]

    if(on){
        d3.select('#'+note_played).style('fill', 'lightgray')
    }
    else{
        d3.select('#'+note_played).style('fill', midi_note.color)
    }

    

}

function create_piano(){

    const controller_width =document.getElementById('controllers').clientWidth,
    controller_height = document.getElementById('piano_viz').clientHeight;

    margin = {top:10, right:10, bottom:10, left:20}
    piano_svg = d3.select('#piano_viz')
    .append('svg')
    .attr('width', controller_width)
    .attr('height', controller_height)
    .style('background-color', 'black');

    let piano = piano_svg.append('g')
    .attr('id', 'piano')

    let y_for_keys = controller_height/2.5
    let height_for_white_keys = controller_height/1.5

    let notes_to_be_present = 16

    let white_key_positions = d3.scaleLinear().domain([0,notes_to_be_present]).range([0,controller_width-margin.left])
    let key_names = ['C','D','E','F','G','A','B', 'C2','D2','E2','F2','G2','A2','B2','C3']
    let white_keys = piano
    .selectAll('rect.white_keys')
    .data(d3.range(0,15,1))
    .enter()
    .append('rect')
    .attr('x', (d,i)=>white_key_positions(i))
    .attr('y',y_for_keys)
    .attr('width', (controller_width-margin.left-margin.right)/notes_to_be_present)
    .attr('height', height_for_white_keys)
    .attr('id', (d,i)=>key_names[i])
    .style('border', '1px solid black')
    .style('fill', 'white')

    // BLACK KEYS 
    let black_key_names =[ 'Db','Eb','Gb','Ab','Bb', 'Db2','Eb2','Gb2','Ab2','Bb2']
    let black_key_height = controller_height/3
    let black_key_positions = d3.scaleLinear().domain([0,notes_to_be_present]).range([0,controller_width-margin.left])
    let black_keys_present = d3.range(0,14,1).filter((d)=>d!=2 && d!=6 && d!=9 && d!=13)
    let black_keys = piano
    .selectAll('rect.black_keys')
    .data(black_keys_present)
    .enter()
    .append('rect')
    .attr('x', (d,i)=>  black_key_positions(d+1)-black_key_positions(0.25))
    .attr('y', y_for_keys)
    .attr('width', ((controller_width-margin.left-margin.right)/notes_to_be_present)/2)
    .attr('height', black_key_height)
    .attr('id', (d,i)=>black_key_names[i])
    .style('border', '1px solid black')
    .style('fill', 'black')
    
    
   
}

function produce_midi_event(note_played, on=true){

    midi_notes = Object.values(notes_playing_keyboard).map((note)=>key_note_to_midi[note].midi_number)
    
    if(on){


        array_for_note = [144, midi_note.midi_number, 127]
      
        message = new MIDIMessageEvent("midimessage", {
            data: new Uint8Array(array_for_note),
            receivedTime: performance.now()
          });
    MIDI.chordOn(0, midi_notes, array_for_note[2],0)
        
    }
    else{
        
        array_for_note = [144, midi_note.midi_number, 0]
        message = new MIDIMessageEvent("midimessage", {
            
            data: new Uint8Array(array_for_note),
            receivedTime: performance.now()
          });
         MIDI.noteOff(0, note_played, 0)
         
       //  MIDI.chordOn(0, midi_notes, array_for_note[2],0)
    }
    
   
    document.dispatchEvent(message)
}
// Create a listener for the "r" button
document.addEventListener("keydown", function(event) {  
    on_note=true

  
    if(event.key == 'Enter'){
        if(!audio_enabled){
            audio_enabled=true
            MIDI.loadPlugin({
                soundfontURL: "/static/MIDI.js/examples/soundfont/",	
                instrument: "acoustic_grand_piano",
                onprogress: function(state, progress) {
                    console.log(state, progress);
                },
                
                onsuccess: function() {
                    console.log('MIDI ready')
                    MIDI.setVolume(0,127)
                    // MIDI.noteOn(0, 60, 127, 0);
                    // MIDI.noteOff(0, 60, 0.75);
                },
                onerror: function( e){
                    console.log(e)
                }
        
            })
        }

        return
    }
    if(keyboard_notes[event.key]===undefined){
    return   
    }
    else if(notes_playing_keyboard[event.key]===undefined){
        notes_playing_keyboard[event.key] = keyboard_notes[event.key]
        note_played = keyboard_notes[event.key]
    }

    else{
        return
    }
       
    

    change_piano_color_on(note_played, on_note)
    produce_midi_event(note_played,on_note)

  });

  

  document.addEventListener("keyup", function(event) {

    on_note=false
    if(notes_playing_keyboard[event.key]!==undefined){

        last_notes_played = Object.values(notes_playing_keyboard)
        delete notes_playing_keyboard[event.key]
        note_played = keyboard_notes[event.key]

    }
    else{
        return
    }
    
    

    change_piano_color_on(note_played, on_note)
    produce_midi_event(note_played, on_note, last_notes_played)




});




// $(document).ready(function(){
    
    

//    controller_svg =  create_piano()
// })





