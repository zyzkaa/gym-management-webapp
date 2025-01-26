let paymentChosen = false;
let priceChosen = false;
let id
let button

function changePaymentForm() {
    let namem = 'method-' + id
    const method = document.querySelector(`input[name="${namem}"]:checked`)?.value;
    const div = document.getElementById('payment-method-form-' + id);
    div.innerHTML = ''
    paymentChosen = true;
    showButton()

    switch (method) {
        case 'credit_card':
            div.innerHTML = `
            <label for="card-number">Card Number:</label>
            <input type="text" id="card-number" name="card_number" required>
            
            <label for="expiry-date">Expiry Date:</label>
            <input type="text" id="expiry-date" name="expiry_date" required>
            
            <label for="cvv">CVV:</label>
            <input type="text" id="cvv" name="cvv" required>
            `;
            break;

        case 'paypal':
            div.innerHTML = `
            <label for="paypal-email">PayPal Email:</label>
            <input type="email" id="paypal-email" name="paypal_email" required>
            `;
            break;

        case 'bank_transfer':
            div.innerHTML = `
            <label for="account-number">Account Number:</label>
            <input type="text" id="account-number" name="account_number" required>
            
            <label for="bank-name">Bank Name:</label>
            <input type="text" id="bank-name" name="bank_name" required>
            `;
            break;

        default:
            break;

    }
}

function changePrice(){
    priceChosen = true
    showButton()
}

function showButton(){
    if (priceChosen && paymentChosen) {
        button.hidden = false;
    }
}

let form
function confirmPayment(){
    if(!form.checkValidity()){
        event.preventDefault();
        return;
    }
    button.disabled = true;
    let dots = ''

    let interval = setInterval(() => {
        dots = dots.length < 3 ? dots + '.' : ''
        button.textContent = 'processing' + dots
    }, 500)

    setTimeout(() => {
        clearInterval(interval)
        form.submit()
    }, 3000)
}

let isShown = false
let payment_cont
function showPayment(event, membership_id){
    event.preventDefault()
    if(!isShown){
        priceChosen = false
        paymentChosen = false
        form = document.getElementById('form-' + membership_id)
        button = document.getElementById('confirm-button-'+membership_id);
        payment_cont = document.getElementById(membership_id+'-form')
        id = membership_id
        payment_cont.style.display = 'block'
        isShown = true
        return
    }

    payment_cont.style.display = 'none'
    isShown = false

    if(membership_id !== id) {
        showPayment(event, membership_id)
    }
}