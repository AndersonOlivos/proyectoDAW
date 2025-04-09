const BotonMostrarComidas = document.getElementById('btn_mostrar_comidas');
const BotonMostrarBebidas = document.getElementById('btn_mostrar_bebidas');
const DivContenedorSubcategorias = document.getElementsByClassName("contenedor-cards-subcategoria")[0]


const mostrar_divs_subcategoria = (data, categoria, tipo) => {


    DivContenedorSubcategorias.innerHTML = '';

    const fragment = document.createDocumentFragment();

    data.forEach(subcategoria => {
      const button = document.createElement("button");
      button.classList.add("card-subcategoria");
      button.setAttribute("onclick", `cargar_cards_platos('${categoria}', '${tipo}', '${subcategoria}')`);
      button.textContent = subcategoria;
      fragment.appendChild(button);
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

    if(categoria === "comida" && tipo === "platos" && subcategoria === ''){
        fetch(`/tipos_subcategorias_comidas/?categoria=${categoria}&tipo=${tipo}`)
        .then(response => response.json())
        .then(data => {
            DivContenedorSubcategorias.innerHTML = '';
            mostrar_divs_subcategoria(data, categoria, tipo)
        }).catch(error => {
            console.error('Error', error);
        })
    } else if (categoria === "comida" && tipo === "platos" && subcategoria !== '') {
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

    cargar_tipo_categoria("comida");
    cargar_cards_platos("comida", "entrantes", "")

}

const mostrar_bebidas = () => {
     BotonMostrarBebidas.classList.add("btn-activo");
    if(BotonMostrarComidas.classList.contains("btn-activo")){BotonMostrarComidas.classList.remove("btn-activo")}

    cargar_tipo_categoria("bebida");
    cargar_cards_platos("bebida", "vinos", "")

}

mostrar_platos();
