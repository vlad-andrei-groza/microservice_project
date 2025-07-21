const API_BASE = '/api/math';

function computePower() {
    const base = document.getElementById('base').value;
    const exponent = document.getElementById('exponent').value;
    fetch(`${API_BASE}/pow`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({base: parseInt(base), exponent: parseInt(exponent)})
    })
        .then(handleResponse)
        .then(data => {
            document.getElementById('pow-result').textContent = `Result: ${data.result}`;
        })
        .catch(err => showSnackbar(err.message))
}

function computeFibonacci() {
    const n = document.getElementById('fib_n').value;
    fetch(`${API_BASE}/fibonacci`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({n: parseInt(n)})
    })
        .then(handleResponse)
        .then(data => {
            document.getElementById('fib-result').textContent = `Result: ${data.result}`;
        })
        .catch(err => showSnackbar(err.message));
}

function computeFactorial() {
    const n = document.getElementById('fact_n').value;
    fetch(`${API_BASE}/factorial`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({n: parseInt(n)})
    })
        .then(handleResponse)
        .then(data => {
            document.getElementById('fact-result').textContent = `Result: ${data.result}`;
        })
        .catch(err => showSnackbar(err.message));
}

function showSnackbar(message) {
    const snackbar = document.getElementById("snackbar");
    snackbar.textContent = message;
    snackbar.className = "show";
    setTimeout(() => {
        snackbar.className = snackbar.className.replace("show", "");
    }, 3000);
}

function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(err => {
            throw new Error(err.errors ? err.errors[0].msg || JSON.stringify(err.errors) : response.statusText);
        });
    }
    return response.json();
}