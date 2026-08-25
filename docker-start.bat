@echo off
REM ============================================================
REM ViT vs CNN ÔÇö Script de lancement Docker (Windows)
REM ============================================================

echo ============================================================
echo   Lancement de ViT vs CNN via Docker Compose
echo ============================================================

where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERREUR] Docker n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Docker Desktop et vous assurer qu'il est demarre.
    pause
    exit /b 1
)

if not exist .env (
    echo [INFO] Creation du fichier .env depuis .env.example...
    copy .env.example .env
)

echo [INFO] Construction et demarrage des conteneurs...
docker compose up --build -d

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo   Application lancee avec succes !
    echo ============================================================
    echo   - Frontend D├®mo  : http://localhost:3000
    echo   - Backend API    : http://localhost:8000/docs
    echo   - MLflow (opt.)  : http://localhost:5000 (lancer avec: docker compose --profile mlflow up)
    echo ============================================================
    echo Pour voir les logs en direct : docker compose logs -f
    echo Pour arreter l'application    : docker compose down
    echo.
) else (
    echo [ERREUR] Une erreur est survenue lors du demarrage des conteneurs.
)

pause
