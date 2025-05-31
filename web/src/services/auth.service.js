import { apiService } from './api.service';

const AUTH_STORAGE_KEY = 'currentUser';


export const login = async (credentials) => {
    try {
        const response =  {exito: true, usuario: { usuario: "kekewicho", "role": "COLABORADOR", "nombre": "Luis" }} //await apiService.post('/auth/login', credentials);

        if (response && response.exito && response.usuario) {
            localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(response.usuario));
            return response.usuario; // Devuelve solo el objeto usuario para facilitar su uso
        } else {
            // Si la API devuelve exito:false pero un status 200, lo manejamos aquí.
            const errorMessage = response?.mensaje || 'Credenciales incorrectas o respuesta inesperada.';
            throw new Error(errorMessage);
        }
    } catch (error) {
        console.error('Error en el servicio de login:', error);
        // Si el error ya es una instancia de Error (lanzado por apiService o aquí), lo relanzamos.
        // De lo contrario, creamos uno nuevo.
        throw error instanceof Error ? error : new Error(error.message || 'Error durante el inicio de sesión.');
    }
};

/**
 * Cierra la sesión del usuario actual eliminando sus datos de localStorage.
 */
export const logout = () => {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    // Aquí podrías añadir lógica adicional, como redirigir al login o notificar a otros componentes.
};


export const getCurrentUser = () => {
    const user = localStorage.getItem(AUTH_STORAGE_KEY);
    return user ? JSON.parse(user) : null;
};
