import { apiService } from "./api.service"; // Descomentar cuando se integre con la API real
import { fetchEvents } from "./eventos.service.js";

export const fetchStaffMembers = (role) => {
    // TODO: Descomentar y probar cuando el endpoint de la API esté funcionando.
    // try {
    //     const params = {};
    //     if (role) {
    //         params.role = role;
    //     }
    //     const staffList = await apiService.get('/banquet-admin/staff', params);
    //     return staffList || []; // Devuelve un array vacío si la respuesta es null/undefined
    // } catch (error) {
    //     console.error("Error fetching staff members:", error);
    //     // Podrías optar por relanzar el error o devolver un array vacío según tu manejo de errores.
    //     // throw error;
    //     return []; // Devuelve un array vacío en caso de error para que la UI no falle.
    // }

    console.warn("fetchStaffMembers está usando datos dummy. Descomenta el código de API para uso real.");

    // Datos dummy
    const dummyStaff = [
        {
            "_id": "60d74a018b3c4d5e6f7a8b9d",
            "usuario": "mesero_carlos",
            "nombre": "Carlos",
            "apellido": "Rodriguez",
            "role": "COLABORADOR"
        },
        {
            "_id": "60d74a028b3c4d5e6f7a8b9e",
            "usuario": "cocinero_ana",
            "nombre": "Ana",
            "apellido": "Lopez",
            "role": "COLABORADOR"
        },
        {
            "_id": "60d74a038b3c4d5e6f7a8b9f",
            "usuario": "host_sofia",
            "nombre": "Sofia",
            "apellido": "Martinez",
            "role": "COLABORADOR"
        }
    ];


    if (role) {
        return dummyStaff.filter(staff => staff.role.toLowerCase() === role.toLowerCase());
    }
    return dummyStaff;
};



export const fetchAvailableStaffByDate = (dateString) => {
    console.warn(`fetchAvailableStaffByDate está usando datos dummy para los servicios fetchEvents y fetchStaffMembers. Descomenta el código de API para uso real.`);
    try {

        const eventsOnDate = fetchEvents({ from_date: dateString, to_date: dateString }); // Usando dummy sync por ahora


        const assignedStaffIds = new Set();
        eventsOnDate.forEach(event => {
            if (event.plantilla && event.plantilla.length > 0) {
                event.plantilla.forEach(staffMember => {
                    assignedStaffIds.add(staffMember._id);
                });
            }
        });

        
        const allStaff = fetchStaffMembers();


        const availableStaff = allStaff.filter(staffMember => !assignedStaffIds.has(staffMember._id));


        return availableStaff;

    } catch (error) {
        console.error(`Error fetching available staff for date ${dateString}:`, error);

        return [];
    }
};