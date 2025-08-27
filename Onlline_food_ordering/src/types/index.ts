export interface User {
  id: number;
  name: string;
  username: string;
  password: string;
  created_at?: Date;
}

export interface Seller extends User {
  // Additional seller-specific fields if needed
}

export interface Buyer extends User {
  // Additional buyer-specific fields if needed
}

export interface Product {
  id: number;
  name: string;
  price: number;
  seller_id: number;
  created_at?: Date;
}

export interface Order {
  id: number;
  buyer_id: number;
  product_id: number;
  status: string;
  address: string;
  mobile: string;
  payment_method: string;
  created_at?: Date;
}

export interface OrderWithDetails extends Order {
  product_name: string;
  seller_name: string;
  buyer_name: string;
}

export interface ChartData {
  name: string;
  order_count: number;
  total_revenue: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  username: string;
  password: string;
}

export interface OrderRequest {
  address: string;
  mobile: string;
  payment_method: string;
}

export interface ProductRequest {
  name: string;
  price: number;
}

export interface JwtPayload {
  userId: number;
  username: string;
  role: 'buyer' | 'seller';
}
