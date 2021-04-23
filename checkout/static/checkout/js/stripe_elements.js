// Core Logic/Payment Flow From: https://stripe.com/docs/payments/accept-a-payment
// CSS From: https://stripe.com/docs/stripe-js


var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var stripeClientSecret = $('#id_stripe_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
// Style Stripe Payment Element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style: style});
card.mount('#card-element');

// Validation Errors on Card
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Form Submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // Prevent Post
    ev.preventDefault();
    // Disable Card Element and Submit Button to Prevent Multiple Submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Call Confirm Card Payment Method and Send Card Info to Stripe
    stripe.confirmCardPayment(stripeClientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // Re-enable Card Element and Submit Button to Fix Error
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
