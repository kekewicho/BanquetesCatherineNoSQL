
const API_BASE_URL = 'http://localhost:3000/api'; 

/**
 * Función helper para manejar la respuesta de la API.
 * Parsea el JSON o maneja errores.
 * @param {Response} response - El objeto Response de fetch.
 * @returns {Promise<any>} - Los datos de la respuesta (parseados si es JSON).
 * @throws {Error} - Si la respuesta no es ok.
 */
async function handleApiResponse(response) {

    if (response.status === 204) {
        return null;
    }

    const contentType = response.headers.get("content-type");
    let data;

    if (contentType && contentType.includes("application/json")) {
        data = await response.json();
    } else {

        data = await response.text();
    }

    if (!response.ok) {

        const errorMessage = (data && (data.message || data.error || JSON.stringify(data))) || response.statusText || `Request failed with status ${response.status}`;
        console.error('API Error:', errorMessage, 'Status:', response.status, 'Response Data:', data);
        return Promise.reject(new Error(errorMessage));
    }

    return data;
}

/**
 * Función genérica para realizar peticiones fetch.
 * @param {string} endpoint - El endpoint de la API (ej: '/users' o 'users').
 * @param {RequestInit} options - Opciones para fetch (method, headers, body, etc.).
 * @returns {Promise<any>} - Los datos de la respuesta.
 */
async function apiFetch(endpoint, options = {}) {

    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    const defaultHeaders = {
        'Accept': 'application/json',
    };

    if (!(options.body instanceof FormData)) {
        defaultHeaders['Content-Type'] = 'application/json';
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };


    if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        return handleApiResponse(response);
    } catch (error) {
        console.error('Network or Fetch API error:', error);

        if (error instanceof Error) {
            return Promise.reject(error);
        } else {
            return Promise.reject(new Error(String(error) || 'An unknown fetch error occurred'));
        }
    }
}

export const apiService = {
    /**
     * Realiza una petición GET.
     * @param {string} endpoint - El endpoint de la API.
     * @param {object} [params] - Parámetros para la query string.
     * @param {RequestInit} [options] - Opciones adicionales para fetch.
     * @returns {Promise<any>}
     */
    get: (endpoint, params = {}, options = {}) => {
        let urlEndpoint = endpoint;
        if (Object.keys(params).length > 0) {
            const queryParams = new URLSearchParams(params);
            urlEndpoint += `?${queryParams.toString()}`;
        }
        return apiFetch(urlEndpoint, { ...options, method: 'GET' });
    },

    /**
     * Realiza una petición POST.
     * @param {string} endpoint - El endpoint de la API.
     * @param {any} [data] - Datos a enviar en el body.
     * @param {RequestInit} [options] - Opciones adicionales para fetch.
     * @returns {Promise<any>}
     */
    post: (endpoint, data, options = {}) => {
        return apiFetch(endpoint, { ...options, method: 'POST', body: data });
    },

    /**
     * Realiza una petición PUT.
     * @param {string} endpoint - El endpoint de la API.
     * @param {any} [data] - Datos a enviar en el body.
     * @param {RequestInit} [options] - Opciones adicionales para fetch.
     * @returns {Promise<any>}
     */
    put: (endpoint, data, options = {}) => {
        return apiFetch(endpoint, { ...options, method: 'PUT', body: data });
    },

    /**
     * Realiza una petición DELETE.
     * @param {string} endpoint - El endpoint de la API.
     * @param {RequestInit} [options] - Opciones adicionales para fetch.
     * @returns {Promise<any>}
     */
    delete: (endpoint, options = {}) => {
        return apiFetch(endpoint, { ...options, method: 'DELETE' });
    },
};

// Ejemplo de función para obtener token (debes implementarla según tu sistema de autenticación)
// function getAuthToken() {
//   return localStorage.getItem('authToken');
// }