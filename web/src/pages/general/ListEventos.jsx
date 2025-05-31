import { fetchEvents } from "../../services/eventos.service";
import { Button } from "../../components/atoms/button/Button";
import { formatDate } from "../../utils/date.utils";



export const ListEventos = ({ scope }) => {

    const events = fetchEvents();



    return (
        <div className="row gy-4">
            <div className="col-12 fs-3">Tus Eventos</div>
            <div className="col-12">
                <table className="table">
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
                </table>
            </div>
        </div>
    )
}