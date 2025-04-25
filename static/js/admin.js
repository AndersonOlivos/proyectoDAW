const BotonGenerarContrasenia = document.getElementById("btn-generar-contrasenia");
const InputContrasenia = document.getElementById("inp-contrasenia")
BotonGenerarContrasenia.addEventListener("click",function (){
     let contrasenia_generada = Array.from({length: 6}, () => Math.floor(Math.random() * 10)).join('');
     InputContrasenia.value = contrasenia_generada;
})