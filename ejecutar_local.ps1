# Ejecuta el proyecto en tu equipo (Windows PowerShell) conectado a Supabase.
# Las credenciales se piden por teclado y solo viven mientras esta ventana esté abierta.
# Uso:  powershell -ExecutionPolicy Bypass -File .\ejecutar_local.ps1
$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $raiz

Write-Host "=== Datos de conexión: Supabase -> Connect -> Transaction pooler ==="
if (-not $env:DB_HOST) { $env:DB_HOST = Read-Host "DB_HOST (host del pooler)" }
if (-not $env:DB_USER) { $env:DB_USER = Read-Host "DB_USER (postgres.xxxxxxxx)" }
if (-not $env:DB_PASSWORD) {
    $seg = Read-Host "DB_PASSWORD (no se muestra)" -AsSecureString
    $env:DB_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($seg))
}
if (-not $env:DB_NAME) { $env:DB_NAME = "postgres" }
if (-not $env:DB_PORT) { $env:DB_PORT = "6543" }
if (-not $env:API_KEY) { $env:API_KEY = "clave-local-de-prueba" }              # solo para pruebas locales
if (-not $env:JWT_SECRET_KEY) { $env:JWT_SECRET_KEY = "secreto-local-de-prueba" }

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) { Write-Host "No se encontró Python 3. Instálalo desde python.org (marca 'Add to PATH')."; exit 1 }
if (-not (Test-Path "$raiz\venv")) { Write-Host "Creando entorno virtual..."; & $py.Source -m venv venv }
$python = "$raiz\venv\Scripts\python.exe"
Write-Host "Instalando dependencias..."
& $python -m pip install -q Flask Flask-Cors Flask-Limiter PyJWT psycopg2-binary python-dotenv

$servicios = @(
    @{ n = "rutas";       d = "servicio_rutas";       p = 5001 },
    @{ n = "operaciones"; d = "servicio_operaciones"; p = 5002 },
    @{ n = "monitoreo";   d = "servicio_monitoreo";   p = 5003 }
)
foreach ($s in $servicios) {
    # Cada servicio abre su propia ventana y hereda las variables de esta sesión
    $cmd = "`$env:SERVER_PORT='$($s.p)'; Set-Location '$raiz\microservicios\$($s.d)'; & '$python' app.py"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmd
}
Start-Sleep -Seconds 8

Write-Host "--- Comprobando servicios ---"
$pruebas = @( @("rutas",5001,"/rutas"), @("operaciones",5002,"/operaciones/paraderos/1"), @("monitoreo",5003,"/") )
foreach ($t in $pruebas) {
    try {
        $r = Invoke-WebRequest -UseBasicParsing -Headers @{ "X-API-Key" = $env:API_KEY } -Uri "http://127.0.0.1:$($t[1])$($t[2])"
        Write-Host "  $($t[0]) (puerto $($t[1])): HTTP $($r.StatusCode)"
    } catch { Write-Host "  $($t[0]) (puerto $($t[1])): ERROR -> revisa su ventana" }
}

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "Iniciando frontend -> abre la dirección que muestre Vite (normalmente http://localhost:5173)"
    Set-Location "$raiz\frontend"
    npm install --no-audit --no-fund
    npm run dev
} else {
    Write-Host "Node.js no está instalado: solo se iniciaron las APIs. Instálalo desde nodejs.org para ver la página."
}