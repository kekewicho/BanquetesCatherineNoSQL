// import { apiService } from "./api.service";

export const fetchClientes = () => {

    // try {
    //     const clientes = await apiService.get('/banquet-admin/clients');
    //     return clientes;
    // } catch (error) {
    //     console.error("Error fetching clientes:", error);
    //     return []; // Devuelve un array vacío en caso de error o maneja de otra forma
    // }

    // Dummy data
    const dummyClientes = [
        {
            "_id": "60d5ecf7b75e9b8a8b0974ea",
            "usuario": "cliente_juan",
            "nombre": "Juan",
            "apellido": "Perez",
            "telefono": "555-1234",
            "rfc": "PEPJ800101XYZ",
            "direccion": {
                "calle": "Av. Siempreviva 742",
                "ciudad": "Springfield",
                "cp": "12345"
            },
            "role": "cliente"
        },
        {
            "_id": "60d5ecf7b75e9b8a8b0974eb",
            "usuario": "cliente_ana",
            "nombre": "Ana",
            "apellido": "Gomez",
            "telefono": "555-5678",
            "rfc": "GOMA850202ABC",
            "direccion": {
                "calle": "Calle Falsa 123",
                "ciudad": "Ciudad Ejemplo",
                "cp": "67890"
            },
            "role": "cliente"
        },
        {
            "_id": "60d5ecf7b75e9b8a8b0974ec",
            "usuario": "cliente_luis",
            "nombre": "Luis",
            "apellido": "Martinez",
            "telefono": "555-9012",
            "rfc": "MALU900303DEF",
            "direccion": {
                "calle": "Boulevard de los Sueños Rotos 45",
                "ciudad": "Metropolis",
                "cp": "11223"
            },
            "role": "cliente"
        }
    ];
    return dummyClientes;

}


export const fetchClienteById = (clientId) => {
    // TODO: Descomentar y probar cuando la API esté lista.
    // try {
    //     const cliente = await apiService.get(`/banquet-admin/clients/${clientId}`);
    //     return cliente;
    // } catch (error) {
    //     console.error(`Error fetching client with ID ${clientId}:`, error);
    //     if (error.message.includes("404") || (error.response && error.response.status === 404)) {
    //         return null; // Cliente no encontrado
    //     }
    //     // Podrías optar por relanzar el error o devolver null/undefined según tu manejo de errores global.
    //     throw error; // Relanzar otros errores para que el componente que llama pueda manejarlos.
    // }
    const dummyCliente = {
        "_id": clientId, // Usar el ID proporcionado para que parezca que lo encontró
        "usuario": `cliente_${clientId.slice(-4)}`,
        "nombre": "Cliente",
        "apellido": "Prueba",
        "telefono": "555-0000",
        "rfc": "XXXX000000XXX",
        "direccion": {
            "calle": "Calle Ficticia 123",
            "ciudad": "Ciudad Demo",
            "cp": "00000"
        },
        "role": "cliente"
    };

    // Para probar el caso de no encontrado, podrías hacer algo como:
    // if (clientId === "notfound") return null;

    return dummyCliente;
};
