import express from 'express';
import { sellerRegister, sellerLogin, buyerRegister, buyerLogin } from '../controllers/authController';

const router = express.Router();

// Seller routes
router.post('/seller/register', sellerRegister);
router.post('/seller/login', sellerLogin);

// Buyer routes
router.post('/buyer/register', buyerRegister);
router.post('/buyer/login', buyerLogin);

export default router;
