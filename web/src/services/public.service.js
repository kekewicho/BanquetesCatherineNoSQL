// import { apiService } from './api.service'; // Descomentar cuando se integre con la API real


export const fetchSalones = () => {
    // Comentado para usar dummy data por ahora:
    // try {
    //     const salones = await apiService.get('/public/salons');
    //     return salones;
    // } catch (error) {
    //     console.error("Error fetching salones:", error);
    //     return []; // Devuelve un array vacío en caso de error o maneja de otra forma
    // }

    // Dummy data
    return [
        {
            "_id": "60d5f0f8b75e9b8a8b0974eb",
            "nombre": "Salón Imperial",
            "descripcion": "Un salón elegante para grandes eventos.",
            "capacidad": 200,
            "thumbnail": "https://cdn0.bodas.com.mx/vendor/8799/3_2/640/jpg/photo-2020-08-13-23-43-22-1_5_288799-162310516184105.jpeg"
        },
        {
            "_id": "60d5f112b75e9b8a8b0974ec",
            "nombre": "Jardín Esmeralda",
            "descripcion": "Hermoso jardín para eventos al aire libre.",
            "capacidad": 150,
            "thumbnail": "https://cdn0.casamientos.com.ar/vendor/5883/3_2/640/jpeg/whatsapp-image-2019-12-16-at-11-24-49-am-1_7_145883-157667440458716.jpeg"
        },
        {
            "_id": "60d5f112b75e9b8a8b0974ed",
            "nombre": "Terraza Panorámica",
            "descripcion": "Vistas increíbles para una celebración única.",
            "capacidad": 100,
            "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTS-6fXj8cMqgFS8Yw0Zm4HBzp1Ix5jvDDT2QLPud5acrBSCnfUvbwAPaQU5ZvVW01Z3PA&usqp=CAU"
        }
    ];
};

export const fetchMenus = () => {
    // Comentado para usar dummy data por ahora:
    // try {
    //     const menus = await apiService.get('/public/platillos');
    //     return menus;
    // } catch (error) {
    //     console.error("Error fetching menus:", error);
    //     return []; // Devuelve un array vacío en caso de error o maneja de otra forma
    // }

    // Dummy data
    return [
        {
            "_id": "60d63b4a1b2c3d4e5f6a7b8c",
            "nombre": "Ensalada César con Pollo",
            "descripcion": "Clásica ensalada César con pollo a la parrilla.",
            "tipo_platillo": "entrada",
            "precio": 120.50,
            "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgCiiahYcCuZ-36Hhfsw65wV2F7ZalpJB-z4XA4Bf4bxJm6MSY6YsjRo-wxrQhlqWq02E&usqp=CAU", // URL de imagen de ejemplo
            "ingredientes": [
                {
                    "ingrediente": { "_id": "60d63c1a1b2c3d4e5f6a7b8d", "descripcion": "Lechuga Romana", "unidad": "pz" },
                    "qty": 1
                },
                {
                    "ingrediente": { "_id": "60d63c2a1b2c3d4e5f6a7b8e", "descripcion": "Pechuga de Pollo", "unidad": "gr" },
                    "qty": 150
                }
            ]
        },
        {
            "_id": "60d63b4a1b2c3d4e5f6a7b8d",
            "nombre": "Crema de Elote",
            "descripcion": "Suave crema de elote con un toque de epazote.",
            "tipo_platillo": "entrada",
            "precio": 95.00,
            "thumbnail": "https://imag.bonviveur.com/foto-final-de-la-crema-de-elote.jpg", // URL de imagen de ejemplo
            "ingredientes": [
                {
                    "ingrediente": { "_id": "ing_elote_id", "descripcion": "Elote Blanco", "unidad": "gr" },
                    "qty": 200
                },
                {
                    "ingrediente": { "_id": "ing_crema_id", "descripcion": "Crema para batir", "unidad": "ml" },
                    "qty": 100
                }
            ]
        },
        {
            "_id": "60d63b4a1b2c3d4e5f6a7b8e",
            "nombre": "Filete Mignon",
            "descripcion": "Tierno filete mignon en salsa de champiñones.",
            "tipo_platillo": "plato_fuerte",
            "precio": 350.75,
            "thumbnail": "https://cloudfront-us-east-1.images.arcpublishing.com/elimparcial/OAGLGVKIBFG5LMEXSHPGLPDEB4.jpg",
            "ingredientes": [
                {
                    "ingrediente": { "_id": "ing_filete_id", "descripcion": "Filete de Res", "unidad": "gr" },
                    "qty": 250
                },
                {
                    "ingrediente": { "_id": "ing_champinon_id", "descripcion": "Champiñones", "unidad": "gr" },
                    "qty": 100
                }
            ]
        }
    ];
};