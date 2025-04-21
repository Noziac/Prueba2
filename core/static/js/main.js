/**********  BARRA LATERAL  **********/
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('cont-menu'); // Selecciona el sidebar por su ID
    const catButton = document.getElementById('menu-icon'); // Selecciona el icono por su nuevo ID
    let sidebarVisible = false;

    function toggleSidebar() {
        if (sidebarVisible) {
            sidebar.style.left = '-250px'; // Oculta la barra lateral
        } else {
            sidebar.style.left = '0';        // Muestra la barra lateral
        }
        sidebarVisible = !sidebarVisible;
    }

    // Asigna la función al evento onclick del botón de categorías
    if (catButton) {
        catButton.onclick = toggleSidebar;
    }

    // Opcional: Cerrar la barra lateral al hacer clic fuera de ella
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
        if (window.innerWidth < window.innerHeight) { // Detecta si el ancho es menor que el alto (vertical)
            rotateMessage.classList.remove('hidden');
            // Opcional: Puedes ocultar el contenido principal aquí
            // document.querySelector('.parent').style.display = 'none';
        } else {
            rotateMessage.classList.add('hidden');
            // Opcional: Puedes mostrar el contenido principal aquí
            // document.querySelector('.parent').style.display = 'grid';
        }
    }

    // Verificar la orientación al cargar la página
    checkOrientation();

    // Verificar la orientación cuando cambia (al rotar el dispositivo)
    window.addEventListener('resize', checkOrientation);
});

/**********  BOTON VOLVER  **********/
document.getElementById("back-button").addEventListener("click", function () {
    window.history.back(); // Regresa a la página anterior
});



/**********  SCROLL  **********/
document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.parent'); // Reemplaza '.parent' con el selector correcto de tu contenedor principal

    if (scrollContainer) {
        scrollContainer.style.scrollSnapType = 'y mandatory'; // Activa el scroll snap verticalmente de forma obligatoria
        scrollContainer.style.overflowY = 'scroll'; // Permite el scroll vertical
        scrollContainer.style.scrollBehavior = 'smooth';
        scrollContainer.style.overflowX = 'hidden';
    } else {
        console.error("No se encontró el contenedor principal para el scroll snapping.");
    }
});