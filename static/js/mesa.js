const BotonMostrarComidas = document.getElementById('btn_mostrar_comidas');
const BotonMostrarBebidas = document.getElementById('btn_mostrar_bebidas');



const mostrar_cards_platos = (categoria, tipo) => {

    console.log(categoria, tipo)

    fetch(`/tipos_categoria_tipo_comidas/?categoria='${categoria}'&tipo='${tipo}'`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        }).catch(error => {
            console.error('Error', error);
    })

}

const cargar_divs_tipo_categoria = (data, categoria) => {

    const DivContenedor = document.getElementsByClassName("contenedor-cards-tipo-comida")

    DivContenedor[0].innerHTML=''

    const fragment = document.createDocumentFragment();

    data.forEach(tipo => {
      const button = document.createElement("button");
      button.classList.add("card-tipo-comida");
      button.setAttribute("onclick", `mostrar_cards_platos(${categoria}, ${tipo})`);
      button.textContent = tipo;
      fragment.appendChild(button);
    });

    DivContenedor[0].appendChild(fragment);
}

const cargar_divs_tipo_categoria_tipo = (data) => {

    const DivCardsPlatos = document.getElementsByClassName("contenedor-cards-comidas")[0];

    DivCardsPlatos.innerHTML=''

    const fragment = document.createDocumentFragment();

    data.forEach(tipo => {
      const div = document.createElement("div");
      div.classList.add("card-comida");
      div.textContent = tipo;
      fragment.appendChild(div);
    });

    DivCardsPlatos.appendChild(fragment);
}

const cargar_tipo_categoria = (categoria) => {
    fetch(`/tipos_categoria_comidas/?categoria=${categoria}`)
        .then(response => response.json())
        .then(data => {
            cargar_divs_tipo_categoria(data, categoria)
        }).catch(error => {
            console.error('Error', error);
    })
}

const mostrar_platos = () => {

    BotonMostrarComidas.classList.add("btn-activo");
    if(BotonMostrarBebidas.classList.contains("btn-activo")){BotonMostrarBebidas.classList.remove("btn-activo")}

    cargar_tipo_categoria("comida");

}

const mostrar_bebidas = () => {
     BotonMostrarBebidas.classList.add("btn-activo");
    if(BotonMostrarComidas.classList.contains("btn-activo")){BotonMostrarComidas.classList.remove("btn-activo")}

    cargar_tipo_categoria("bebida");

}

mostrar_platos();
