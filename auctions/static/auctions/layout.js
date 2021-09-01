document.addEventListener('DOMContentLoaded', () => {
    // User is on "create listing" page
    var bid = document.querySelector('#id_start_bid')

    // Adjust bid input on 'listing' page to display 2 decimal places
    // and to round to nearest 0.5
    if (!bid) {
        // User is on "listing" page
        var bid = document.querySelector('#id_bid')
        if (bid) {
            if (bid.value % 1 == 0) {
                bid.defaultValue = bid.value + '0'
            }
            // else if (bid.value.length >= 3) {
            //     bid.defaultValue = bid.value + '0'
            // }
            index = String(bid.value).indexOf('.')
            if (index === -1) {
                bid.value = bid.value + '.00';
            }
            while (index > bid.value.length - 3) {
                bid.value = bid.value + '0';
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
            index = String(bid.value).indexOf('.')
            if (index === -1) {
                bid.value = bid.value + '.00';
            }
            while (index > bid.value.length - 3) {
                bid.value = bid.value + '0';
            }
        }
    }

    // Updates countdown timer on listing page
    setInterval(function(){
        $("#timer").load(window.location.href + " #timer" );
  }, 100);

});