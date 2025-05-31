// import { apiService } from './api.service'; // Descomentar cuando se integre con la API real


export const fetchEvents = (params = {}) => {
    console.log("Fetching events (dummy data) with params:", params);
    // Comentado para usar dummy data por ahora:
    // try {
    //     // El apiService.get ya maneja la construcción de la query string a partir del objeto params
    //     const events = await apiService.get('/banquet-admin/events', params);
    //     return events;
    // } catch (error) {
    //     console.error("Error fetching events:", error);
    //     return []; // Devuelve un array vacío en caso de error o maneja de otra forma
    // }

    // Dummy data
    const dummyEvents = [
        {
            "_id": "60d73f2a8b3c4d5e6f7a8b9c",
            "fecha": "2024-07-15", // Upcoming
            "tipo": "Boda",
            "descripcion": "Boda de Ana y Carlos",
            "menu": [
                {
                    "_id": "60d63b4a1b2c3d4e5f6a7b8c",
                    "nombre": "Ensalada César con Pollo",
                    "descripcion": "Clásica ensalada César con pollo a la parrilla.",
                    "tipo_platillo": "entrada",
                    "precio": 120.50,
                    "thumbnail": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                    "ingredientes": [
                        { "ingrediente": { "_id": "ing001", "descripcion": "Lechuga Romana", "unidad": "pz" }, "qty": 1 },
                        { "ingrediente": { "_id": "ing002", "descripcion": "Pechuga de Pollo", "unidad": "gr" }, "qty": 150 }
                    ]
                },
                {
                    "_id": "60d63b4a1b2c3d4e5f6a7b8e",
                    "nombre": "Filete Mignon",
                    "descripcion": "Tierno filete mignon en salsa de champiñones.",
                    "tipo_platillo": "plato_fuerte",
                    "precio": 350.75,
                    "thumbnail": "https://images.unsplash.com/photo-1604130092119-78512891627f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                    "ingredientes": [
                        { "ingrediente": { "_id": "ing003", "descripcion": "Filete de Res", "unidad": "gr" }, "qty": 250 }
                    ]
                }
            ],
            "plantilla": [
                { "_id": "staff001", "usuario": "mesero_luis", "nombre": "Luis", "role": "mesero" },
                { "_id": "staff002", "usuario": "cocinero_pepe", "nombre": "Pepe", "role": "cocinero" }
            ],
            "salon": {
                "_id": "60d5f0f8b75e9b8a8b0974eb", // Salón Imperial
                "nombre": "Salón Imperial",
                "descripcion": "Un salón elegante para grandes eventos.",
                "capacidad": 200
            },
            "invitados": 150,
            "validated": true,
            "cliente": { "_id": "client001", "nombre": "Ana", "apellido": "Garcia" }
        },
        {
            "_id": "70e84g3b9c4d5e7f8a9b0c1d",
            "fecha": "2024-03-10", // Past
            "tipo": "Graduación",
            "descripcion": "Graduación Ingeniería 2024",
            "menu": [
                {
                    "_id": "60d63b4a1b2c3d4e5f6a7b8d", // Crema de Elote
                    "nombre": "Crema de Elote",
                    "descripcion": "Suave crema de elote con un toque de epazote.",
                    "tipo_platillo": "entrada",
                    "precio": 95.00,
                    "thumbnail": "https://images.unsplash.com/photo-1588665076405-8f5c4e0000b5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                    "ingredientes": [
                        { "ingrediente": { "_id": "ing004", "descripcion": "Elote Blanco", "unidad": "gr" }, "qty": 200 }
                    ]
                }
            ],
            "plantilla": [
                { "_id": "staff003", "usuario": "capitan_rosa", "nombre": "Rosa", "role": "capitan_meseros" }
            ],
            "salon": {
                "_id": "60d5f112b75e9b8a8b0974ec", // Jardín Esmeralda
                "nombre": "Jardín Esmeralda",
                "descripcion": "Hermoso jardín para eventos al aire libre.",
                "capacidad": 150
            },
            "invitados": 100,
            "validated": false,
            "cliente": { "_id": "client002", "nombre": "Carlos", "apellido": "Lopez" }
        }
    ];

    return dummyEvents;
};

/**
 * Simula la obtención de detalles de un evento específico por su ID.
 * TODO: Reemplazar con la llamada real a la API.
 * Endpoint: GET /banquet-admin/events/{event_id}
 * @param {string} eventId - El ID del evento a recuperar.
 * @returns {Promise<object|null>} - Una promesa que resuelve al objeto del evento o null si no se encuentra.
 */
export const fetchEventById = (eventId) => {
    console.log(`Fetching event by ID (dummy data) for eventId: ${eventId}`);
    // Comentado para usar dummy data por ahora:
    // try {
    //     const event = await apiService.get(`/banquet-admin/events/${eventId}`);
    //     return event;
    // } catch (error) {
    //     console.error(`Error fetching event with ID ${eventId}:`, error);
    //     if (error.message.includes("404") || (error.response && error.response.status === 404)) {
    //         return null; // Evento no encontrado
    //     }
    //     throw error; // Relanzar otros errores
    // }

    // Dummy data para un evento específico (puedes ajustar el ID si es necesario)
    const dummyEventDetail = {
        "_id": "60d73f2a8b3c4d5e6f7a8b9c", // Asegúrate que este ID coincida con el que usarás para probar
        "fecha": "2025-12-24",
        "tipo": "Cena Navideña",
        "descripcion": "Cena familiar navideña en el Salón Imperial. Menú especial de temporada.",
        "menu": [
            {
                "_id": "60d63b4a1b2c3d4e5f6a7b8c", "nombre": "Pavo Relleno", "descripcion": "Delicioso pavo relleno horneado.", "tipo_platillo": "plato_fuerte", "precio": 450.00, "thumbnail": "https://images.unsplash.com/photo-1574667041000-02f0a5953988?auto=format&fit=crop&w=800&q=60"
            },
            {
                "_id": "menu002", "nombre": "Ensalada de Manzana Navideña", "descripcion": "Ensalada fresca con manzana, nuez y un toque de canela.", "tipo_platillo": "entrada", "precio": 150.00, "thumbnail": "https://images.unsplash.com/photo-1571979195097-59e29905193e?auto=format&fit=crop&w=800&q=60"
            }
        ],
        "plantilla": [
            { "_id": "staff001", "usuario": "mesero_carlos", "nombre": "Carlos", "role": "mesero" },
            { "_id": "staff004", "usuario": "host_ana", "nombre": "Ana", "role": "host" }
        ],
        "salon": { "_id": "60d5f0f8b75e9b8a8b0974eb", "nombre": "Salón Imperial", "descripcion": "Un salón elegante para grandes eventos.", "capacidad": 200 },
        "invitados": 50,
        "validated": true,
        "cliente": { "_id": "60d5ecf7b75e9b8a8b0974ea", "nombre": "Juan", "apellido": "Perez", "telefono": "555-1234" }
    };

    // Simular que solo encontramos el evento si el ID coincide
    if (eventId === dummyEventDetail._id) {
        return dummyEventDetail;
    } else {
        console.warn(`Dummy event with ID ${eventId} not found. Returning null.`);
        return null; // Simula un 404 Not Found
    }
};




export const updateEvent = async (eventId, eventData) => {
    // TODO: Descomentar y probar cuando la API esté lista.
    // try {
    //     const updatedEvent = await apiService.put(`/banquet-admin/events/${eventId}`, eventData);
    //     return updatedEvent;
    // } catch (error) {
    //     console.error(`Error updating event with ID ${eventId}:`, error);
    //     // Considerar manejo específico de errores (ej. 404, 400)
    //     // throw error; // O relanzar para que el componente lo maneje
    //     return null;
    // }

    console.warn(`updateEvent está usando una simulación para el evento con ID: ${eventId}. Descomenta el código de API para uso real.`);
    // Simular una actualización exitosa devolviendo los datos enviados con el _id del evento
    // En una implementación real, el backend devolvería el evento completo y enriquecido.
    await new Promise(resolve => setTimeout(resolve, 500)); // Simular demora de red

    // Para la simulación, asumimos que eventData contiene la plantilla actualizada con IDs.
    // Devolvemos un objeto que se parezca al evento actualizado.
    // Lo ideal sería tener el evento original y fusionar los cambios.
    // Por ahora, solo devolvemos un objeto simple para indicar éxito.
    return { _id: eventId, ...eventData, message: "Evento actualizado (simulado)" };
};