import { Request, Response } from 'express';
import { db } from '../config/database';
import { OrderRequest } from '../types';

export const placeOrder = async (req: Request, res: Response): Promise<void> => {
  try {
    const { productId } = req.params;
    const { address, mobile, payment_method }: OrderRequest = req.body;
    const buyerId = req.user?.userId;

    if (!buyerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    // Get product price
    const [products] = await db.execute(
      'SELECT price FROM products WHERE id = ?',
      [productId]
    );

    if (!Array.isArray(products) || products.length === 0) {
      res.status(404).json({ error: 'Product not found' });
      return;
    }

    const product = products[0] as any;

    // Insert order
    const [result] = await db.execute(`
      INSERT INTO orders (buyer_id, product_id, status, address, mobile, payment_method)
      VALUES (?, ?, 'Placed', ?, ?, ?)
    `, [buyerId, productId, address, mobile, payment_method]);

    res.status(201).json({ message: '✅ Order placed successfully!' });
  } catch (error) {
    console.error('Place order error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getBuyerOrders = async (req: Request, res: Response): Promise<void> => {
  try {
    const buyerId = req.user?.userId;

    if (!buyerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [orders] = await db.execute(`
      SELECT orders.*, products.name AS product_name, sellers.name AS seller_name
      FROM orders
      JOIN products ON orders.product_id = products.id
      JOIN sellers ON products.seller_id = sellers.id
      WHERE orders.buyer_id = ?
    `, [buyerId]);

    res.json({ orders });
  } catch (error) {
    console.error('Get buyer orders error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getSellerOrders = async (req: Request, res: Response): Promise<void> => {
  try {
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const [orders] = await db.execute(`
      SELECT orders.*, products.name AS product_name, buyers.name AS buyer_name
      FROM orders
      JOIN products ON orders.product_id = products.id
      JOIN buyers ON orders.buyer_id = buyers.id
      WHERE products.seller_id = ?
    `, [sellerId]);

    res.json({ orders });
  } catch (error) {
    console.error('Get seller orders error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const updateOrderStatus = async (req: Request, res: Response): Promise<void> => {
  try {
    const { orderId } = req.params;
    const { status } = req.body;
    const sellerId = req.user?.userId;

    if (!sellerId) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    // Verify the order belongs to this seller
    const [orders] = await db.execute(`
      SELECT orders.id FROM orders
      JOIN products ON orders.product_id = products.id
      WHERE orders.id = ? AND products.seller_id = ?
    `, [orderId, sellerId]);

    if (!Array.isArray(orders) || orders.length === 0) {
      res.status(404).json({ error: 'Order not found or access denied' });
      return;
    }

    // Update order status
    await db.execute(
      'UPDATE orders SET status = ? WHERE id = ?',
      [status, orderId]
    );

    res.json({ message: 'Order status updated!' });
  } catch (error) {
    console.error('Update order status error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
