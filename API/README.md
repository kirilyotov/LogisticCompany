# Logistics Company API

This is a FastAPI-based REST API for a logistics company management system. It supports multi-tenancy, role-based access control, and shipment tracking.

## Getting Started

### Run with Docker Compose
1. Go to the API folder:
   ```bash
   cd API
   ```
2. Run the following command:
   ```bash
   docker compose up -d --build
   ```
3. The API will be available at [http://localhost:8000/](http://localhost:8000/).
4. **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Authentication & Authorization

The API uses **OAuth2 with Password Flow** (Bearer Token).

### Roles
*   **Super Admin**: System-wide administrator. Can manage all companies, offices, users, and shipments.
*   **Admin**: Administrator for a specific Company. Can manage users, offices, and shipments within their company.
*   **Employee**: Staff member of a specific Company. Can create and view shipments for their company.
*   **Client**: End-user. Can only view shipments they sent or received, and update their own profile.

### How to Login
1.  **Endpoint**: `POST /api/v1/auth/token`
2.  **Body**: `username` (email) and `password`.
3.  **Response**: Returns an `access_token`.
4.  **Usage**: Include the token in the `Authorization` header of subsequent requests:
    `Authorization: Bearer <your_token>`

---

## API Endpoints & Permissions

### 1. Authentication & Registration
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/token` | Login to get access token | Public |
| `POST` | `/api/v1/register/organization` | Register a new Company + Admin | Public |
| `POST` | `/api/v1/register/company/{id}/user` | Register a new User (Client) for a Company | Public |

### 2. Companies
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/companies` | List all companies | **Super Admin** Only |
| `POST` | `/api/v1/companies` | Create a new company | **Super Admin** Only |
| `GET` | `/api/v1/companies/{id}` | Get company details | **Super Admin** (Any), **Admin/Employee** (Own Company) |
| `PUT` | `/api/v1/companies/{id}` | Update company details | **Super Admin** (Any), **Admin** (Own Company) |
| `DELETE` | `/api/v1/companies/{id}` | Delete a company | **Super Admin** Only |
| `GET` | `/api/v1/companies/{id}/public` | Get public company info (Name) | Public |
| `GET` | `/api/v1/companies/{id}/revenue` | Get company revenue for period | **Super Admin** (Any), **Admin** (Own Company) |

### 3. Offices
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/offices` | List all offices | Authenticated Users |
| `POST` | `/api/v1/offices` | Create a new office | **Super Admin** (Any), **Admin** (Own Company) |
| `GET` | `/api/v1/offices/{id}` | Get office details | Authenticated Users |
| `PUT` | `/api/v1/offices/{id}` | Update office details | **Super Admin** (Any), **Admin** (Own Company) |
| `DELETE` | `/api/v1/offices/{id}` | Delete an office | **Super Admin** (Any), **Admin** (Own Company) |

### 4. Users
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/users` | List users | **Super Admin** (All), **Admin** (Own Company) |
| `POST` | `/api/v1/users` | Create a user (Admin/Employee) | **Super Admin** (Any), **Admin** (Own Company) |
| `PATCH` | `/api/v1/users/{id}` | Update user profile | **User Themselves** Only |
| `DELETE` | `/api/v1/users/{id}` | Delete a user | **Super Admin** (Any), **Admin** (Own Company) |
| `GET` | `/api/v1/users/employees` | List employees | **Super Admin** (All), **Admin** (Own Company) |
| `GET` | `/api/v1/users/clients` | List clients | **Super Admin** (All), **Admin** (Own Company) |

### 5. Shipments
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/shipments` | List shipments | **Super Admin** (All), **Admin/Employee** (Own Company), **Client** (Own Sent/Received) |
| `POST` | `/api/v1/shipments` | Create a shipment | **Super Admin** (Any), **Admin/Employee** (Own Company). *Note: 20% discount if to office.* |
| `GET` | `/api/v1/shipments/{id}` | Get shipment details | **Super Admin** (Any), **Admin/Employee** (Own Company), **Client** (Own Sent/Received) |
| `PUT` | `/api/v1/shipments/{id}` | Update shipment details | **Super Admin** (Any), **Admin/Employee** (Own Company) |
| `DELETE` | `/api/v1/shipments/{id}` | Delete a shipment | **Super Admin** (Any), **Admin/Employee** (Own Company) |
| `PATCH` | `/api/v1/shipments/{id}/status` | Update shipment status | **Super Admin** (Any), **Admin/Employee** (Own Company) |
| `GET` | `/api/v1/shipments/{id}/history` | Get shipment status history | **Super Admin** (Any), **Admin/Employee** (Own Company), **Client** (Own Sent/Received) |

#### Specific Shipment Queries
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/shipments/employee/{id}` | Shipments registered by employee | **Super Admin**, **Admin** (Own Company), **Employee** (Self) |
| `GET` | `/api/v1/shipments/company/{id}` | Shipments of a company | **Super Admin**, **Admin** (Own Company) |
| `GET` | `/api/v1/shipments/client/{id}/sent` | Shipments sent by client | **Super Admin**, **Admin** (Own Company), **Client** (Self) |
| `GET` | `/api/v1/shipments/client/{id}/received` | Shipments received by client | **Super Admin**, **Admin** (Own Company), **Client** (Self) |
