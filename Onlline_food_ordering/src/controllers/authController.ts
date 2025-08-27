import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { db } from '../config/database';
import { LoginRequest, RegisterRequest, JwtPayload } from '../types';

export const sellerRegister = async (req: Request, res: Response): Promise<void> => {
  try {
    const { name, username, password }: RegisterRequest = req.body;

    // Check if username already exists
    const [existingUsers] = await db.execute(
      'SELECT * FROM sellers WHERE username = ?',
      [username]
    );

    if (Array.isArray(existingUsers) && existingUsers.length > 0) {
      res.status(400).json({ error: 'Username already exists!' });
      return;
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert new seller
    const [result] = await db.execute(
      'INSERT INTO sellers (name, username, password) VALUES (?, ?, ?)',
      [name, username, hashedPassword]
    );

    res.status(201).json({ message: 'Seller registered successfully!' });
  } catch (error) {
    console.error('Seller registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const sellerLogin = async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, password }: LoginRequest = req.body;

    // Find seller
    const [sellers] = await db.execute(
      'SELECT * FROM sellers WHERE username = ?',
      [username]
    );

    if (!Array.isArray(sellers) || sellers.length === 0) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    const seller = sellers[0] as any;

    // Check password
    const isValidPassword = await bcrypt.compare(password, seller.password);
    if (!isValidPassword) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    // Generate JWT token
    const payload: JwtPayload = {
      userId: seller.id,
      username: seller.username,
      role: 'seller'
    };

    const token = jwt.sign(payload, process.env.JWT_SECRET || 'fallback_secret', {
      expiresIn: '24h'
    });

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: seller.id,
        name: seller.name,
        username: seller.username,
        role: 'seller'
      }
    });
  } catch (error) {
    console.error('Seller login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const buyerRegister = async (req: Request, res: Response): Promise<void> => {
  try {
    const { name, username, password }: RegisterRequest = req.body;

    // Check if username already exists
    const [existingUsers] = await db.execute(
      'SELECT * FROM buyers WHERE username = ?',
      [username]
    );

    if (Array.isArray(existingUsers) && existingUsers.length > 0) {
      res.status(400).json({ error: 'Username already exists!' });
      return;
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert new buyer
    const [result] = await db.execute(
      'INSERT INTO buyers (name, username, password) VALUES (?, ?, ?)',
      [name, username, hashedPassword]
    );

    res.status(201).json({ message: 'Buyer registered successfully!' });
  } catch (error) {
    console.error('Buyer registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const buyerLogin = async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, password }: LoginRequest = req.body;

    // Find buyer
    const [buyers] = await db.execute(
      'SELECT * FROM buyers WHERE username = ?',
      [username]
    );

    if (!Array.isArray(buyers) || buyers.length === 0) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    const buyer = buyers[0] as any;

    // Check password
    const isValidPassword = await bcrypt.compare(password, buyer.password);
    if (!isValidPassword) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    // Generate JWT token
    const payload: JwtPayload = {
      userId: buyer.id,
      username: buyer.username,
      role: 'buyer'
    };

    const token = jwt.sign(payload, process.env.JWT_SECRET || 'fallback_secret', {
      expiresIn: '24h'
    });

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: buyer.id,
        name: buyer.name,
        username: buyer.username,
        role: 'buyer'
      }
    });
  } catch (error) {
    console.error('Buyer login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
