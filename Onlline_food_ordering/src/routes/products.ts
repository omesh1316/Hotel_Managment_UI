import express from 'express';
import { authenticateToken, requireRole } from '../middleware/auth';
import { 
  getAllProducts, 
  getSellerProducts, 
  addProduct, 
  deleteProduct, 
  getSellerAnalytics 
} from '../controllers/productController';

const router = express.Router();

// Public routes
router.get('/', getAllProducts);

// Protected routes
router.get('/seller', authenticateToken, requireRole('seller'), getSellerProducts);
router.post('/', authenticateToken, requireRole('seller'), addProduct);
router.delete('/:productId', authenticateToken, requireRole('seller'), deleteProduct);
router.get('/analytics', authenticateToken, requireRole('seller'), getSellerAnalytics);

export default router;
