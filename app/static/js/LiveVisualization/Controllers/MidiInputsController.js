
document.addEventListener("keydown", function(event) {  
    

    on=false
    if(event.key == 'Enter' && !on){
        on=true
            
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
                    //   MIDI.noteOn(0, 60, 127, 0);
                    // MIDI.noteOff(0, 60, 0.75);
                },
                onerror: function( e){
                    console.log(e)
                }
        
            })
        }

     
    
   
         
        if(navigator.requestMIDIAccess){
            console.log('MIENTES')
            navigator.requestMIDIAccess().then(midiSuccess, midiFailure)
        }
        return
    }


  });

function midiSuccess(midiAccess){
    console.log(midiAccess)
    midiAccess.addEventListener('statechange', midiStateChange)
    var inputs = midiAccess.inputs.values();
    console.log(inputs)
    for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
        // TODO: MAP THE INPUTS TO THE VISUALIZATION

        //HARDCODED TO my meme
        console.log('here')
        console.log(input.value.name)

        if(input.value.name == 'AKM320 [1]'){
            console.log('FOUND MIDI')

            input.value.onmidimessage = onMIDIMessage;
        }
    }
}
function onMIDIMessage(event){
    console.log(event)
    play_midi_event(event)
    
    visualization_pipeline(event)
}

midi_notes_played = []
function play_midi_event(event){

    if(event.data[0]==144){
        midi_notes_played.push(event.data[1])
        MIDI.noteOn(0, event.data[1], 127,0)
    }

    

else{
    
    
    console.log('here????')
     MIDI.noteOff(0, event.data[1], 0)
     midi_notes_played.splice(midi_notes_played.indexOf(event.data[1]),1)
    //  MIDI.chordOn(0, midi_notes_played, 127,0)




}
}
function midiStateChange(event){
    console.log(event)
}
function midiFailure(){
    console.log('MIDI failure')
}  

 