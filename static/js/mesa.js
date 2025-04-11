/* FUNCIONES PARA EL CARRITO */

const pTotalUnidadesPedido = document.getElementById('total-unidades-pedido');
let totalUnidades = 0;

const actualizarTotalUnidadesPedido = () => {pTotalUnidadesPedido.innerHTML = totalUnidades.toString();}

const actualizarCantidadProducto = (producto, cantidad) => {
    const CardProductoCarrito = document.getElementById(`producto_${producto.id_Producto}_carrito`);
    if(CardProductoCarrito){
        totalUnidades = totalUnidades + cantidad;
        const cantidadProductoCarrito = CardProductoCarrito.getElementsByClassName("card-pedido-carrito-cantidad")[0];
        const cantidadActualizada = parseInt(cantidadProductoCarrito.textContent) + cantidad;

        const subtotalProductoCarrito = CardProductoCarrito.getElementsByClassName("card-pedido-subtotal-precio")[0];
        subtotalProductoCarrito.innerHTML = `${cantidadActualizada * producto.precio} €`;

        if (cantidadActualizada === 0){
            CardProductoCarrito.remove();
        } else {
            cantidadProductoCarrito.innerHTML = cantidadActualizada;
        }
        actualizarTotalUnidadesPedido();
    } else {
        crearCardProductoCarrito(producto);
    }
}

const crearCardProductoCarrito = (producto) => {

    const contenedorPedidos = document.getElementsByClassName("contenedor-pedidos-carrito")[0];


// Crear el div principal
    const cardPedido = document.createElement("div");
    cardPedido.classList.add("card-pedido-carrito");
    cardPedido.id = `producto_${producto.id_Producto}_carrito`;

// Nombre del producto
    const nombreProducto = document.createElement("p");
    nombreProducto.classList.add("card-pedido-nombre");
    nombreProducto.textContent = producto.nombre;
    cardPedido.appendChild(nombreProducto);

// Div de cantidades y precio
    const cantidadesDiv = document.createElement("div");
    cantidadesDiv.classList.add("card-pedido-cantidades");

// Precio
    const precio = document.createElement("p");
    precio.classList.add("card-pedido-precio");
    precio.textContent = `${producto.precio}€`;
    cantidadesDiv.appendChild(precio);

// Cantidades con botones
    const cantidadesControl = document.createElement("div");
    cantidadesControl.classList.add("card-pedido-carrito-cantidades");

    const botonMenos = document.createElement("button");
    botonMenos.addEventListener("click", () => actualizarCantidadProducto(producto, -1));
    botonMenos.textContent = "-";

    const cantidad = document.createElement("p");
    cantidad.classList.add("card-pedido-carrito-cantidad");
    cantidad.textContent = "1";

    const botonMas = document.createElement("button");
    botonMas.addEventListener("click", () => actualizarCantidadProducto(producto, 1));
    botonMas.textContent = "+";

    cantidadesControl.appendChild(botonMenos);
    cantidadesControl.appendChild(cantidad);
    cantidadesControl.appendChild(botonMas);

    cantidadesDiv.appendChild(cantidadesControl);
    cardPedido.appendChild(cantidadesDiv);
    totalUnidades++;
    actualizarTotalUnidadesPedido();

// Subtotal
    const subtotalDiv = document.createElement("div");

    const textoSubtotal = document.createElement("p");
    textoSubtotal.classList.add("card-pedido-subtotal");
    textoSubtotal.textContent = "Subtotal";

    const subtotalPrecio = document.createElement("p");
    subtotalPrecio.classList.add("card-pedido-subtotal-precio");
    subtotalPrecio.textContent = `${producto.precio} €`;

    subtotalDiv.appendChild(textoSubtotal);
    subtotalDiv.appendChild(subtotalPrecio);

    cardPedido.appendChild(subtotalDiv);

// Añadir al contenedor
    contenedorPedidos.appendChild(cardPedido);
}

actualizarTotalUnidadesPedido();

/* FUNCIONES PARA MOSTRAR LAS CARDS DE LA CARTA */

const BotonMostrarComidas = document.getElementById('btn_mostrar_comidas');
const BotonMostrarBebidas = document.getElementById('btn_mostrar_bebidas');
const DivContenedorSubcategorias = document.getElementsByClassName("contenedor-cards-subcategoria")[0]

const cambiar_colores_botones = (a) => {

    const BotonComidas = document.getElementById('btn_mostrar_comidas').querySelector('img');
    const BotonBebidas = document.getElementById('btn_mostrar_bebidas').querySelector('img');

    if (a === "bebidas"){
        BotonComidas.src = "/static/image/comidas-marron.png";
        BotonBebidas.src = "/static/image/bebidas-blanco.png";
    } else if (a === "comidas") {
        BotonBebidas.src = "/static/image/bebidas-marron.png";
        BotonComidas.src = "/static/image/comidas-blanco.png";
    }
}

const mostrar_divs_subcategoria = (data, categoria, tipo) => {


    DivContenedorSubcategorias.innerHTML = '';

    const fragment = document.createDocumentFragment();

    data.forEach(subcategoria => {
        if( subcategoria != ""){
            const button = document.createElement("button");
            button.classList.add("card-subcategoria");
            button.setAttribute("onclick", `cargar_cards_platos('${categoria}', '${tipo}', '${subcategoria}')`);
            button.textContent = subcategoria;
            fragment.appendChild(button);
        }

    });

    DivContenedorSubcategorias.appendChild(fragment);
}

const mostrar_divs_tipo_categoria_tipo = (data) => {

    const DivCardsPlatos = document.getElementsByClassName("contenedor-cards-comidas")[0];

    DivCardsPlatos.innerHTML = '';

    const fragment = document.createDocumentFragment();

    data.forEach(tipo => {
    const card = document.createElement("div");
    card.classList.add("card-comida");


    const imgDiv = document.createElement("div");
    imgDiv.classList.add("card-comida-img");
    if (tipo.imagen) {
        const img = document.createElement("img");
        img.src = tipo.imagen;
        img.alt = tipo.nombre;
        imgDiv.appendChild(img);
    }


    const infoDiv = document.createElement("div");
    infoDiv.classList.add("card-comida-info");

    const nombre = document.createElement("p");
    nombre.classList.add("card-comida-nombre");
    nombre.textContent = tipo.nombre;

    const descripcion = document.createElement("p");
    descripcion.classList.add("card-comida-descripcion");
    descripcion.textContent = tipo.descripcion;

    const precioYBotonDiv = document.createElement("div");

    const precio = document.createElement("p");
    precio.classList.add("card-comida-precio");
    precio.textContent = `${tipo.precio}€`;

    const boton = document.createElement("button");
    boton.classList.add("card-comida-btn");
    boton.addEventListener("click", () => actualizarCantidadProducto(tipo, 1))
    boton.textContent = "+";

    // Armado
    precioYBotonDiv.appendChild(precio);
    precioYBotonDiv.appendChild(boton);

    infoDiv.appendChild(nombre);
    infoDiv.appendChild(descripcion);
    infoDiv.appendChild(precioYBotonDiv);

    card.appendChild(imgDiv);
    card.appendChild(infoDiv);

    fragment.appendChild(card);
    });

    DivCardsPlatos.appendChild(fragment);

}

const mostrar_divs_tipo_categoria = (data, categoria) => {

    const DivContenedor = document.getElementsByClassName("contenedor-cards-tipo-comida")

    DivContenedor[0].innerHTML=''

    const fragment = document.createDocumentFragment();

    data.forEach(tipo => {
      const button = document.createElement("button");
      button.classList.add("card-tipo-comida");
      button.setAttribute("onclick", `cargar_cards_platos('${categoria}', '${tipo}', '')`);
      button.textContent = tipo;
      fragment.appendChild(button);
    });

    DivContenedor[0].appendChild(fragment);
}

const cargar_cards_platos = (categoria, tipo, subcategoria) => {

    if(categoria === "Comida" && tipo === "Platos" && subcategoria === ''){
        fetch(`/tipos_subcategorias_comidas/?categoria=${categoria}&tipo=${tipo}`)
        .then(response => response.json())
        .then(data => {
            DivContenedorSubcategorias.innerHTML = '';
            mostrar_divs_subcategoria(data, categoria, tipo)
        }).catch(error => {
            console.error('Error', error);
        })
    } else if (categoria === "Comida" && tipo === "Platos" && subcategoria !== '') {
        fetch(`/tipos_categoria_tipo_comidas/?categoria=${categoria}&tipo=${tipo}&subcategoria=${subcategoria}`)
        .then(response => response.json())
        .then(data => {
            mostrar_divs_tipo_categoria_tipo(data)
        }).catch(error => {
            console.error('Error', error);
        })
    } else {
        fetch(`/tipos_categoria_tipo_comidas/?categoria=${categoria}&tipo=${tipo}&subcategoria=0`)
        .then(response => response.json())
        .then(data => {
            DivContenedorSubcategorias.innerHTML = '';
            mostrar_divs_tipo_categoria_tipo(data)
        }).catch(error => {
            console.error('Error', error);
        })
    }
}

const cargar_tipo_categoria = (categoria) => {

    DivContenedorSubcategorias.innerHTML = '';

    fetch(`/tipos_categoria_comidas/?categoria=${categoria}`)
        .then(response => response.json())
        .then(data => {
            mostrar_divs_tipo_categoria(data, categoria)
        }).catch(error => {
            console.error('Error', error);
    })
}

const mostrar_platos = () => {

    BotonMostrarComidas.classList.add("btn-activo");
    if(BotonMostrarBebidas.classList.contains("btn-activo")){BotonMostrarBebidas.classList.remove("btn-activo")}

    cambiar_colores_botones("comidas");
    cargar_tipo_categoria("Comida");
    cargar_cards_platos("Comida", "Entrantes", "")

}

const mostrar_bebidas = () => {
     BotonMostrarBebidas.classList.add("btn-activo");
    if(BotonMostrarComidas.classList.contains("btn-activo")){BotonMostrarComidas.classList.remove("btn-activo")}

    cambiar_colores_botones("bebidas");
    cargar_tipo_categoria("Bebida");
    cargar_cards_platos("Bebida", "Vinos", "")

}

mostrar_platos();