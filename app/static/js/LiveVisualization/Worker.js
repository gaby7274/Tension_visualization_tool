
self.addEventListener('message', function(e){
    self.importScripts('/static/js/HarmonicCalculator.js')
    let worker_id= e.data.worker_id
    let harmonics_in_ticks = null
    //console.log('Entramos??')
     switch(e.data.type_of_work){
         case 'merge_notes':

        let tracks_to_process_for_worker = e.data.tracks_for_worker
        let tick_list = e.data.tick_list
      
    
       harmonics_in_ticks = process_tracks(tracks_to_process_for_worker, tick_list)
    //    console.log('worker_id', worker_id)
    //    console.log('FINISHED')
    //    console.log(harmonics_in_ticks)
        self.postMessage({worker_id: worker_id, harmonics_in_ticks: harmonics_in_ticks})
         break
        
         case 'calculate_harmonics':
            let note_data = e.data.note_data
            let tickes_for_worker = e.data.ticks_for_worker
            // console.log( 'note_data: ', note_data)
            harmonics_in_ticks = divide_calculation_per_worker(note_data)
            self.postMessage({worker_id: worker_id, harmonics_in_ticks: harmonics_in_ticks})

            break

    }

}, false)



let process_tracks = function(tracks_to_process_for_worker, tick_list){
    
    let worker_ticks = tick_list
    
    //loop through tracks
    for(let current_track = 0; current_track<tracks_to_process_for_worker.length; current_track++){
        let events_for_current_track = tracks_to_process_for_worker[current_track]

        let current_notes_playing = {}
        let verbose = false

 

        let current_ticks_playing = {}
        //loop through events
        for(let current_event_index =0; current_event_index<events_for_current_track.length; current_event_index++){
            
            let current_event = events_for_current_track[current_event_index]
            
            

            //TODO: FIX THiS< FOR PERCUSSION

            if(current_event.track==11){
                break
            }
            if(current_event.name== 'Note on'){
                // console.log('NOTE ON')
                // console.log(current_event)

                // If note on, if the velocity is 0 that means note off, 
                // if not, it means note on
                
                if(current_event.velocity != 0){
                    current_notes_playing[current_event.noteNumber] = {
                        velocity:current_event.velocity,
                        track_id : current_event.track
                    }

                }
                else{
                    //Note off, delete from current_notes_playing
                    delete current_notes_playing[current_event.noteNumber]
                    
                }

                

                

                if(worker_ticks[current_event.tick] == null){
                    worker_ticks[current_event.tick] ={
                        notes_playing:{},
                        harmonics: {}
                    }

                }
               // worker_ticks[current_event.tick].notes_playing = {... worker_ticks[current_event.tick].notes_playing,...current_notes_playing}



                current_ticks_playing[current_event.tick] ={
                    notes_playing: {...current_notes_playing},
                   //harmonics: calculate_per_worker({...worker_ticks[current_event.tick].notes_playing,... current_notes_playing})
                } 


                
            }
            
            
        }
        for(let tick in current_ticks_playing){
            worker_ticks[tick].notes_playing = {...worker_ticks[tick].notes_playing, ...current_ticks_playing[tick].notes_playing}
            //worker_ticks[tick].harmonics = {...current_ticks_playing[tick].harmonics}
        }
        // worker_ticks = {...worker_ticks, ...current_ticks_playing}
    }

  


    return worker_ticks

    }

    let divide_calculation_per_worker = function(note_data){

        let harmonics_in_ticks = {}
        for(let tick in note_data){
            let notes_playing_in_tick = note_data[tick].notes_playing
            // console.log('notes_playing_in_tick: ', notes_playing_in_tick)
            let harmonics = calculate_per_worker(notes_playing_in_tick)
            harmonics_in_ticks[tick] = {}
            harmonics_in_ticks[tick].notes_playing = notes_playing_in_tick
            harmonics_in_ticks[tick].harmonics = harmonics
    
        }
        return harmonics_in_ticks
    }
    
