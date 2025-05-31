import { useState, useEffect } from "react";
import { Button } from "../../components/atoms/button/Button"
import { Image } from "../../components/atoms/image/Image"
import { fetchSalones, fetchMenus } from "../../services/public.service";

export const Landing = ({ }) => {
    const [salonesData, setSalonesData] = useState([]);
    const [menuData, setMenuData] = useState([]);

    const [selectedSalonId, setSelectedSalonId] = useState('');
    const [selectedMenuId, setSelectedMenuId] = useState('');
    const [guestCount, setGuestCount] = useState(10);
    const [eventDate, setEventDate] = useState('');

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [eventType, setEventType] = useState('');
    const [eventDescription, setEventDescription] = useState('');

    useEffect(() => {
        const loadInitialData = async () => {
            try {
                const salones = fetchSalones();
                setSalonesData(salones);
                if (salones.length > 0) setSelectedSalonId(salones[0]._id); 

                const menus = fetchMenus();
                setMenuData(menus);
                if (menus.length > 0) setSelectedMenuId(menus[0]._id); 
            } catch (error) {
                console.error("Error loading initial data:", error);
            }
        };
        loadInitialData();
    }, []);

    const handleOpenModal = () => setIsModalOpen(true);
    const handleCloseModal = () => setIsModalOpen(false);

    return (
        <>
            <div className="container">
                <div className="row py-3 gy-5">
                    {/* Header */}
                    <div className="col-12 d-flex justify-content-between align-items-center position-sticky bg-white py-2" style={{ top: "0", left: 0, zIndex: 1020 }}> {/* Aumentado z-index y fondo para visibilidad */}
                        <span className="fs-4 fw-bold d-flex align-items-center">
                            <Image src="LOGO.svg" style={{ height: "35px" }} className="me-3" />
                            Catherine Co.
                        </span>
                        <Button navigateTo="login" primary>Login</Button>
                    </div>
                    <div className="col-12 position-relative">
                        <Image src="boda.jpg" className="w-100 rounded rounded-4" style={{ height: "80vh", objectFit: "cover", objectPosition: "center", filter: "brightness(70%)" }} />
                        <div className="w-100 h-100 position-absolute top-0 start-0 d-flex align-items-center flex-column text-white justify-content-center">
                            <h1>Tu Evento Soñado Comienza Aquí</h1>
                            <h6>Crea memorias inolvidables con nuestro excepcional servicio de catering. Comienza cotizando tu evento.</h6>
                            <Button secondary className="px-5 mt-4">Ir a cotizar</Button>
                        </div>
                    </div>
                    <div className="col-12 d-flex flex-column align-items-center">
                        <div className="col-12 fs-4 fw-bold mb-4">Salones con convenio</div>
                        <div className="col-12 d-flex overflow-x-auto py-3">
                            {
                                salonesData.map(salon => (
                                    <div key={salon._id} className="col-12 col-md-4 col-lg-3 me-4 d-flex flex-column flex-shrink-0" style={{width: "280px"}}>
                                        <Image src={salon.thumbnail} className="rounded" style={{height: "180px", objectFit: "cover"}} />
                                        <b className="mt-2">{salon.nombre}</b>
                                        <p className="text-muted small">{salon.descripcion}</p>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                    <div className="col-12 d-flex flex-column align-items-center">
                        <div className="col-12 fs-4 fw-bold mb-4">Menú disponible</div>
                        <div className="col-12 d-flex overflow-x-auto py-3">
                            {
                                menuData.map(platillo => (
                                    <div key={platillo._id} className="col-12 col-md-4 col-lg-3 me-4 d-flex flex-column flex-shrink-0" style={{width: "280px"}}>
                                        <Image src={platillo.thumbnail} className="rounded" style={{height: "180px", objectFit: "cover"}} />
                                        <b className="mt-2">{platillo.nombre}</b>
                                        <p className="text-muted small">{platillo.descripcion}</p>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                    <div className="col-12 d-flex flex-column align-items-center">
                        <div className="col-12 fs-4 fw-bold mb-4 text-center">¿Listo para planear tu evento?</div>
                        <div className="col-12">
                            <div className="row">
                                <div className="col-2"></div>
                                <div className="col-4 border-end px-4">
                                    <label htmlFor="salonSelect" className="form-label">Escoge un salón de eventos</label>
                                    <select id="salonSelect" className="form-select" value={selectedSalonId} onChange={(e) => setSelectedSalonId(e.target.value)}>
                                        {
                                            salonesData.map(salon => (
                                                <option key={salon._id} value={salon._id}>{salon.nombre}</option>
                                            ))
                                        }
                                    </select>
                                    <label className="mt-3 form-label" htmlFor="menuSelect">¿Qué menú darás a tus invitados?</label>
                                    <select id="menuSelect" className="form-select" value={selectedMenuId} onChange={(e) => setSelectedMenuId(e.target.value)}>
                                        {
                                            menuData.map(platillo => (
                                                <option key={platillo._id} value={`[${platillo._id}]`}>{platillo.nombre} - ${platillo.precio.toFixed(2) } pp</option>
                                            ))
                                        }
                                    </select>
                                    <label className="mt-3 form-label" htmlFor="guestCountInput">Cantidad de invitados</label>
                                    <input id="guestCountInput" type="number" className="form-control" value={guestCount} onChange={(e) => setGuestCount(parseInt(e.target.value, 10))} min="1" />
                                    <label className="mt-3 form-label" htmlFor="eventDateInput">Fecha de tu evento</label>
                                    <input id="eventDateInput" type="date" className="form-control" value={eventDate} onChange={(e) => setEventDate(e.target.value)} />
                                </div>
                                <div className="col-4 d-flex flex-column justify-content-center">
                                    <h1>$ {(54000).toLocaleString('en', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} MXN</h1>
                                    <label htmlFor="">Costo estimado de tu evento</label>
                                    <p>Incluye:</p>
                                    <ul>
                                        <li>Platillos</li>
                                        <li>Renta del salón</li>
                                        <li>Servicio de meseros</li>
                                    </ul>
                                    <Button className="mt-2" accent onClick={handleOpenModal}>¡Solicitar apartado!</Button>
                                </div>
                                <div className="col-2"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal de Bootstrap */}
            {isModalOpen && (
                <div className="modal fade show" tabIndex="-1" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }} aria-labelledby="apartadoModalLabel" aria-hidden={!isModalOpen}>
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title" id="apartadoModalLabel">Confirmar Solicitud de Apartado</h5>
                                <Button type="button" className="btn-close" onClick={handleCloseModal} aria-label="Close"></Button>
                            </div>
                            <div className="modal-body">
                                <p>Por favor, proporciona los siguientes detalles adicionales para tu evento:</p>
                                <div className="mb-3">
                                    <label htmlFor="eventTypeSelect" className="form-label">Tipo de Evento</label>
                                    <select id="eventTypeSelect" className="form-select" value={eventType} onChange={(e) => setEventType(e.target.value)}>
                                        <option value="">Selecciona un tipo</option>
                                        <option value="boda">Boda</option>
                                        <option value="graduacion">Graduación</option>
                                        <option value="cumpleanos">Cumpleaños</option>
                                        <option value="corporativo">Evento Corporativo</option>
                                        <option value="otro">Otro</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="eventDescriptionInput" className="form-label">Nombre/Descripción del Evento</label>
                                    <input 
                                        type="text" 
                                        className="form-control" 
                                        id="eventDescriptionInput" 
                                        placeholder="Ej: Boda Erick y Juana, XV Años de Sofía" 
                                        value={eventDescription} 
                                        onChange={(e) => setEventDescription(e.target.value)} 
                                    />
                                </div>
                            </div>
                            <div className="modal-footer">
                                <Button type="button" secondary onClick={handleCloseModal}>Cancelar</Button>
                                <Button type="button" primary onClick={() => {
                                    const formData = { selectedSalonId, selectedMenuId, guestCount, eventDate, eventType, eventDescription };
                                    console.log("Datos del Apartado:", formData);
                                    // Aquí podrías enviar 'formData' a tu backend
                                    handleCloseModal(); // Cierra el modal después de confirmar
                                }}>Confirmar Apartado</Button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}