# Backend API Documentation - Plataforma de Banquetes

## 1. Overview

This document outlines the backend API endpoints for the Banquets Platform. The API is designed to support various user roles including general users, clients, banquet administrators, and salon administrators. It facilitates event management, client relations, staff scheduling, and procurement processes.

The API returns enriched JSON responses, meaning that fields referencing other documents (e.g., a `salon_id` in an event) will often be populated with the actual data of the referenced document rather than just its ID.

## 2. Authentication

A token-based authentication system (e.g., JWT) is expected. Authenticated endpoints will require an `Authorization` header with a bearer token.

* **Endpoint:** `POST /auth/login`
    * **Description:** Authenticates a user (client, admin, manager) and returns an access token.
    * **Request Body Example:**
        ```json
        {
            "usuario": "nombre_usuario",
            "password": "supersecretpassword"
        }
        ```
    * **Response Body Example (Success):**
        ```json
        {
            "mensaje": "Login exitoso",
            "exito": true,
            "usuario": {
                "id": "60d5ecf7b75e9b8a8b0974ea",
                "usuario": "cliente_juan",
                "role": "CLIENTE",
                "nombre": "Juan Perez"
            }
        }
        ```

* **Endpoint:** `POST /auth/logout`
    * **Description:** Invalidates the user's session/token.
    * **Response Body Example (Success):**
        ```json
        {
            "message": "Logout successful"
        }
        ```

---

## 3. Public Endpoints (`/public`)

Endpoints accessible without authentication, primarily for the landing page and initial information gathering.

### 3.1 Salons

* **Endpoint:** `GET /public/salons`
    * **Description:** Retrieves a list of all available event salons.
    * **Response Body Example:**
        ```json
        [
            {
                "_id": "60d5f0f8b75e9b8a8b0974eb",
                "nombre": "Salón Imperial",
                "descripcion": "Un salón elegante para grandes eventos.",
                "capacidad": 200
            },
            {
                "_id": "60d5f112b75e9b8a8b0974ec",
                "nombre": "Jardín Esmeralda",
                "descripcion": "Hermoso jardín para eventos al aire libre.",
                "capacidad": 150
            }
        ]
        ```

* **Endpoint:** `GET /public/salons/{salon_id}`
    * **Description:** Retrieves detailed information for a specific salon.
    * **Response Body Example:**
        ```json
        {
            "_id": "60d5f0f8b75e9b8a8b0974eb",
            "nombre": "Salón Imperial",
            "descripcion": "Un salón elegante para grandes eventos.",
            "capacidad": 200
        }
        ```

### 3.2 Platillos (Menu Items)

* **Endpoint:** `GET /public/platillos`
    * **Description:** Retrieves a list of all available platillos (menu items) for quoting and information.
    * **Query Parameters:**
        * `tipo_platillo` (optional): Filter by type (e.g., "entrada", "plato_fuerte", "postre").
    * **Response Body Example:**
        ```json
        [
            {
                "_id": "60d63b4a1b2c3d4e5f6a7b8c",
                "nombre": "Ensalada César con Pollo",
                "descripcion": "Clásica ensalada César con pollo a la parrilla.",
                "tipo_platillo": "entrada",
                "precio": 120.50,
                "thumbnail": "url_to_image.jpg",
                "ingredientes": [
                    {
                        "ingrediente": {
                            "_id": "60d63c1a1b2c3d4e5f6a7b8d",
                            "descripcion": "Lechuga Romana",
                            "unidad": "pz"
                        },
                        "qty": 1
                    },
                    {
                        "ingrediente": {
                            "_id": "60d63c2a1b2c3d4e5f6a7b8e",
                            "descripcion": "Pechuga de Pollo",
                            "unidad": "gr"
                        },
                        "qty": 150
                    }
                ]
            }
        ]
        ```

* **Endpoint:** `GET /public/platillos/{platillo_id}`
    * **Description:** Retrieves detailed information for a specific platillo.
    * **Response Body Example (similar to one item in the list above).**

---

## 4. Client Endpoints (`/clients`)

Endpoints for logged-in clients to manage their events and view their information. Requires authentication.

### 4.1 Client Information

* **Endpoint:** `GET /clients/me`
    * **Description:** Retrieves the profile information of the currently logged-in client.
    * **Response Body Example:**
        ```json
        {
            "_id": "60d5ecf7b75e9b8a8b0974ea",
            "usuario": "cliente_juan",
            "nombre": "Juan",
            "apellido": "Perez",
            "telefono": "555-1234",
            "rfc": "PEPJ800101XYZ",
            "direccion": {
                "calle": "Av. Siempreviva 742",
                "ciudad": "Springfield",
                "cp": "12345"
            },
            "role": "cliente"
        }
        ```

### 4.2 Client Events

* **Endpoint:** `GET /clients/me/events`
    * **Description:** Retrieves a list of events (upcoming and historical) for the logged-in client.
    * **Query Parameters:**
        * `status` (optional): "upcoming", "past". Defaults to all.
    * **Response Body Example:** (See enriched Evento JSON structure under `/banquet-admin/events/{event_id}`)
        ```json
        [
            // List of Evento objects
            {
                "_id": "60d73f2a8b3c4d5e6f7a8b9c",
                "fecha": "2025-12-24",
                "tipo": "Cena Navideña",
                "descripcion": "Cena familiar navideña.",
                "menu": [
                    {
                        "_id": "60d63b4a1b2c3d4e5f6a7b8c",
                        "nombre": "Pavo Relleno",
                        // ... other platillo details
                    }
                ],
                "plantilla": [ // Staff assigned
                    {
                        "_id": "60d74a018b3c4d5e6f7a8b9d",
                        "nombre": "Carlos (Mesero)",
                        "role": "mesero"
                        // ... other staff details
                    }
                ],
                "salon": {
                    "_id": "60d5f0f8b75e9b8a8b0974eb",
                    "nombre": "Salón Imperial",
                    "capacidad": 200
                    // ... other salon details
                },
                "invitados": 50,
                "validated": true
            }
        ]
        ```

* **Endpoint:** `GET /clients/me/events/{event_id}`
    * **Description:** Retrieves detailed information for a specific event belonging to the logged-in client.
    * **Response Body Example:** (Single enriched Evento object, see `/banquet-admin/events/{event_id}`)

* **Endpoint:** `PUT /clients/me/events/{event_id}`
    * **Description:** Allows a client to update the number of guests for their event (up to 3 days before the event). This will likely trigger a notification for administrators and may set `validated` to `false`.
    * **Request Body Example:**
        ```json
        {
            "invitados": 55
        }
        ```
    * **Response Body Example (Success):** (Updated enriched Evento object)
        ```json
        {
            "_id": "60d73f2a8b3c4d5e6f7a8b9c",
            "fecha": "2025-12-24",
            "tipo": "Cena Navideña",
            "descripcion": "Cena familiar navideña.",
            // ... other fields
            "invitados": 55,
            "validated": false // Or true, depending on business logic
        }
        ```

---

## 5. Banquet Administrator Endpoints (`/banquet-admin`)

Endpoints for banquet administrators. Requires authentication and "admin_banquetes" role.

### 5.1 Staff Management (RH Plantilla)

* **Endpoint:** `POST /banquet-admin/staff`
    * **Description:** Creates a new staff member (collaborator). Password should be handled securely (e.g., sent via a separate secure channel or set up for first login).
    * **Request Body Example:**
        ```json
        {
            "usuario": "mesero_carlos",
            "password": "initial_password", // Handle securely
            "role": "mesero", // Or "cocinero", "host", etc.
            "nombre": "Carlos",
            "apellido": "Rodriguez",
            "telefono": "555-5678"
        }
        ```
    * **Response Body Example (Success):** (The created User/Cliente object)
        ```json
        {
            "_id": "60d74a018b3c4d5e6f7a8b9d",
            "usuario": "mesero_carlos",
            "nombre": "Carlos",
            "apellido": "Rodriguez",
            "telefono": "555-5678",
            "role": "mesero"
        }
        ```

* **Endpoint:** `GET /banquet-admin/staff`
    * **Description:** Retrieves a list of all staff members.
    * **Query Parameters:**
        * `role` (optional): Filter by staff role.
    * **Response Body Example:**
        ```json
        [
            {
                "_id": "60d74a018b3c4d5e6f7a8b9d",
                "usuario": "mesero_carlos",
                "nombre": "Carlos",
                "apellido": "Rodriguez",
                "role": "mesero"
            }
            // ... more staff members
        ]
        ```

* **Endpoint:** `GET /banquet-admin/staff/{staff_id}`
    * **Description:** Retrieves details for a specific staff member.
    * **Response Body Example:** (Single staff member object)

* **Endpoint:** `PUT /banquet-admin/staff/{staff_id}`
    * **Description:** Updates a staff member's information.
    * **Request Body Example:**
        ```json
        {
            "telefono": "555-8765",
            "role": "capitan_meseros"
        }
        ```
    * **Response Body Example (Success):** (Updated staff member object)

* **Endpoint:** `DELETE /banquet-admin/staff/{staff_id}`
    * **Description:** Deletes/deactivates a staff member. (Consider soft delete vs. hard delete).
    * **Response Body Example (Success):**
        ```json
        {
            "message": "Staff member deactivated successfully."
        }
        ```

### 5.2 Client Management

* **Endpoint:** `GET /banquet-admin/clients`
    * **Description:** Retrieves a list of all clients.
    * **Query Parameters:**
        * `search` (optional): Search by name, RFC, etc.
    * **Response Body Example:** (List of Cliente objects, see `/clients/me` for structure)

* **Endpoint:** `GET /banquet-admin/clients/{client_id}`
    * **Description:** Retrieves detailed information for a specific client.
    * **Response Body Example:** (Single Cliente object)

* **Endpoint:** `GET /banquet-admin/clients/{client_id}/events`
    * **Description:** Retrieves all events (past and upcoming) for a specific client.
    * **Response Body Example:** (List of enriched Evento objects)

* **Endpoint:** `POST /banquet-admin/clients`
    * **Description:** Creates a new client.
    * **Request Body Example:**
        ```json
        {
            "usuario": "nuevo_cliente_ana",
            "password": "client_password", // Handle securely
            "nombre": "Ana",
            "apellido": "Gomez",
            "telefono": "555-1122",
            "rfc": "GOMA900101ABC",
            "direccion": { "calle": "Calle Falsa 123", "ciudad": "Ciudad Ejemplo", "cp": "54321"},
            "role": "cliente" // Automatically set or confirmed
        }
        ```
    * **Response Body Example (Success):** (The created Cliente object)

* **Endpoint:** `PUT /banquet-admin/clients/{client_id}`
    * **Description:** Updates a client's information.
    * **Request Body Example:**
        ```json
        {
            "telefono": "555-3344",
            "direccion": { "calle": "Calle Verdadera 456", "ciudad": "Otra Ciudad", "cp": "67890"}
        }
        ```
    * **Response Body Example (Success):** (Updated Cliente object)

### 5.3 Event Management

* **Endpoint:** `POST /banquet-admin/events`
    * **Description:** Creates a new event.
    * **Request Body Example:**
        ```json
        {
            "fecha": "2026-01-15",
            "tipo": "Boda",
            "descripcion": "Boda de Juan y Ana",
            "menu": ["platillo_id_1", "platillo_id_2"], // List of Platillo ObjectIds
            "plantilla": ["staff_id_1", "staff_id_2"], // List of User (staff) ObjectIds
            "salon": "salon_id_1", // Salon ObjectId
            "invitados": 150,
            "cliente_id": "cliente_id_responsable", // To associate with a client
            "validated": true // Or false if requires further steps
        }
        ```
    * **Response Body Example (Success):** (The created, enriched Evento object)

* **Endpoint:** `GET /banquet-admin/events`
    * **Description:** Retrieves a list of events.
    * **Query Parameters:**
        * `from_date` (optional, e.g., YYYY-MM-DD): Start date for a range (e.g., next 15 days).
        * `to_date` (optional, e.g., YYYY-MM-DD): End date for a range.
        * `salon_id` (optional): Filter by salon.
        * `validated` (optional): "true" or "false".
        * `status` (optional): "upcoming", "past".
    * **Response Body Example:** (List of enriched Evento objects)

* **Endpoint:** `GET /banquet-admin/events/{event_id}`
    * **Description:** Retrieves detailed information for a specific event, enriched with related data.
    * **Response Body Example (Enriched Evento):**
        ```json
        {
            "_id": "60d73f2a8b3c4d5e6f7a8b9c",
            "fecha": "2025-12-24",
            "tipo": "Cena Navideña",
            "descripcion": "Cena familiar navideña.",
            "menu": [
                {
                    "_id": "60d63b4a1b2c3d4e5f6a7b8c",
                    "nombre": "Pavo Relleno",
                    "descripcion": "Delicioso pavo relleno horneado.",
                    "tipo_platillo": "plato_fuerte",
                    "precio": 450.00,
                    "thumbnail": "url_to_pavo.jpg",
                    "ingredientes": [
                        {
                            "ingrediente": {
                                "_id": "ingrediente_id_pavo",
                                "descripcion": "Pavo Entero",
                                "unidad": "kg"
                            },
                            "qty": 5
                        }
                        // ... other ingredients for pavo
                    ]
                }
                // ... other platillos in the menu
            ],
            "plantilla": [ // Staff assigned
                {
                    "_id": "60d74a018b3c4d5e6f7a8b9d",
                    "usuario": "mesero_carlos",
                    "nombre": "Carlos",
                    "role": "mesero"
                }
                // ... other staff members
            ],
            "salon": {
                "_id": "60d5f0f8b75e9b8a8b0974eb",
                "nombre": "Salón Imperial",
                "descripcion": "Un salón elegante para grandes eventos.",
                "capacidad": 200
            },
            "invitados": 50,
            "validated": true,
            "cliente": { // Information about the client who booked the event
                "_id": "60d5ecf7b75e9b8a8b0974ea",
                "nombre": "Juan",
                "apellido": "Perez"
                // ... other relevant client fields
            }
        }
        ```

* **Endpoint:** `PUT /banquet-admin/events/{event_id}`
    * **Description:** Updates an existing event.
    * **Request Body Example:** (Fields to update, can include `menu`, `plantilla`, `salon` IDs, etc.)
        ```json
        {
            "descripcion": "Boda elegante de Juan y Ana",
            "invitados": 160,
            "menu": ["platillo_id_1_new", "platillo_id_3"],
            "validated": true
        }
        ```
    * **Response Body Example (Success):** (The updated, enriched Evento object)

* **Endpoint:** `DELETE /banquet-admin/events/{event_id}`
    * **Description:** Cancels/deletes an event.
    * **Response Body Example (Success):**
        ```json
        {
            "message": "Event deleted successfully."
        }
        ```

### 5.4 Event Staff Assignment (RH Planeacion Horarios)

* **Endpoint:** `GET /banquet-admin/events/{event_id}/staff`
    * **Description:** Lists the staff assigned to a specific event (populates `plantilla`).
    * **Response Body Example:** (List of User objects - staff)
        ```json
        [
            {
                "_id": "60d74a018b3c4d5e6f7a8b9d",
                "usuario": "mesero_carlos",
                "nombre": "Carlos",
                "role": "mesero"
            }
        ]
        ```

* **Endpoint:** `POST /banquet-admin/events/{event_id}/staff`
    * **Description:** Assigns a staff member to an event (adds to `plantilla`).
    * **Request Body Example:**
        ```json
        {
            "staff_id": "60d74a018b3c4d5e6f7a8b9d"
        }
        ```
    * **Response Body Example (Success):** (Updated list of assigned staff or the full Evento object)

* **Endpoint:** `DELETE /banquet-admin/events/{event_id}/staff/{staff_id}`
    * **Description:** Removes a staff member from an event (removes from `plantilla`).
    * **Response Body Example (Success):**
        ```json
        {
            "message": "Staff member removed from event successfully."
        }
        ```

### 5.5 Procurement Management

* **Endpoint:** `GET /banquet-admin/procurement/required-ingredients`
    * **Description:** Calculates and lists aggregated ingredient quantities required for events within a given date range (e.g., next 15 days).
    * **Query Parameters:**
        * `from_date` (required, YYYY-MM-DD)
        * `to_date` (required, YYYY-MM-DD)
    * **Response Body Example:**
        ```json
        [
            {
                "ingrediente": {
                    "_id": "60d63c2a1b2c3d4e5f6a7b8e",
                    "descripcion": "Pechuga de Pollo",
                    "unidad": "gr"
                },
                "total_qty_requerida": 5500 // e.g., 5.5 kg
            },
            {
                "ingrediente": {
                    "_id": "ingrediente_id_tomate",
                    "descripcion": "Tomate Saladet",
                    "unidad": "kg"
                },
                "total_qty_requerida": 25
            }
            // ... other ingredients
        ]
        ```

* **Endpoint:** `POST /banquet-admin/procurement/deliveries`
    * **Description:** Records a new procurement delivery.
    * **Request Body Example (`Delivery` model):**
        ```json
        {
            "ingredientes": [
                { "ingrediente_id": "60d63c2a1b2c3d4e5f6a7b8e", "cantidad": 5000, "unidad_compra": "gr" }, // Assuming an ID for Ingrediente
                { "ingrediente_id": "ingrediente_id_tomate", "cantidad": 20, "unidad_compra": "kg" }
            ],
            "fecha_creacion": "2025-05-20", // Or set by server
            "fecha_entrega": "2025-05-22"
            // Potentially add supplier info, cost, etc. in a more complex model
        }
        ```
    * **Response Body Example (Success):** (The created Delivery object, with enriched ingredients)
        ```json
        {
            "_id": "delivery_object_id",
            "ingredientes": [
                {
                    "ingrediente": { "_id": "60d63c2a1b2c3d4e5f6a7b8e", "descripcion": "Pechuga de Pollo", "unidad": "gr" },
                    "cantidad": 5000,
                    "unidad_compra": "gr"
                }
                // ...
            ],
            "fecha_creacion": "2025-05-20",
            "fecha_entrega": "2025-05-22"
        }
        ```

* **Endpoint:** `GET /banquet-admin/procurement/deliveries`
    * **Description:** Retrieves a list of past and pending procurement deliveries.
    * **Query Parameters:**
        * `status` (optional): "pending", "completed".
        * `from_date` / `to_date` (optional): Filter by delivery date.
    * **Response Body Example:** (List of Delivery objects, enriched)

* **Endpoint:** `GET /banquet-admin/ingredients/{ingredient_id}/deliveries`
    * **Description:** Retrieves procurement deliveries (finished and pending) for a specific ingredient.
    * **Response Body Example:** (List of Delivery objects filtered by the ingredient)
        * **Note:** This requires the `Delivery.ingredientes` list to be queryable for specific ingredient IDs.

### 5.6 Ingredient Management (Informational)

* **Endpoint:** `GET /banquet-admin/ingredients`
    * **Description:** Retrieves a list of all ingredients.
    * **Response Body Example:**
        ```json
        [
            {
                "_id": "60d63c1a1b2c3d4e5f6a7b8d",
                "descripcion": "Lechuga Romana",
                "unidad": "pz"
            }
            // ... other ingredients
        ]
        ```
* **Endpoint:** `GET /banquet-admin/ingredients/{ingredient_id}`
    * **Description:** Retrieves details for a specific ingredient.
    * **Response Body Example:**
        ```json
        {
            "_id": "60d63c1a1b2c3d4e5f6a7b8d",
            "descripcion": "Lechuga Romana",
            "unidad": "pz"
        }
        ```
    * **Note:** Endpoints for CRUD operations on Ingredients (`POST`, `PUT`, `DELETE /banquet-admin/ingredients`) can be added if admins need to manage the master list of ingredients.

### 5.7 Platillo Management (Informational/CRUD)

* **Endpoint:** `GET /banquet-admin/platillos` (Similar to `/public/platillos` but potentially with more admin actions)
* **Endpoint:** `POST /banquet-admin/platillos`
    * **Description:** Creates a new platillo.
    * **Request Body Example:** (Structure from `Platillo` model, `ingredientes` list will contain dicts like `{"ingrediente": "ingrediente_object_id", "qty": 2}`)
* **Endpoint:** `PUT /banquet-admin/platillos/{platillo_id}`
    * **Description:** Updates an existing platillo.
* **Endpoint:** `DELETE /banquet-admin/platillos/{platillo_id}`
    * **Description:** Deletes a platillo.

### 5.8 Salon Management (Informational/CRUD)

* **Endpoint:** `GET /banquet-admin/salons` (Similar to `/public/salons`)
* **Endpoint:** `POST /banquet-admin/salons`
    * **Description:** Creates a new salon.
    * **Request Body Example:** (`Salon` model structure)
* **Endpoint:** `PUT /banquet-admin/salons/{salon_id}`
    * **Description:** Updates an existing salon.
* **Endpoint:** `DELETE /banquet-admin/salons/{salon_id}`
    * **Description:** Deletes a salon.

### 5.9 Notifications

* **Endpoint:** `GET /banquet-admin/notifications`
    * **Description:** Retrieves a list of notifications for the admin (e.g., client changed guest count, new event pending validation).
    * **Response Body Example:**
        ```json
        [
            {
                "_id": "notification_id_1",
                "timestamp": "2025-05-29T10:00:00Z",
                "type": "EVENT_GUEST_UPDATE",
                "message": "Cliente Juan Perez actualizó el número de invitados para el evento 'Cena Navideña' (ID: 60d73f2a8b3c4d5e6f7a8b9c) a 55.",
                "related_event_id": "60d73f2a8b3c4d5e6f7a8b9c",
                "is_read": false
            }
            // ... other notifications
        ]
        ```
* **Endpoint:** `PUT /banquet-admin/notifications/{notification_id}/read`
    * **Description:** Marks a notification as read.
    * **Response Body Example:**
        ```json
        {
            "message": "Notification marked as read."
        }
        ```

---

## 6. Salon Administrator Endpoints (`/salon-admin`)

Endpoints for logged-in salon administrators (`Gerente` role). Requires authentication and "admin_salon" role. These users are associated with a specific salon.

### 6.1 Salon Admin Events

* **Endpoint:** `GET /salon-admin/me/events`
    * **Description:** Retrieves a list of events scheduled for the salon managed by the logged-in administrator. The backend will identify the salon based on the authenticated `Gerente`'s `salon` field.
    * **Query Parameters:**
        * `from_date` (optional, e.g., YYYY-MM-DD): Start date for a range (e.g., next 15 days).
        * `to_date` (optional, e.g., YYYY-MM-DD): End date for a range.
    * **Response Body Example:** (List of enriched Evento objects for their salon, see `/banquet-admin/events/{event_id}` for structure)

* **Endpoint:** `GET /salon-admin/me/events/{event_id}`
    * **Description:** Retrieves detailed information for a specific event in the manager's salon. The backend should verify that the event belongs to the manager's salon.
    * **Response Body Example:** (Single enriched Evento object, see `/banquet-admin/events/{event_id}` for structure)

---

This README provides a foundational set of endpoints. Depending on the exact implementation of features like "RH Planeacion horarios" (beyond just assigning staff to `plantilla`) or detailed inventory tracking, further specialized endpoints might be necessary.