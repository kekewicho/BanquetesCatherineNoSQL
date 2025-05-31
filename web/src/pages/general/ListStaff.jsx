import React, { useEffect, useState } from 'react';
import { fetchStaffMembers } from '../../services/staff.services'; // Ajusta la ruta si es necesario

export const ListStaff = ({ }) => {
    const [staffList, setStaffList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const cargarStaff = async () => {
            setLoading(true);
            setError(null);
            try {
                console.log("Cargando lista de personal...");
                const data = await fetchStaffMembers("COLABORADOR");
                if (data) {
                    setStaffList(data);
                } else {
                    // El servicio fetchStaffMembers ya podría devolver [] si no se encuentra,
                    // o podrías manejar el error aquí si el servicio lanza errores.
                    setError("No se pudo cargar la lista del personal o está vacía.");
                    setStaffList([]); // Asegurarse de que sea un array vacío
                }
            } catch (err) {
                console.error("Error al cargar el personal:", err);
                setError(err.message || "Ocurrió un error al cargar los datos del personal.");
                setStaffList([]); // Asegurarse de que sea un array vacío en caso de error
            } finally {
                setLoading(false);
            }
        };

        cargarStaff();
    }, []); // El efecto se ejecuta solo una vez al montar el componente

    if (loading) {
        return <div className="container mt-5"><p className="text-center">Cargando lista del personal...</p></div>;
    }

    if (error) {
        return <div className="container mt-5"><p className="alert alert-danger text-center">Error: {error}</p></div>;
    }

    return (
        <div className="container mt-4">
            <h1 className="mb-4">Lista de Personal</h1>
            {staffList.length === 0 ? (
                <p className="text-center">No hay miembros del personal para mostrar.</p>
            ) : (
                <div className="table-responsive">
                    <table className="table">
                        <thead className="thead-dark">
                            <tr>
                                <th scope="col">Usuario</th>
                                <th scope="col">Nombre</th>
                                <th scope="col">Apellido</th>
                                <th scope='col'>Rol</th>
                            </tr>
                        </thead>
                        <tbody>
                            {staffList.map((staff) => (
                                <tr key={staff._id}>
                                    <td>{staff.usuario}</td>
                                    <td>{staff.nombre}</td>
                                    <td>{staff.apellido}</td>
                                    <td>{staff.role}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
