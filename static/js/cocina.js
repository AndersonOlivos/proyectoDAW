const actualizar_linea_pedido = (estado, id_linea) => {
    fetch(`/actualizar_linea_pedido/?id_linea_pedido=${id_linea}&estado=${estado}`)
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    }).catch(error => {
        console.error('Error', error);
    })
}