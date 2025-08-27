from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'admin_secret_key_2024'

# MySQL Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # No password for XAMPP
    database='shop_db'
)
cursor = conn.cursor(dictionary=True)

# Admin Dashboard Home
@app.route('/')
def admin_home():
    try:
        # Get real-time statistics
        cursor.execute("SELECT COUNT(*) as total_sellers FROM sellers")
        total_sellers = cursor.fetchone()['total_sellers']
        
        cursor.execute("SELECT COUNT(*) as total_buyers FROM buyers")
        total_buyers = cursor.fetchone()['total_buyers']
        
        cursor.execute("SELECT COUNT(*) as total_products FROM products")
        total_products = cursor.fetchone()['total_products']
        
        cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']
        
        # Get recent orders
        cursor.execute("""
            SELECT orders.*, products.name as product_name, 
                   buyers.name as buyer_name, sellers.name as seller_name
            FROM orders 
            JOIN products ON orders.product_id = products.id
            JOIN buyers ON orders.buyer_id = buyers.id
            JOIN sellers ON products.seller_id = sellers.id
            ORDER BY orders.id DESC LIMIT 10
        """)
        recent_orders = cursor.fetchall()
        
        # Get top sellers
        cursor.execute("""
            SELECT sellers.name, COUNT(orders.id) as order_count, SUM(products.price) as revenue
            FROM sellers
            LEFT JOIN products ON sellers.id = products.seller_id
            LEFT JOIN orders ON products.id = orders.product_id
            GROUP BY sellers.id, sellers.name
            ORDER BY revenue DESC
            LIMIT 5""")
        top_sellers = cursor.fetchall()
        
        return render_template('admin_home.html', 
                             total_sellers=total_sellers,
                             total_buyers=total_buyers,
                             total_products=total_products,
                             total_orders=total_orders,
                             recent_orders=recent_orders,
                             top_sellers=top_sellers)
    except Exception as e:
        return f"Error: {str(e)}"

# Routes Listing Page
@app.route('/routes')
def admin_routes():
    # Define all routes for both applications
    admin_routes = [
        {
            'category': '📊 Dashboard',
            'routes': [
                {'path': '/', 'method': 'GET', 'description': 'Main admin dashboard with real-time stats'},
                {'path': '/api/stats', 'method': 'GET', 'description': 'JSON API for live statistics'},
                {'path': '/api/recent-orders', 'method': 'GET', 'description': 'JSON API for recent orders'}
            ]
        },
        {
            'category': '👥 User Management',
            'routes': [
                {'path': '/users', 'method': 'GET', 'description': 'View and manage all sellers and buyers'},
                {'path': '/delete-user/<user_type>/<user_id>', 'method': 'GET', 'description': 'Delete a user (seller or buyer)'}
            ]
        },
        {
            'category': '📦 Order Management',
            'routes': [
                {'path': '/orders', 'method': 'GET', 'description': 'View all orders with details'},
                {'path': '/update-order-status/<order_id>', 'method': 'POST', 'description': 'Update order status'}
            ]
        },
        {
            'category': '🛍️ Product Management',
            'routes': [
                {'path': '/products', 'method': 'GET', 'description': 'View all products with seller info'},
                {'path': '/delete-product/<product_id>', 'method': 'GET', 'description': 'Delete a product'}
            ]
        },
        {
            'category': '🔗 System Info',
            'routes': [
                {'path': '/routes', 'method': 'GET', 'description': 'This page - view all available routes'}
            ]
        }
    ]
    
    main_app_routes = [
        {
            'category': '🏠 Public Pages',
            'routes': [
                {'path': '/', 'method': 'GET', 'description': 'Home page'},
                {'path': '/seller_register', 'method': 'GET/POST', 'description': 'Seller registration form'},
                {'path': '/seller_login', 'method': 'GET/POST', 'description': 'Seller login form'},
                {'path': '/buyer_register', 'method': 'GET/POST', 'description': 'Buyer registration form'},
                {'path': '/buyer_login', 'method': 'GET/POST', 'description': 'Buyer login form'}
            ]
        },
        {
            'category': '🏪 Seller Features',
            'routes': [
                {'path': '/seller/<seller_id>', 'method': 'GET', 'description': 'Seller dashboard with products and analytics'},
                {'path': '/seller/<seller_id>/add', 'method': 'POST', 'description': 'Add new product'},
                {'path': '/seller/<seller_id>/delete/<product_id>', 'method': 'GET', 'description': 'Delete product'},
                {'path': '/seller/<seller_id>/orders', 'method': 'GET', 'description': 'View seller orders'},
                {'path': '/seller/<seller_id>/orders/update/<order_id>', 'method': 'POST', 'description': 'Update order status'}
            ]
        },
        {
            'category': '🛒 Buyer Features',
            'routes': [
                {'path': '/buyer/<buyer_id>', 'method': 'GET', 'description': 'Buyer dashboard with available products'},
                {'path': '/buyer/<buyer_id>/order/<product_id>', 'method': 'GET/POST', 'description': 'Place order for product'},
                {'path': '/buyer/<buyer_id>/orders', 'method': 'GET', 'description': 'View buyer order history'}
            ]
        },
        {
            'category': '🛠️ Admin Features (Main App)',
            'routes': [
                {'path': '/admin/dashboard', 'method': 'GET', 'description': 'Admin dashboard in main app'},
                {'path': '/admin/users', 'method': 'GET', 'description': 'Admin users management'},
                {'path': '/admin/orders', 'method': 'GET', 'description': 'Admin orders management'}
            ]
        },
        {
            'category': '🔐 Authentication',
            'routes': [
                {'path': '/logout', 'method': 'GET', 'description': 'Logout and clear session'}
            ]
        }
    ]
    
           # Calculate totals
    admin_total = sum(len(category['routes']) for category in admin_routes)
    main_total = sum(len(category['routes']) for category in main_app_routes)
    total_routes = admin_total + main_total
    
    return render_template('admin_routes.html', 
                         admin_routes=admin_routes, 
                         main_app_routes=main_app_routes,
                         admin_total=admin_total,
                         main_total=main_total,
                         total_routes=total_routes)


# API Endpoints for real-time data
@app.route('/api/stats')
def get_stats():
    try:
        cursor.execute("SELECT COUNT(*) as total_sellers FROM sellers")
        total_sellers = cursor.fetchone()['total_sellers']
        
        cursor.execute("SELECT COUNT(*) as total_buyers FROM buyers")
        total_buyers = cursor.fetchone()['total_buyers']
        
        cursor.execute("SELECT COUNT(*) as total_products FROM products")
        total_products = cursor.fetchone()['total_products']
        
        cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']
        
        return jsonify({
            'total_sellers': total_sellers,
            'total_buyers': total_buyers,
            'total_products': total_products,
            'total_orders': total_orders,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recent-orders')
def get_recent_orders():
    try:
        cursor.execute("""
            SELECT orders.*, products.name as product_name, 
                   buyers.name as buyer_name, sellers.name as seller_name
            FROM orders 
            JOIN products ON orders.product_id = products.id
            JOIN buyers ON orders.buyer_id = buyers.id
            JOIN sellers ON products.seller_id = sellers.id
            ORDER BY orders.id DESC LIMIT 10
        """)
        orders = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON
        for order in orders:
            if 'created_at' in order and order['created_at']:
                order['created_at'] = order['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)})

# Users Management
@app.route('/users')
def admin_users():
    try:
        cursor.execute("SELECT * FROM sellers")
        sellers = cursor.fetchall()
        
        cursor.execute("SELECT * FROM buyers")
        buyers = cursor.fetchall()
        
        return render_template('admin_users.html', sellers=sellers, buyers=buyers)
    except Exception as e:
        return f"Error: {str(e)}"

# Orders Management
@app.route('/orders')
def admin_orders():
    try:
        cursor.execute("""
            SELECT orders.*, products.name as product_name, 
                   buyers.name as buyer_name, sellers.name as seller_name
            FROM orders 
            JOIN products ON orders.product_id = products.id
            JOIN buyers ON orders.buyer_id = buyers.id
            JOIN sellers ON products.seller_id = sellers.id
            ORDER BY orders.id DESC
        """)
        orders = cursor.fetchall()
        
        return render_template('admin_orders.html', orders=orders)
    except Exception as e:
        return f"Error: {str(e)}"

# Products Management
@app.route('/products')
def admin_products():
    try:
        cursor.execute("""
            SELECT products.*, sellers.name as seller_name
            FROM products
            JOIN sellers ON products.seller_id = sellers.id
            ORDER BY products.id DESC
        """)
        products = cursor.fetchall()
        
        return render_template('admin_products.html', products=products)
    except Exception as e:
        return f"Error: {str(e)}"

# Delete User
@app.route('/delete-user/<user_type>/<int:user_id>')
def delete_user(user_type, user_id):
    try:
        if user_type == 'seller':
            cursor.execute("DELETE FROM sellers WHERE id = %s", (user_id,))
        elif user_type == 'buyer':
            cursor.execute("DELETE FROM buyers WHERE id = %s", (user_id,))
        
        conn.commit()
        flash(f"{user_type.title()} deleted successfully!")
        return redirect(url_for('admin_users'))
    except Exception as e:
        flash(f"Error deleting user: {str(e)}")
        return redirect(url_for('admin_users'))

# Update Order Status
@app.route('/update-order-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    try:
        new_status = request.form['status']
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
        conn.commit()
        flash("Order status updated successfully!")
        return redirect(url_for('admin_orders'))
    except Exception as e:
        flash(f"Error updating order: {str(e)}")
        return redirect(url_for('admin_orders'))

# Delete Product
@app.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        flash("Product deleted successfully!")
        return redirect(url_for('admin_products'))
    except Exception as e:
        flash(f"Error deleting product: {str(e)}")
        return redirect(url_for('admin_products'))

if __name__ == '__main__':
    print("🚀 Admin Panel starting on http://localhost:5001")
    print("📊 Dashboard: http://localhost:5001")
    print("👥 Users: http://localhost:5001/users")
    print("📦 Orders: http://localhost:5001/orders")
    print("🛍️ Products: http://localhost:5001/products")
    print("🔗 Routes: http://localhost:5001/routes")
    app.run(port=5001, debug=True)
