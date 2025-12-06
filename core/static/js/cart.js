/**
 * Add item to cart using AJAX
 * @param {string} productId - Product ID
 * @param {number} quantity - Quantity to add (default: 1)
 */
function add_cart_item(productId, quantity = 1) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      getCookie('csrftoken');
    
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);

    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        
        if (data.status === 'success') {
            console.log('✓ Product added to cart');
            console.log('Cart Items:', data.cart_items);
            console.log('Total Items:', data.total_items);
            
            // Update UI if needed
            updateCartUI(data);
        } else {
            console.error('Error:', data.message);
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Fetch Error:', error);
        alert('Failed to add product to cart');
    });
}

/**
 * Get CSRF token from cookies
 * @param {string} name - Cookie name
 * @returns {string} Cookie value
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Update cart UI with cart data
 * @param {object} data - Response data from server
 */
function updateCartUI(data) {
    // Update cart counter with the correct class name
    const cartCounter = document.querySelector('.cart-item-count');
    if (cartCounter) {
        cartCounter.textContent = data.total_items;
    }
    
    // Trigger custom event for other components to listen
    document.dispatchEvent(new CustomEvent('cartUpdated', { detail: data }));
}

// Example usage:
// add_cart_item('5', 2);  // Add product with ID 5, quantity 2
