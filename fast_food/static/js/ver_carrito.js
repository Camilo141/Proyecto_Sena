
    const modal = document.getElementById("pedidoModal");

    function openModal() {
        modal.style.display = "flex";
    }

    function closeModal() {
        modal.style.display = "none";
    }

    // Cierra el modal al hacer clic fuera de él
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    };

