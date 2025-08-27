import { Request, Response } from 'express';
import { db } from '../config/database';
import { ProductRequest } from '../types';

export const getAllProducts = async (req: Request, res: Response): Promise<void> => {
  try {
    const [products] = await db.execute(`
      SELECT products.*, sellers.name AS seller_name
      FROM products
      JOIN sellers ON products.seller_id = sellers.id
    `);

    res.json({ products });
  } catch (error) {
    console.error('Get all products error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getSellerProducts = async (req: Request, res: Response): Promise<void> => {
  try {
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [products] = await db.execute(
      'SELECT * FROM products WHERE seller_id = ?',
      [sellerId]
    );

    res.json({ products });
  } catch (error) {
    console.error('Get seller products error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const addProduct = async (req: Request, res: Response): Promise<void> => {
  try {
    const { name, price }: ProductRequest = req.body;
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [result] = await db.execute(
      'INSERT INTO products (name, price, seller_id) VALUES (?, ?, ?)',
      [name, price, sellerId]
    );

    res.status(201).json({ message: 'Product added successfully!' });
  } catch (error) {
    console.error('Add product error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const deleteProduct = async (req: Request, res: Response): Promise<void> => {
  try {
    const { productId } = req.params;
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [result] = await db.execute(
      'DELETE FROM products WHERE id = ? AND seller_id = ?',
      [productId, sellerId]
    );

    res.json({ message: 'Product deleted successfully!' });
  } catch (error) {
    console.error('Delete product error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getSellerAnalytics = async (req: Request, res: Response): Promise<void> => {
  try {
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [chartData] = await db.execute(`
      SELECT products.name, COUNT(orders.id) AS order_count, SUM(products.price) AS total_revenue
      FROM products
      LEFT JOIN orders ON products.id = orders.product_id
      WHERE products.seller_id = ?
      GROUP BY products.name
    `, [sellerId]);

    res.json({ chartData });
  } catch (error) {
    console.error('Get seller analytics error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
