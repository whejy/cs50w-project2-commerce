document.addEventListener('DOMContentLoaded', () => {
    var bid = document.querySelector('#id_start_bid')

    // Adjust bid input on l'isting' page to display 2 decimal places
    // and to round to nearest 0.5
    if (!bid) {
        var bid = document.querySelector('#id_bid')
        if (bid) {
            if (bid.value.length <= 2) {
                bid.defaultValue = bid.value + '.00'
            } else if (bid.value.length >= 3) {
                bid.defaultValue = bid.value + '0'
            }   
        }
    }

    // Adjust starting bid input on 'new' page to display 2 decimal places
    // and to round to nearest 0.5
    if (bid) {
        bid.onchange = () => {
            if (bid.value % 0.5 > 0) {
                const roundBid = Math.round(bid.value*2)/2
                bid.value = roundBid
            }
            if (bid.value.length <= 2) {
                bid.value = bid.value + '.00'
            } else if (bid.value.length >= 3) {
                bid.value = bid.value + '0'
            }                        
        }
    }
});