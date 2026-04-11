const API_URL = "http://localhost:8000/api/products-grouped/";

let allData = {};
let currentCategory = null;

// 🚀 Cargar datos
fetch(API_URL)
  .then(res => res.json())
  .then(data => {
    allData = data;

    renderCategories(data);
    renderProducts(Object.values(data).flat());
  });

// 🧭 Categorías
function renderCategories(data) {
  const container = document.getElementById("categories");
  container.innerHTML = "";

  Object.keys(data).forEach(category => {
    const item = document.createElement("div");
    item.textContent = category;

    item.onclick = () => {
      currentCategory = category;
      renderProducts(data[category]);
    };

    container.appendChild(item);
  });
}

// 🧱 Render productos
function renderProducts(products) {
  const container = document.getElementById("products");
  container.innerHTML = "";

  products.forEach(p => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img src="${p.image}">
      <div class="card-body">
        <h3>${p.name}</h3>
        <p class="price">$${p.price}</p>
      </div>
    `;

    container.appendChild(card);
  });
}

// 🔍 Buscador
document.getElementById("search").addEventListener("input", e => {
  const text = e.target.value.toLowerCase();

  let products = currentCategory
    ? allData[currentCategory]
    : Object.values(allData).flat();

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(text)
  );

  renderProducts(filtered);
});