import express from 'express';
import { authenticateToken, requireRole } from '../middleware/auth';
import { 
  placeOrder, 
  getBuyerOrders, 
  getSellerOrders, 
  updateOrderStatus 
} from '../controllers/orderController';

const router = express.Router();

// Buyer routes
router.post('/:productId', authenticateToken, requireRole('buyer'), placeOrder);
router.get('/buyer', authenticateToken, requireRole('buyer'), getBuyerOrders);

// Seller routes
router.get('/seller', authenticateToken, requireRole('seller'), getSellerOrders);
router.put('/:orderId/status', authenticateToken, requireRole('seller'), updateOrderStatus);

export default router;
