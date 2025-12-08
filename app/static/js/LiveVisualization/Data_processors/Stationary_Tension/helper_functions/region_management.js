/**
 * Insert a new region into r_regions_with_weights, handling overlaps and maintaining continuity
 * @param {Array} regions - The existing r_regions_with_weights array
 * @param {Object} newRegion - New region object with r_lower, r_upper, weight, label, color
 * @returns {Array} Updated regions array
 */
function insertRegion(regions, newRegion) {
    const { r_lower: newLower, r_upper: newUpper } = newRegion;
    
    // Validate new region
    if (newLower >= newUpper) {
        console.error('Invalid region: r_lower must be less than r_upper');
        return regions;
    }
    
    let updatedRegions = [];
    
    for (let region of regions) {
        const { r_lower, r_upper } = region;
        
        // Case 1: Existing region is completely before new region (no overlap)
        if (r_upper <= newLower) {
            updatedRegions.push({ ...region });
        }
        // Case 2: Existing region is completely after new region (no overlap)
        else if (r_lower >= newUpper) {
            updatedRegions.push({ ...region });
        }
        // Case 3: Existing region partially overlaps at the start (trim the end)
        else if (r_lower < newLower && r_upper > newLower && r_upper <= newUpper) {
            updatedRegions.push({
                ...region,
                r_upper: newLower
            });
        }
        // Case 4: Existing region partially overlaps at the end (trim the start)
        else if (r_lower >= newLower && r_lower < newUpper && r_upper > newUpper) {
            updatedRegions.push({
                ...region,
                r_lower: newUpper
            });
        }
        // Case 5: New region is completely inside existing region (split into two)
        else if (r_lower < newLower && r_upper > newUpper) {
            // Add the part before new region
            updatedRegions.push({
                ...region,
                r_upper: newLower
            });
            // The part after new region will be added after we insert the new region
            // Store it for later
            updatedRegions.push({
                ...region,
                r_lower: newUpper
            });
        }
        // Case 6: Existing region is completely inside new region (delete it)
        // Do nothing - region is not added to updatedRegions
    }
    
    // Insert the new region
    updatedRegions.push(newRegion);
    
    // Sort by r_lower to maintain order
    updatedRegions.sort((a, b) => a.r_lower - b.r_lower);
    
    return updatedRegions;
}

