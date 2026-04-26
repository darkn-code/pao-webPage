const API_BASE_URL = 'http://localhost:8000/api/mothers-day/products/';

const productsGrid = document.querySelector('#products-grid');

function formatPrice(value) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
    }).format(Number(value));
}

function renderProducts(products) {
    if (!products.length) {
        productsGrid.innerHTML = '<p class="status">Aun no hay productos en el catalogo.</p>';
        return;
    }

    productsGrid.innerHTML = products.map((product) => `
        <article class="card">
            <img src="${product.image_url}" alt="${product.name}">
            <p>${product.description}</p>
            <span>${formatPrice(product.price)}</span>
        </article>
    `).join('');
}

async function loadProducts() {
    try {
        const response = await fetch(API_BASE_URL);

        if (!response.ok) {
            throw new Error('No se pudo cargar el catalogo.');
        }

        const products = await response.json();
        renderProducts(products);
    } catch (error) {
        productsGrid.innerHTML = `<p class="status">${error.message}</p>`;
    }
}

loadProducts();
