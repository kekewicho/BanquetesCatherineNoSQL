# Front end

## 1. General
### 1.1 Landing page
Muestra la informacion del procedimiento, politicas, salones de eventos, espacio para cotizador de eventos. Tiene boton para acceder al login.
### 1.2 Login
No tiene distinción de tipo de usuario, si no que es detectado junto con los datos del usuario que inicia sesion

## 2. Administrador banquetes
### 2.1 RH Plantilla
Permite dar de alta y baja colaboradores para que puedan ser usados en la planeaciones de horarios
### 2.1 RH Planeacion horarios
Permite armar horarios para los eventos, de manera que se asegure que las personas no chocan, etc
### 2.2 Provisionamiento
Pantalla principal con los ingredientes que se van a requerir para los eventos de los siguientes 15 dias y los ultimos surtidos de provisionamiento. Proporciona una manera de seleccionar un ingrediente en especifico.
### 2.2 Provisionamiento ingredientes detalles
Una vez que el usuario selecciona un ingrediente en especifico, aqui le decimos cuanto hay de ese ingrediente en almacen y los provisionamientos finalizados y pendientes.
### 2.3 Clientes
Listado de los clientes y lo necesario para buscarlos y seleccionarlos
### 2.3 Clientes detalles
Estan los detalles de los usuarios y sus eventos historicos
### 2.4 Eventos
Listado de eventos pendientes para los siguientes 15 dias, y da la opcion para ir a su detalle. Muestra tambien las notificaciones de los cambios que hacen los usuarios 
### 2.4 Eventos detalles
Despliega el detalle de los eventos

## 3. Clientes
### 3.1 Eventos <extends 2.3 Clientes detalles>
Muestra el listado de eventos que hay para un usuario en especifico, ademas del historico 
### 3.1 Eventos detalles <extends 2.4 Eventos detalles>
Proporciona una interfaz adicional para poder modificar el numero de invitados, hasta 3 dias antes del evento

## 4. Administradores Salones
### 4.1 Eventos <Extends 2.4 Eventos>
Despliega un listado de eventos para cierto salon en especifico para los siguientes 15 dias con la posibilidad de dar click para ver el detalle
### 4.2 Eventos detalle <Extends 2.4 Eventos detalles>
Extiende la misma interfaz, sin cambios

