@echo off
echo ========================================
echo      DAWN UPGRADE SYSTEM DEMO
echo ========================================
echo.
echo This will show you how upgrades work!
echo.

echo Running simple demonstration...
echo.

python demo_upgrades_simple.py

echo.
echo ========================================
echo.
echo To use upgrades with your real DAWN:
echo.
echo 1. Copy dawn_upgrade_system.py to core\
echo 2. Add to your launch script:
echo    from dawn_upgrade_system import integrate_upgrade_system
echo    engine = integrate_upgrade_system(engine)
echo 3. Install upgrades:
echo    engine.install_upgrade('creative_expression')
echo.
echo ========================================
echo.

pause