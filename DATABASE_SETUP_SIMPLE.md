# 📋 Basit Veritabanı Setup Rehberi

Bu rehber, Oracle database scriptlerini adım adım çalıştırmak için **en basit yöntem**i gösterir.

## ✅ Ön Koşullar

```
✓ Oracle Database 21c veya 23c kurulu
✓ SQL*Plus client erişimi
✓ DBA yetkisi
✓ Komut satırına erişim
```

## 🚀 Adım Adım (Basit Yöntem)

### Adım 1: Veritabanı Klasörüne Git

```bash
cd dbadmin/to_do_list_app
```

### Adım 2: V001 - Schema Oluştur (DBA olarak)

```bash
sqlplus / AS SYSDBA
```

SQL*Plus'ta:
```sql
@migrations/001_schema_creation.sql
EXIT;
```

**Çıktı örneği:**
```
Tablespace TODO_TS created.
User TODO created.
Privileges granted.
```

### Adım 3: V002 - Tabloları Oluştur

```bash
sqlplus todo/welcome123@xe
```

SQL*Plus'ta:
```sql
@migrations/002_create_tables.sql
EXIT;
```

**Çıktı örneği:**
```
Table USER created.
Table TRANSACTION created.
Table AUDIT created.
Triggers created.
Indexes created.
```

### Adım 4: V003 - CRUD Prosedürlerini Oluştur

```bash
sqlplus todo/welcome123@xe
```

SQL*Plus'ta:
```sql
@migrations/003_crud_procedures.sql
EXIT;
```

**Çıktı örneği:**
```
Package PKG_USER_OPS created.
Package PKG_TRANSACTION_OPS created.
Package PKG_AUDIT_OPS created.
Procedures created successfully.
```

### Adım 5: Kurulumu Doğrula

```bash
sqlplus todo/welcome123@xe
```

SQL*Plus'ta:
```sql
-- Tabloları kontrol et
SELECT table_name FROM user_tables;

-- Output:
-- USER
-- TRANSACTION
-- AUDIT

-- Exit
EXIT;
```

## 🔧 Yapılandırma Dosyası Yöntemi

Daha hızlı çalıştırma için `.env.db` dosyası oluştur:

```bash
cat > .env.db << 'EOF'
# Oracle Bağlantı Bilgileri
DB_HOST=localhost
DB_PORT=1521
DB_SID=xe
DB_ADMIN_USER=sys
DB_ADMIN_PASS=oracle
DB_SCHEMA_USER=todo
DB_SCHEMA_PASS=welcome123
EOF
```

Sonra basit script'i çalıştır:

```bash
chmod +x run_migrations_simple.sh
./run_migrations_simple.sh
```

## 📝 run_migrations_simple.sh

```bash
#!/bin/bash

# Konfigürasyonu yükle
if [ ! -f ".env.db" ]; then
  echo "❌ .env.db dosyası bulunamadı!"
  echo "Lütfen .env.db dosyasını oluşturun"
  exit 1
fi

source .env.db

MIGRATIONS_DIR="migrations"
echo "🚀 Veritabanı Migrasyonları Başlıyor..."

# V001: Schema Oluştur
echo ""
echo "📥 V001: Schema oluşturuluyor..."
sqlplus -s /nolog << EOSQL
CONNECT $DB_ADMIN_USER/$DB_ADMIN_PASS@$DB_HOST:$DB_PORT/$DB_SID AS SYSDBA
SET ECHO ON
@$MIGRATIONS_DIR/001_schema_creation.sql
EXIT;
EOSQL

if [ $? -eq 0 ]; then
  echo "✅ V001 tamamlandı"
else
  echo "❌ V001 başarısız"
  exit 1
fi

# V002: Tabloları Oluştur
echo ""
echo "📥 V002: Tablolar oluşturuluyor..."
sqlplus -s /nolog << EOSQL
CONNECT $DB_SCHEMA_USER/$DB_SCHEMA_PASS@$DB_HOST:$DB_PORT/$DB_SID
SET ECHO ON
@$MIGRATIONS_DIR/002_create_tables.sql
EXIT;
EOSQL

if [ $? -eq 0 ]; then
  echo "✅ V002 tamamlandı"
else
  echo "❌ V002 başarısız"
  exit 1
fi

# V003: CRUD Prosedürleri Oluştur
echo ""
echo "📥 V003: CRUD prosedürleri oluşturuluyor..."
sqlplus -s /nolog << EOSQL
CONNECT $DB_SCHEMA_USER/$DB_SCHEMA_PASS@$DB_HOST:$DB_PORT/$DB_SID
SET ECHO ON
@$MIGRATIONS_DIR/003_crud_procedures.sql
EXIT;
EOSQL

if [ $? -eq 0 ]; then
  echo "✅ V003 tamamlandı"
else
  echo "❌ V003 başarısız"
  exit 1
fi

# Kontrol Et
echo ""
echo "✅ Tüm migrasyonlar tamamlandı!"
echo ""
echo "Doğrulama yapılıyor..."

sqlplus -s /nolog << EOSQL
CONNECT $DB_SCHEMA_USER/$DB_SCHEMA_PASS@$DB_HOST:$DB_PORT/$DB_SID
SET ECHO OFF
SELECT 'Tables:' as type, COUNT(*) as count FROM user_tables;
SELECT 'Procedures:' as type, COUNT(*) as count FROM user_procedures;
SELECT 'Packages:' as type, COUNT(*) as count FROM user_packages;
EXIT;
EOSQL

echo ""
echo "🎉 Veritabanı hazır!"
```

## 🪟 Windows Kullanıcıları İçin

### PowerShell Versiyonu

```powershell
# run_migrations.ps1

# Konfigürasyonu yükle
if (-not (Test-Path ".env.db")) {
    Write-Host "❌ .env.db dosyası bulunamadı!" -ForegroundColor Red
    exit 1
}

# .env.db'yi oku
$env_content = Get-Content ".env.db" | Where-Object { $_ -notmatch '^\s*#' -and $_ -notmatch '^\s*$' }
foreach ($line in $env_content) {
    $parts = $line -split '=', 2
    Set-Item -Path "env:\$($parts[0])" -Value $parts[1]
}

$MIGRATIONS_DIR = "migrations"
Write-Host "🚀 Veritabanı Migrasyonları Başlıyor..." -ForegroundColor Green

# V001
Write-Host "📥 V001: Schema oluşturuluyor..." -ForegroundColor Yellow
$sqlplus_cmd = @"
CONNECT $env:DB_ADMIN_USER/$env:DB_ADMIN_PASS@$env:DB_HOST:$env:DB_PORT/$env:DB_SID AS SYSDBA
@$MIGRATIONS_DIR/001_schema_creation.sql
EXIT;
"@

$sqlplus_cmd | sqlplus -s /nolog
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ V001 tamamlandı" -ForegroundColor Green
} else {
    Write-Host "❌ V001 başarısız" -ForegroundColor Red
    exit 1
}

# V002
Write-Host "📥 V002: Tablolar oluşturuluyor..." -ForegroundColor Yellow
$sqlplus_cmd = @"
CONNECT $env:DB_SCHEMA_USER/$env:DB_SCHEMA_PASS@$env:DB_HOST:$env:DB_PORT/$env:DB_SID
@$MIGRATIONS_DIR/002_create_tables.sql
EXIT;
"@

$sqlplus_cmd | sqlplus -s /nolog
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ V002 tamamlandı" -ForegroundColor Green
} else {
    Write-Host "❌ V002 başarısız" -ForegroundColor Red
    exit 1
}

# V003
Write-Host "📥 V003: CRUD prosedürleri oluşturuluyor..." -ForegroundColor Yellow
$sqlplus_cmd = @"
CONNECT $env:DB_SCHEMA_USER/$env:DB_SCHEMA_PASS@$env:DB_HOST:$env:DB_PORT/$env:DB_SID
@$MIGRATIONS_DIR/003_crud_procedures.sql
EXIT;
"@

$sqlplus_cmd | sqlplus -s /nolog
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ V003 tamamlandı" -ForegroundColor Green
} else {
    Write-Host "❌ V003 başarısız" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Tüm migrasyonlar tamamlandı!" -ForegroundColor Green
Write-Host "🎉 Veritabanı hazır!" -ForegroundColor Cyan
```

**Çalıştırmak için:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\run_migrations.ps1
```

## 📋 Çalıştırma Kontrol Listesi

```
[ ] .env.db dosyası oluşturuldu
[ ] DB_HOST doğru (localhost)
[ ] DB_PORT doğru (1521)
[ ] DB_SID doğru (xe)
[ ] V001 başarıyla çalıştırıldı
[ ] V002 başarıyla çalıştırıldı
[ ] V003 başarıyla çalıştırıldı
[ ] Doğrulama yapıldı
[ ] .migration_status güncellendi
[ ] Git'e commit edildi
```

## 🐛 Hata Çözümleri

### Error: ORA-01017: invalid username/password

**Çözüm:**
```bash
# .env.db dosyasındaki şifreyi kontrol et
# V001'i DBA olarak çalıştırdığından emin ol
```

### Error: ORA-01536: space quota exceeded

**Çözüm:**
```bash
# Tablespace'in yeterli alanı olduğundan emin ol
# V001 başarıyla çalıştırıldığından emin ol
```

### Error: table or view does not exist

**Çözüm:**
```bash
# V002 başarıyla çalıştırıldığından emin ol
# Doğru user'dan bağlanıyor musun kontrol et
```

## 📊 Başarılı Sonuç Örneği

```
🚀 Veritabanı Migrasyonları Başlıyor...

📥 V001: Schema oluşturuluyor...
Tablespace TODO_TS created.
User TODO created.
✅ V001 tamamlandı

📥 V002: Tablolar oluşturuluyor...
Table USER created.
Table TRANSACTION created.
Table AUDIT created.
✅ V002 tamamlandı

📥 V003: CRUD prosedürleri oluşturuluyor...
Package PKG_USER_OPS created.
Package PKG_TRANSACTION_OPS created.
Package PKG_AUDIT_OPS created.
✅ V003 tamamlandı

✅ Tüm migrasyonlar tamamlandı!

Tables:      3
Procedures:  9
Packages:    3

🎉 Veritabanı hazır!
```

## 🎯 Özet

1. **Basit Yöntem**: SQL*Plus'ta adım adım çalıştır (en güvenli)
2. **Config Dosyası**: .env.db + bash/PowerShell script
3. **Otomatasyon**: GitHub Actions (ileri seviye)

**Önemli**: Her zaman test ortamında ilk çalıştırın! 🔒

---

**Başarıyla kurulum yapılmış olmalı! 🎉**
