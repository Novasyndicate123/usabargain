# NovaBargains Full Setup & Test Script

# --- Configuration ---
$projectPath = "$env:USERPROFILE\Desktop\NovaBargains"
$venvActivate = "$projectPath\venv\Scripts\Activate.ps1"
$initDbScript = "$projectPath\init_db.py"
$scraperScript = "$projectPath\scraper_live.py"
$dbPath = "$projectPath\data\bargains.db"

# --- Change to project directory ---
Set-Location -Path $projectPath

# --- Activate virtual environment ---
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvActivate
} else {
    Write-Host "ERROR: Virtual environment not found at $venvActivate" -ForegroundColor Red
    exit 1
}

# --- Create init_db.py dynamically ---
@"
import sqlite3
import os

DB_PATH = os.path.join('data', 'bargains.db')

def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT,
            url TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Database initialized with deals table.')

if __name__ == '__main__':
    init_db()
"@ | Set-Content -Path $initDbScript -Encoding UTF8

Write-Host "Running database initialization..." -ForegroundColor Cyan
python $initDbScript

Write-Host "Running scraper..." -ForegroundColor Cyan
python $scraperScript

Write-Host "Querying inserted deals..." -ForegroundColor Cyan
$query = @"
import sqlite3
conn = sqlite3.connect(r'$dbPath')
cursor = conn.cursor()
cursor.execute('SELECT title, price FROM deals LIMIT 10')
rows = cursor.fetchall()
conn.close()
for row in rows:
    print(f'Title: {row[0]}, Price: {row[1]}')
"@

python -c $query

Write-Host "Done." -ForegroundColor Green
