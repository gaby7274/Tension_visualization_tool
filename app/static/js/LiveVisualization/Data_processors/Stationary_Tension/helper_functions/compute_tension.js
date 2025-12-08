


function compute_ground_normalized_rankings(){


    //tanke rankings and create normalized ranking


    // get max ranking and min ranking to compute normalized 
    // ranking score
    let max_ranking = 13
    let min_ranking = 1



    for(let i=0; i<ground_truth_intervals.length; i++){
        ground_truth_intervals[i].normalized_ranking = (ground_truth_intervals[i].ranking - min_ranking) / (max_ranking - min_ranking)
   
    }

    for(let i=0; i<ground_truth_triads.length; i++){
        ground_truth_triads[i].normalized_ranking = (ground_truth_triads[i].ranking - min_ranking) / (max_ranking - min_ranking)
    }

    let min_explicit_rating = 1.667
    let max_explicit_rating = 5.259

    for(let i=0; i<ground_truth_triads.length; i++){
        ground_truth_triads[i].normalized_explicit_rating = (ground_truth_triads[i].explicit_rating - min_explicit_rating) / (max_explicit_rating - min_explicit_rating)
    }
    

}


$(document).ready(function(){
     compute_ground_normalized_rankings()
});