import { Link } from "react-router-dom"

export const NavBar = ({ links = [] }) => {

    return (
        <div className="d-flex flex-column justify-content-center align-items-center bg-primario position-fixed px-3 py-5" style={{ bottom: "50%", left: 0, borderRadius:"0 30px 30px 0", transform:"translateY(50%)" }}>
            {
                links.map(link => (
                    <Link to={link.to} className={`bi ${link.icon} text-white fs-5 my-3`} />
                ))
            }
        </div>
    )
}