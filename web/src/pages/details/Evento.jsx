import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchEventById } from '../../services/eventos.service';
import { formatDate } from '../../utils/date.utils';
import { Image } from '../../components/atoms/image/Image';

const LoadingSpinner = () => (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '200px' }}>
        <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Cargando...</span>
        </div>
    </div>
);

const ErrorMessage = ({ message }) => (
    <div className="alert alert-danger" role="alert">
        {message}
    </div>
);

export const EventoDetalle = ({ scope }) => {
    const { eventId } = useParams();
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadEvent = async () => {
            if (!eventId) {
                setError("No se proporcionó ID de evento.");
                setLoading(false);
                return;
            }
            try {
                setLoading(true);
                setError(null);
                const eventData = await fetchEventById(eventId);
                if (eventData) {
                    setEvent(eventData);
                } else {
                    setError(`No se encontró ningún evento con el ID: ${eventId}`);
                }
            } catch (err) {
                console.error("Error al cargar el evento:", err);
                setError(err.message || "Ocurrió un error al cargar los detalles del evento.");
            } finally {
                setLoading(false);
            }
        };

        loadEvent();
    }, [eventId]);

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;
    if (!event) return <ErrorMessage message="Evento no encontrado." />;

    return (
        <div className="container mt-4">
            <nav aria-label="breadcrumb">
                <ol className="breadcrumb">
                    <li className="breadcrumb-item"><Link to="">Inicio</Link></li>
                    <li className="breadcrumb-item active" aria-current="page">Detalle del Evento</li>
                </ol>
            </nav>

            <div className="card shadow mt-5">
                <div className="card-header bg-secundario">
                    <h2 className="mb-0">{event.tipo}: {event.descripcion}</h2>
                </div>
                <div className="card-body">
                    <p><strong>ID Evento:</strong> {event._id}</p>
                    <p><strong>Fecha:</strong> {formatDate(event.fecha + " 00:00", "%A, %d de %B de %Y")}</p> {/* Asumiendo que fecha es YYYY-MM-DD */}
                    <p><strong>Salón:</strong> {event.salon.nombre} (Capacidad: {event.salon.capacidad})</p>
                    <p><strong>Invitados:</strong> {event.invitados}</p>
                    <p><strong>Validado:</strong> {event.validated ? <span className="badge bg-success">Sí</span> : <span className="badge bg-warning text-dark">No</span>}</p>
                    
                    <h5 className="mt-4">Cliente:</h5>
                    <p>{event.cliente.nombre} {event.cliente.apellido} {event.cliente.telefono && `(${event.cliente.telefono})`}</p>

                    <h5 className="mt-4">Menú Contratado:</h5>
                    {event.menu && event.menu.length > 0 ? (
                        <ul className="list-group list-group-flush">
                            {event.menu.map(item => (
                                <li key={item._id} className="list-group-item d-flex justify-content-between align-items-center">
                                    <div>
                                        {item.thumbnail && <Image src={item.thumbnail} alt={item.nombre} style={{ width: '50px', height: '50px', marginRight: '10px', borderRadius: '4px' }} />}
                                        {item.nombre} <small className="text-muted">({item.tipo_platillo})</small> - ${item.precio.toFixed(2)}
                                        <p className="mb-0 text-muted small">{item.descripcion}</p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : <p>No hay menú asignado.</p>}

                    <h5 className="mt-4">Personal Asignado (Plantilla):</h5>
                    {event.plantilla && event.plantilla.length > 0 ? (
                        <ul className="list-group list-group-flush">
                            {event.plantilla.map(staff => (
                                <li key={staff._id} className="list-group-item">
                                    {staff.nombre} ({staff.role}) - <span className="text-muted small">Usuario: {staff.usuario}</span>
                                </li>
                            ))}
                        </ul>
                    ) : <p>No hay personal asignado.</p>}
                </div>
            </div>
        </div>
    );
};