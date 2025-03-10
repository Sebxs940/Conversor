document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const amountInput = document.getElementById('amount');
    const fromCurrencySelect = document.getElementById('from-currency');
    const toCurrencySelect = document.getElementById('to-currency');
    const swapButton = document.getElementById('swap-currencies');
    const convertButton = document.getElementById('convert-button');
    const resultAmount = document.getElementById('result-amount');
    const resultDate = document.getElementById('result-date');
    const resultRate = document.getElementById('result-rate');
    const pairCards = document.querySelectorAll('.pair-card');
    
    // Format number with commas
    function formatNumber(number) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(number);
    }
    
    // Update the result section
    function updateResult(amount, fromCurrency, toCurrency, convertedAmount) {
        resultAmount.textContent = `${amount} ${fromCurrency} = ${formatNumber(convertedAmount)} ${toCurrency}`;
        resultRate.textContent = `1 ${fromCurrency} = ${formatNumber(convertedAmount / amount)} ${toCurrency}`;
        
        const now = new Date();
        resultDate.textContent = `Updated: ${now.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })}`;
    }
    
    // Convert currency
    async function convertCurrency() {
        const amount = parseFloat(amountInput.value);
        const fromCurrency = fromCurrencySelect.value;
        const toCurrency = toCurrencySelect.value;
        
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }
        
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount: amount,
                    from: fromCurrency,
                    to: toCurrency
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                updateResult(amount, fromCurrency, toCurrency, data.result);
            } else {
                alert('Conversion failed: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during conversion');
        }
    }
    
    // Swap currencies
    function swapCurrencies() {
        const fromValue = fromCurrencySelect.value;
        const toValue = toCurrencySelect.value;
        
        fromCurrencySelect.value = toValue;
        toCurrencySelect.value = fromValue;
    }
    
    // Event listeners
    convertButton.addEventListener('click', convertCurrency);
    
    swapButton.addEventListener('click', function() {
        swapCurrencies();
        convertCurrency();
    });
    
    // Handle popular currency pair clicks
    pairCards.forEach(card => {
        card.addEventListener('click', function() {
            const fromCurrency = this.getAttribute('data-from');
            const toCurrency = this.getAttribute('data-to');
            
            fromCurrencySelect.value = fromCurrency;
            toCurrencySelect.value = toCurrency;
            
            convertCurrency();
        });
    });
    
    // Initial conversion
    convertCurrency();
});
