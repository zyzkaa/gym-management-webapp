let paymentChosen = false;
let priceChosen = false;
const button = document.getElementById('confirm-button')
const form = document.getElementById('payment-form');

function changePaymentForm() {

    const method = document.querySelector('input[name="method"]:checked')?.value;
    const div = document.getElementById('payment-method-form');
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

function confirmPayment(){
    button.disabled = true;
    let dots = ''

    let interval = setInterval(() => {
        dots = dots.length < 3 ? dots + '.' : ''
        button.textContent = `Processing${dots}`
    }, 500)

    setTimeout(() => {
        clearInterval(interval)
        form.submit()
    }, 3000)
}
