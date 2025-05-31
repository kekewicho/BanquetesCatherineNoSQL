import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchClienteById } from '../../services/clientes.service';

export const ClienteDetalle = ({ }) => {
    const { clienteId } = useParams();
    const [cliente, setCliente] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!clienteId) {
            setError("No se proporcionó un ID de cliente en la URL.");
            setLoading(false);
            return;
        }

        const cargarCliente = async () => {
            setLoading(true);
            setError(null);
            try {
                console.log(`Cargando cliente con ID: ${clienteId}`);
                const data = fetchClienteById(clienteId);
                if (data) {
                    setCliente(data);
                } else {
                    setError(`No se encontró ningún cliente con el ID: ${clienteId}`);
                }
            } catch (err) {
                console.error("Error al cargar el cliente:", err);
                setError(err.message || "Ocurrió un error al cargar los datos del cliente.");
            } finally {
                setLoading(false);
            }
        };

        cargarCliente();
    }, [clienteId]); // El efecto se re-ejecuta si clienteId cambia

    if (loading) {
        return <div className="container mt-5"><p className="text-center">Cargando información del cliente...</p></div>;
    }

    if (error) {
        return <div className="container mt-5"><p className="alert alert-danger text-center">Error: {error}</p></div>;
    }

    if (!cliente) {
        // Este caso podría ya estar cubierto por el estado de error si fetchClienteById devuelve null
        // y se establece un error. Sin embargo, es una buena comprobación adicional.
        return <div className="container mt-5"><p className="text-center">No se encontró información para el cliente especificado.</p></div>;
    }

    // Si llegamos aquí, tenemos datos del cliente para renderizar
    return (
        <div className="row gy-4">
            <div className="col-12">
                <div className="card">
                    <div className="card-header">
                        <h1>Detalles del Cliente: {cliente.nombre} {cliente.apellido}</h1>
                    </div>
                    <div className="card-body">
                        <p><strong>ID:</strong> {cliente._id}</p>
                        <p><strong>Usuario:</strong> {cliente.usuario}</p>
                        <p><strong>Nombre Completo:</strong> {cliente.nombre} {cliente.apellido}</p>
                        <p><strong>Teléfono:</strong> {cliente.telefono}</p>
                        <p><strong>RFC:</strong> {cliente.rfc}</p>
                        <p><strong>Rol:</strong> {cliente.role}</p>
                        <h2>Dirección</h2>
                        <p><strong>Calle:</strong> {cliente.direccion?.calle || 'N/A'}</p>
                        <p><strong>Ciudad:</strong> {cliente.direccion?.ciudad || 'N/A'}</p>
                        <p><strong>Código Postal:</strong> {cliente.direccion?.cp || 'N/A'}</p>
                    </div>
                </div>
            </div>
            <div className="col-12 fs-1 fw-bold">Eventos</div>
            <div className="col-12">
                {/* <table className="table">
                    <thead>
                        <tr>
                            <td>Fecha</td>
                            <td>Tipo</td>
                            <td>Evento</td>
                            <td>Cliente</td>
                            <td>Menu</td>
                            <td>Plantilla</td>
                            <td>Salon</td>
                            <td>Invitados</td>
                            <td></td>
                            <td></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            events.map(event => (
                                <tr key={event._id}>
                                    <td>{formatDate(event.fecha + " 00:00", "%d/%b")}</td>
                                    <td>{event.tipo}</td>
                                    <td>{event.descripcion}</td>
                                    <td>{event.cliente.nombre}</td>
                                    <td>{event.menu.map(menu => menu.nombre).join(", ")}</td>
                                    <td>{event.plantilla.length} colaboradores</td>
                                    <td>{event.salon.nombre}</td>
                                    <td>{event.invitados}</td>
                                    <td className={(event.validated ? "bi-check-circle-fill text-success" : "bi-x-circle-fill text-danger")}></td>
                                    <td><Button className="bi bi-search" navigateTo={`evento/${event._id}`}></Button></td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table> */}
            </div>
        </div>
    );
}