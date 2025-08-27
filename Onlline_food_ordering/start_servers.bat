@echo off
echo ========================================
echo 🚀 Starting Food Ordering System
echo ========================================
echo.
echo 📱 Main App: http://localhost:5000
echo 🛠️ Admin Panel: http://localhost:5001
echo.
echo Starting servers...
echo.

REM Start main Flask app in background
start "Main App" cmd /k "python app.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start admin panel in background
start "Admin Panel" cmd /k "python admin_panel.py"

echo ✅ Both servers started!
echo.
echo 🌐 Open these URLs in your browser:
echo    Main App: http://localhost:5000
echo    Admin Panel: http://localhost:5001
echo.
pause
