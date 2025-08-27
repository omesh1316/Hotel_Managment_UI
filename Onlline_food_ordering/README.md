# Online Food Ordering System - TypeScript Backend

A modern TypeScript backend for an online food ordering system with JWT authentication, role-based access control, and RESTful API endpoints.

## 🚀 Features

- **TypeScript** - Type-safe development
- **JWT Authentication** - Secure token-based authentication
- **Role-based Access Control** - Separate buyer and seller roles
- **MySQL Database** - Reliable data storage
- **RESTful API** - Clean and consistent endpoints
- **Password Hashing** - Secure password storage with bcrypt
- **CORS Support** - Cross-origin resource sharing enabled

## 📋 Prerequisites

- Node.js (v16 or higher)
- MySQL Server
- npm or yarn

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Onlline_food_ordering
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your database credentials
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=omesh
   DB_NAME=shop_db
   JWT_SECRET=your_super_secret_jwt_key_for_food_ordering
   PORT=3000
   ```

4. **Set up the database**
   ```sql
   -- Create database (if not exists)
   CREATE DATABASE shop_db;
   USE shop_db;
   
   -- Create tables (your existing schema)
   CREATE TABLE sellers (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     username VARCHAR(255) UNIQUE NOT NULL,
     password VARCHAR(255) NOT NULL
   );
   
   CREATE TABLE buyers (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     username VARCHAR(255) UNIQUE NOT NULL,
     password VARCHAR(255) NOT NULL
   );
   
   CREATE TABLE products (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     price DECIMAL(10,2) NOT NULL,
     seller_id INT,
     FOREIGN KEY (seller_id) REFERENCES sellers(id)
   );
   
   CREATE TABLE orders (
     id INT AUTO_INCREMENT PRIMARY KEY,
     buyer_id INT,
     product_id INT,
     status VARCHAR(50) DEFAULT 'Placed',
     address TEXT NOT NULL,
     mobile VARCHAR(20) NOT NULL,
     payment_method VARCHAR(50) NOT NULL,
     FOREIGN KEY (buyer_id) REFERENCES buyers(id),
     FOREIGN KEY (product_id) REFERENCES products(id)
   );
   ```

## 🚀 Running the Application

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm run build
npm start
```

The server will start on `http://localhost:3000`

## 📚 API Documentation

### Authentication Endpoints

#### Seller Registration
```http
POST /api/auth/seller/register
Content-Type: application/json

{
  "name": "John Doe",
  "username": "johndoe",
  "password": "password123"
}
```

#### Seller Login
```http
POST /api/auth/seller/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

#### Buyer Registration
```http
POST /api/auth/buyer/register
Content-Type: application/json

{
  "name": "Jane Smith",
  "username": "janesmith",
  "password": "password123"
}
```

#### Buyer Login
```http
POST /api/auth/buyer/login
Content-Type: application/json

{
  "username": "janesmith",
  "password": "password123"
}
```

### Product Endpoints

#### Get All Products (Public)
```http
GET /api/products
```

#### Get Seller Products (Protected)
```http
GET /api/products/seller
Authorization: Bearer <jwt_token>
```

#### Add Product (Seller Only)
```http
POST /api/products
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "Pizza Margherita",
  "price": 12.99
}
```

#### Delete Product (Seller Only)
```http
DELETE /api/products/:productId
Authorization: Bearer <jwt_token>
```

#### Get Seller Analytics (Seller Only)
```http
GET /api/products/analytics
Authorization: Bearer <jwt_token>
```

### Order Endpoints

#### Place Order (Buyer Only)
```http
POST /api/orders/:productId
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "address": "123 Main St, City",
  "mobile": "1234567890",
  "payment_method": "Credit Card"
}
```

#### Get Buyer Orders (Buyer Only)
```http
GET /api/orders/buyer
Authorization: Bearer <jwt_token>
```

#### Get Seller Orders (Seller Only)
```http
GET /api/orders/seller
Authorization: Bearer <jwt_token>
```

#### Update Order Status (Seller Only)
```http
PUT /api/orders/:orderId/status
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "status": "Delivered"
}
```

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

JWT tokens are returned upon successful login and contain:
- `userId`: User's ID
- `username`: User's username
- `role`: User's role (buyer/seller)

## 📁 Project Structure

```
src/
├── config/
│   └── database.ts          # Database configuration
├── controllers/
│   ├── authController.ts    # Authentication logic
│   ├── productController.ts # Product management
│   └── orderController.ts   # Order management
├── middleware/
│   └── auth.ts             # JWT authentication middleware
├── routes/
│   ├── auth.ts             # Authentication routes
│   ├── products.ts         # Product routes
│   └── orders.ts           # Order routes
├── types/
│   └── index.ts            # TypeScript interfaces
└── app.ts                  # Main application file
```

## 🧪 Testing

Test the API endpoints using tools like:
- Postman
- Insomnia
- curl
- Thunder Client (VS Code extension)

## 🔧 Development

### Available Scripts
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build TypeScript to JavaScript
- `npm start` - Start production server
- `npm test` - Run tests (to be implemented)

### Environment Variables
- `DB_HOST` - Database host
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name
- `JWT_SECRET` - Secret key for JWT tokens
- `PORT` - Server port (default: 3000)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the ISC License.

## 🆘 Support

For support, please open an issue in the repository or contact the development team.
# Hotel Management GUI Based WebApp
