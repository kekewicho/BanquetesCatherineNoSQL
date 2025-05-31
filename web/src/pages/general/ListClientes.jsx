import { fetchClientes } from "../../services/clientes.service";
import { Button } from "../../components/atoms/button/Button";
import { formatDate } from "../../utils/date.utils";



export const ListClientes = ({ scope }) => {

    const clientes = fetchClientes();



    return (
        <div className="row gy-4">
            <div className="col-12 fs-3">Tus clientes</div>
            <div className="col-12">
                <table className="table">
                    <thead>
                        <tr className="fw-bold">
                            <td>Nombre</td>
                            <td>Teléfono</td>
                            <td>RFC</td>
                            <td>Dirección</td>
                            <td></td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            clientes.map(cliente => (
                                <tr key={cliente._id}>
                                    <td>{cliente.nombre} {cliente.apellido}</td>
                                    <td>{cliente.telefono}</td>
                                    <td>{cliente.rfc}</td>
                                    <td>{cliente.direccion.calle}, {cliente.direccion.ciudad}, {cliente.direccion.cp}</td>
                                    <td><Button className="bi bi-search" navigateTo={cliente._id}></Button></td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
            </div>
        </div>
    )
}