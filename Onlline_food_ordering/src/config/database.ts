import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'shop_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

export const db = mysql.createPool(dbConfig);

// Test database connection
export const testConnection = async (): Promise<void> => {
  try {
    const connection = await db.getConnection();
    console.log('✅ Database connected successfully!');
    connection.release();
  } catch (error) {
    console.error('❌ Database connection failed:', error);
    process.exit(1);
  }
};
