document.addEventListener('DOMContentLoaded', () => {
    const bid = document.querySelector('#id_start_bid')

    // Adjust starting bid input to display 2 decimal places
    // and to round to nearest 0.5
    if (bid) {
        bid.onchange = () => {
            if (bid.value % 0.5 > 0) {
                const roundBid = Math.round(bid.value*2)/2
                bid.value = roundBid;
            }
            if (bid.value.length <= 2) {
                bid.value = bid.value + '.00'
            } else if (bid.value.length >= 3) {
                bid.value = bid.value + '0'
            }                        
        }
    }
});