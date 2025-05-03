/**********  BARRA LATERAL  **********/
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('cont-menu');
    const catButton = document.getElementById('menu-icon');
    let sidebarVisible = false;

    function toggleSidebar() {
        if (sidebarVisible) {
            sidebar.style.left = '-250px'; 
        } else {
            sidebar.style.left = '0';
        }
        sidebarVisible = !sidebarVisible;
    }

    if (catButton) {
        catButton.onclick = toggleSidebar;
    }

    document.addEventListener('click', function(event) {
        if (sidebarVisible && !event.target.closest('#cont-menu') && event.target !== catButton && !event.target.closest('#menu-icon')) {
            sidebar.style.left = '-250px';
            sidebarVisible = false;
        }
    });
});

/**********  ROTAR  **********/
document.addEventListener('DOMContentLoaded', function() {
    const rotateMessage = document.getElementById('rotate-message');

    function checkOrientation() {
        if (window.innerWidth < window.innerHeight) {
            rotateMessage.classList.remove('hidden');
        } else {
            rotateMessage.classList.add('hidden');
        }
    }

    checkOrientation();

    window.addEventListener('resize', checkOrientation);
});

/**********  SCROLL  **********/
/*document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.parent');

    if (scrollContainer) {
        scrollContainer.style.scrollSnapType = 'y mandatory';
        scrollContainer.style.overflowY = 'scroll';
        scrollContainer.style.scrollBehavior = 'smooth';
        scrollContainer.style.overflowX = 'hidden';
    } else {
        console.error("No se encontró el contenedor principal para el scroll snapping.");
    }
});*/

/**********  TARKOV-CHANGES  **********/
document.addEventListener('DOMContentLoaded', () => {
    const rutaMapas = 'static/img/mapas/';
    const authToken = 'TU_AUTH_TOKEN_AQUI';

    function Mapas() {
        const url = 'https://api.tarkov-changes.com/v1/maps';
        const headers = {
            'Content-Type': 'application/json',
            'AUTH-Token': authToken,
        };

        fetch(url, {
            method: 'GET',
            headers: headers,
        })
        .then(response => {
            if (!response.ok) {
                console.error("Error en la respuesta de la API de mapas (tarkov-changes):", response.status);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.results) {
                mapasCarrusel(data.results);
            } else {
                console.error("Estructura de datos de mapas inesperada:", data);
                const mapasContainer = document.getElementById('mapasCarouselInner');
                if (mapasContainer) {
                    mapasContainer.textContent = 'Error al cargar la información de los mapas.';
                }
            }
        })
        .catch(error => {
            console.error('Error al obtener mapas (tarkov-changes):', error);
            const mapasContainer = document.getElementById('mapasCarouselInner');
            if (mapasContainer) {
                mapasContainer.textContent = 'Error al cargar la información de los mapas.';
            }
        });
    }

    function mapasCarrusel(maps) {
        const carouselInner = document.getElementById('mapasCarouselInner');
        if (!carouselInner) return;
        carouselInner.innerHTML = '';

        if (maps && Array.isArray(maps)) {
            maps
                .filter(map => map.Name.toLowerCase() !== 'sandbox' && 
                        map.Name.toLowerCase() !== 'terminal' &&
                        !(map.Name === 'Factory' && map["Map Internal Name"] === 'factory4_night'))
                .forEach((map, index) => {
                    const mapName = map.Name;
                    const carouselItem = document.createElement('div');
                    carouselItem.classList.add('carousel-item');
                    if (index === 0 && carouselInner.innerHTML === '') {
                        carouselItem.classList.add('active');
                    }

                    const imageName = mapName.toLowerCase().replace(/ /g, '_') + '.png';
                    const imageUrl = `${rutaMapas}${imageName}`;

                    const image = document.createElement('img');
                    image.src = imageUrl;
                    image.alt = mapName;
                    image.classList.add('d-block', 'w-100');

                    carouselItem.appendChild(image);
                    carouselInner.appendChild(carouselItem);
                });

            if (carouselInner.innerHTML === '') {
                carouselInner.textContent = 'No hay mapas disponibles para mostrar.';
            }

            const carousel = new bootstrap.Carousel(document.getElementById('mapasCarousel'));
        } else {
            carouselInner.textContent = 'No hay información de mapas disponible.';
        }
    }

    Mapas();
});

/**********  TARKOV.DEV  **********/
const searchInput = document.getElementById('searchInput');
const fleaMarketBody = document.getElementById('fleaMarketBody');
let allFleaMarketItems = [];

function FleaMarket() {
    const query = `
      query {
        items {
          name
          avg24hPrice
          low24hPrice
          high24hPrice
          lastOfferCount
        }
      }
    `;

    fetch('https://api.tarkov.dev/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ query }),
    })
    .then(response => {
        if (!response.ok) {
            console.error("Error en la respuesta de la API (Flea Market):", response.status);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        allFleaMarketItems = data.data.items;
        datosFleaMarket(allFleaMarketItems);
    })
    .catch(error => {
        console.error('Error al obtener datos del Flea Market:', error);
        if (fleaMarketBody) {
            fleaMarketBody.innerHTML = '<tr><td colspan="5">Error al cargar los datos del Flea Market.</td></tr>';
        }
    });
}

function datosFleaMarket(items) {
    if (!fleaMarketBody) return;
    fleaMarketBody.innerHTML = '';

    if (items && Array.isArray(items)) {
        items.forEach(item => {
            const row = fleaMarketBody.insertRow();
            const nameCell = row.insertCell();
            const avgPriceCell = row.insertCell();
            const lowPriceCell = row.insertCell();
            const highPriceCell = row.insertCell();
            const offerCountCell = row.insertCell();

            nameCell.textContent = item.name;
            avgPriceCell.textContent = item.avg24hPrice ? item.avg24hPrice.toLocaleString() : 'N/A';
            lowPriceCell.textContent = item.low24hPrice ? item.low24hPrice.toLocaleString() : 'N/A';
            highPriceCell.textContent = item.high24hPrice ? item.high24hPrice.toLocaleString() : 'N/A';
            offerCountCell.textContent = item.lastOfferCount ? item.lastOfferCount.toLocaleString() : 'N/A';
        });
    } else {
        fleaMarketBody.innerHTML = '<tr><td colspan="5">No hay datos del Flea Market disponibles.</td></tr>';
    }
}

searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const filteredItems = allFleaMarketItems.filter(item =>
        item.name.toLowerCase().includes(searchTerm)
    );
    datosFleaMarket(filteredItems);
});

FleaMarket();