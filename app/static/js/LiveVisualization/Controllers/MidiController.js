import MidiPlayer from 'midi-player-js'
import $ from 'jquery'

let amount_of_workers = 1

function change_amount_of_workers(){
    amount_of_workers = parseInt($('#amount_of_workers').val())
    console.log(amount_of_workers)
}

let MAX_WORKERS =8

let Player = new MidiPlayer.Player(function(event) {
	console.log(event);
});


let divide_calculation_per_worker = function(note_data){

    let harmonics_in_ticks = {}
    for(let tick in note_data){
        let notes_playing_in_tick = note_data[tick].notes_playing
        let harmonics = calculate_per_worker(notes_playing_in_tick)
        harmonics_in_ticks[tick] = {}
        harmonics_in_ticks[tick].notes_playing = notes_playing_in_tick
        harmonics_in_ticks[tick].harmonics = harmonics

    }
    return harmonics_in_ticks
}

function submit_midi(){
    alert('clicked')
    console.log($("#midi_file").prop('files'))

    let file = $("#midi_file").prop('files')[0]
    let file_reader = new FileReader()
    file_reader.onload = function(e){
        let data = e.target.result
        Player.loadDataUri(data)
        console.log(Player)

        //FOR CLASS PURPOSES ONLY

        // for(let i =1; i< MAX_WORKERS; i++){
        //     amount_of_workers =i
            let start_time = new Date().getTime()

        processMidiFileEvents(Player.getEvents(), Player.totalTicks).then(function(data){
            // console.log('FINISHED??????')
            // console.log(data)
            console.log('FINISHED')
            console.log('amount_of_workers', amount_of_workers)
            console.log('time: ', new Date().getTime() - start_time)
        })
    
    }
    file_reader.readAsDataURL(file)
    // Player.loadFile($("#midi_file").val());
    // console.log(Player)
    
}

$(document).ready(function(){

    document.getElementById('submit_midi_for_process').addEventListener('click',submit_midi)
    document.getElementById("amount_of_workers").addEventListener('change', change_amount_of_workers)

})

async function processMidiFileEvents(midi_events, total_ticks){

    //MASTER


    //MPI BARRIER??

    try{
        let tracks_processed = await process_tracks(midi_events, total_ticks)

        // console.log('tracks_processed', tracks_processed)


    //now merge all the information

    let merged_data = {
        
    }
    for(let worker_id in tracks_processed){
        
        for(let tick in tracks_processed[worker_id]){
            if(merged_data[tick] == null){
            merged_data[tick]={
                notes_playing:{}
            }
        }
            merged_data[tick].notes_playing = {...merged_data[tick].notes_playing, ...tracks_processed[worker_id][tick].notes_playing}
        }
    }


    //mpi Barrier????

    let processed_harmonics = await calculate_merged_harmonics(merged_data)
   

    
    for(let worker_id in processed_harmonics){
        
        for(let tick in processed_harmonics[worker_id]){
            if(merged_data[tick] == null){
            merged_data[tick]={
                notes_playing:{},
                harmonics:{}
            }
        }
            merged_data[tick].notes_playing = {...merged_data[tick].notes_playing, ...processed_harmonics[worker_id][tick].notes_playing}
            merged_data[tick].harmonics = {...merged_data[tick].harmonics, ...processed_harmonics[worker_id][tick].harmonics}
        }
    }




    return merged_data

    
    }catch(e){
        console.log(e)
    }

   
    

   



}

function calculate_merged_harmonics(merged_data){

    return new Promise(function(resolve, reject){
        let ticks = Object.keys(merged_data)
        let ticks_for_each_worker = Math.floor(ticks.length/amount_of_workers)
        let ranks_who_are_working_more = ticks.length % amount_of_workers

        let offset = 0
        let information_of_workers = {}

        for(let worker_id=0; worker_id<amount_of_workers; worker_id++){
            let start_index = (worker_id * ticks_for_each_worker) + offset
            let end_index = (start_index + ticks_for_each_worker)

            if(worker_id < ranks_who_are_working_more){
                end_index += 1
                offset+=1
            }



            let ticks_for_worker = ticks.slice(start_index,end_index)
            let data_to_send ={}
            ticks_for_worker.forEach(tick=>{
                data_to_send[tick] = merged_data[tick]
            })

        
            let worker = new Worker('/static/js/Worker.js')
            // let worker = list_of_workers[worker_id]j

            
            worker.postMessage({ticks_for_worker: ticks_for_worker,
                note_data: data_to_send,
                worker_id: worker_id,
                type_of_work: 'calculate_harmonics'
                })
            worker.onerror =function(e){
                reject(e)
            }
            worker.onmessage = function(e){
                let worker_id = e.data.worker_id
                information_of_workers[worker_id] = e.data.harmonics_in_ticks
                if(Object.keys(information_of_workers).length == amount_of_workers){
                    console.log('FINISHED')
                    console.log(information_of_workers)
                    resolve(information_of_workers)
                    worker.terminate()
                }
                else{
                    worker.terminate()
                }
            }
        



    }
})}


function process_tracks(midi_events, total_ticks){

    return new Promise(function(resolve, reject){
        let tick_list = {}

        let tracks_to_process = midi_events.slice(1)
        
        
        // Ranks that are lower than the residualget one job extra
        let amount_of_tracks_per_worker = Math.floor(tracks_to_process.length/amount_of_workers)
        let ranks_who_are_working_more = tracks_to_process.length % amount_of_workers

        //Offset will determine the start
        let offset = 0
        let information_of_workers ={}

        let list_of_workers = []
        for(let worker_id = 0; worker_id < amount_of_workers; worker_id++){
            list_of_workers.push(new Worker('/static/js/Worker.js'))
        }


        

        for(let worker_id =0; worker_id < amount_of_workers; worker_id++){

            //So por ejemplo, el primero conseguirá 0, hasta k-1 trabajo, pero 
            //si su id  está en ranks_who_are_working_more se jorobó, y trabaja mas
            let start_index = (worker_id * amount_of_tracks_per_worker) + offset
            let end_index = (start_index + amount_of_tracks_per_worker)

            if(worker_id < ranks_who_are_working_more){
                end_index += 1
                offset+=1
            }
            
            let tracks_for_worker = tracks_to_process.slice(start_index,end_index)
            // console.log('tracks_for_worker', tracks_for_worker)
            // console.log(

            //     'worker_id', worker_id,
            //     'amount_of_workers-1', amount_of_workers-1,
            // )
            
            //     console.log('worker_id', worker_id)
                
                
                
                let worker = list_of_workers[worker_id]
                
                worker.postMessage({
                    tracks_for_worker: tracks_for_worker,
                    tick_list: tick_list, 
                    worker_id: worker_id,
                    type_of_work: 'merge_notes'
                    })
                console.log('posted message')
                worker.onerror =function(e){
                    reject(e)
                }
                worker.onmessage = function(e){
                    console.log(e)
                    
                    let worker_id = e.data.worker_id
                    // console.log('worker', worker)

                    information_of_workers[worker_id] = e.data.harmonics_in_ticks
                    if(Object.keys(information_of_workers).length == amount_of_workers){
                        // console.log('FINISHED')
                        // console.log(information_of_workers)
                        resolve(information_of_workers)
                    }
                    else{
                        worker.terminate()
                    }

                }
            
        


        }
        
})}

// $('#submit_midi_for_process').click(function() {
//     alert('clicked')
//     Player.loadFile($('#midi_file').val());
//     console.log(Player)
    
// });

