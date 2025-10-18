document.addEventListener('DOMContentLoaded', () => {

    // Productos
    const productosTable = document.getElementById('productos-table');
    if (productosTable) {
        fetch('/api/productos/')
            .then(res => res.json())
            .then(data => {
                const tbody = productosTable.querySelector('tbody');
                data.forEach(p => {
                    tbody.innerHTML += `<tr>
                        <td>${p.id}</td>
                        <td>${p.nombre}</td>
                        <td>${p.stock_actual}</td>
                        <td>${p.precio}</td>
                    </tr>`;
                });
            });
    }

    // Movimientos
    const movimientosTable = document.getElementById('movimientos-table');
    if (movimientosTable) {
        fetch('/api/movimientos/')
            .then(res => res.json())
            .then(data => {
                const tbody = movimientosTable.querySelector('tbody');
                data.forEach(m => {
                    tbody.innerHTML += `<tr>
                        <td>${m.id}</td>
                        <td>${m.producto}</td>
                        <td>${m.tipo}</td>
                        <td>${m.cantidad}</td>
                        <td>${m.fecha}</td>
                    </tr>`;
                });
            });
    }

    // Crear movimiento (solo Admin y Vendedor)
    if (['Administrador', 'Vendedor'].includes(userRole)) {
        const formMovimiento = document.getElementById('form-movimiento');
        if (formMovimiento) {
            formMovimiento.addEventListener('submit', e => {
                e.preventDefault();
                const producto_id = document.getElementById('producto_id').value;
                const tipo = document.getElementById('tipo').value;
                const cantidad = document.getElementById('cantidad').value;

                fetch('/api/movimientos/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        producto: producto_id,
                        tipo: tipo,
                        cantidad: cantidad
                    }),
                    credentials: 'same-origin'
                })
                .then(res => res.json())
                .then(data => {
                    if (data.id) location.reload();
                    else alert('Error al crear movimiento');
                });
            });
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
