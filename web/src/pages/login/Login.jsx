import { useState } from "react";
import { Button } from "../../components/atoms/button/Button";
import { Image } from "../../components/atoms/image/Image";
import { Link, useNavigate } from "react-router-dom"; 
import { login } from "../../services/auth.service"; 

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(''); 
    const [loading, setLoading] = useState(false); 
    const navigate = useNavigate(); 

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(''); 
        setLoading(true);

        try {
            
            
            const credentials = { usuario: email, password: password };
            const userData = await login(credentials);

            console.log("Login exitoso, usuario:", userData);
            
            navigate('/app'); 

        } catch (err) {
            console.error("Error en el login:", err);
            
            setError(err.message || "Error al iniciar sesión. Por favor, verifica tus credenciales.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="vw-100 vh-100 d-flex justify-content-center align-items-center bg-secundario">
            <div className="rounded p-5 bg-white d-flex justify-content-center flex-column shadow-sm" style={{ minWidth: "400px" }}>
                <div className="text-center mb-4">
                    <Link to="/">
                        <Image src="/LOGO.svg" style={{ height: "50px" }} className="mb-3" />
                    </Link>
                    <h4>Iniciar sesión</h4>
                    <p className="text-muted">Bienvenido de nuevo</p>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="emailInput" className="form-label">Correo Electrónico</label>
                        <input type="text" className="form-control" id="emailInput" placeholder="tu@correo.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="passwordInput" className="form-label">Contraseña</label>
                        <input type="password" className="form-control" id="passwordInput" placeholder="********" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    {error && <div className="alert alert-danger mt-3" role="alert">{error}</div>}
                    <Button type="submit" primary className="w-100 mt-3" disabled={loading}>
                        {loading ? 'Ingresando...' : 'Ingresar'}
                    </Button>
                </form>
            </div>
        </div>
    )
}