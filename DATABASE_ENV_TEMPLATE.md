# 📝 Veritabanı Konfigürasyon Şablonu

Bu dosyayı `dbadmin/[project_name]/` klasöründe `.env.db` olarak kaydetin.

## 🔧 Basit Konfigürasyon (.env.db)

```bash
# Oracle Database Bağlantı Bilgileri
# Bu değerleri kendi sisteminize göre güncelleyin

# ============================================
# ORACLE SUNUCUSU
# ============================================
DB_HOST=localhost
DB_PORT=1521
DB_SID=xe

# ============================================
# ADMIN KULLANIŞI (DBA) - SCHEMA OLUŞTURMAK İÇİN
# ============================================
DB_ADMIN_USER=sys
DB_ADMIN_PASS=oracle

# ============================================
# SCHEMA KULLANIŞI - TABLOLAR VE PROSEDÜRLER İÇİN
# ============================================
DB_SCHEMA_USER=todo
DB_SCHEMA_PASS=welcome123

# ============================================
# OPSIYONEL AYARLAR
# ============================================
# DB_CHARSET=UTF8
# DB_NATIONAL_CHARSET=AL16UTF16
# SQLPLUS_PATH=/opt/oracle/client/bin/sqlplus
```

## 💻 Kolay Kullanım

### 1. .env.db Dosyası Oluştur

Proje klasöründe:

```bash
cd dbadmin/to_do_list_app
cat > .env.db << 'EOF'
DB_HOST=localhost
DB_PORT=1521
DB_SID=xe
DB_ADMIN_USER=sys
DB_ADMIN_PASS=oracle
DB_SCHEMA_USER=todo
DB_SCHEMA_PASS=welcome123
EOF
```

### 2. Değerleri Düzenle

Sisteminize göre değişik ise:

```bash
# Örnek: Uzak sunucu bağlantısı
DB_HOST=192.168.1.100
DB_PORT=1521
DB_SID=ORCL
DB_ADMIN_USER=sys
DB_ADMIN_PASS=your_admin_pass
DB_SCHEMA_USER=myapp
DB_SCHEMA_PASS=myapp_pass
```

### 3. Manuel Çalıştır

```bash
# V001
sqlplus /nolog << EOF
CONNECT ${DB_ADMIN_USER}/${DB_ADMIN_PASS}@${DB_HOST}:${DB_PORT}/${DB_SID} AS SYSDBA
@migrations/001_schema_creation.sql
EXIT;
EOF

# V002
sqlplus /nolog << EOF
CONNECT ${DB_SCHEMA_USER}/${DB_SCHEMA_PASS}@${DB_HOST}:${DB_PORT}/${DB_SID}
@migrations/002_create_tables.sql
EXIT;
EOF

# V003
sqlplus /nolog << EOF
CONNECT ${DB_SCHEMA_USER}/${DB_SCHEMA_PASS}@${DB_HOST}:${DB_PORT}/${DB_SID}
@migrations/003_crud_procedures.sql
EXIT;
EOF
```

## 🔐 Güvenlik Notları

✅ **Yapın:**
- Local geliştirme için basit şifreler kullanabilirsiniz
- .env.db dosyasını .gitignore'a ekleyin
- Production'da güçlü şifreler kullanın
- Hassas verileri konfigürasyon dosyalarına koymayın

❌ **Yapmayın:**
- Admin şifresini commit etmeyin
- .env.db dosyasını paylaşmayın
- Test şifrelerini production'da kullanmayın
- Şifreleri source codda bırakmayın

## 📦 Farklı Senaryolar

### Scenario 1: Local Oracle XE

```env
DB_HOST=localhost
DB_PORT=1521
DB_SID=xe
DB_ADMIN_USER=sys
DB_ADMIN_PASS=oracle
DB_SCHEMA_USER=myapp
DB_SCHEMA_PASS=myapp123
```

### Scenario 2: Docker Oracle

```env
DB_HOST=oracle-db
DB_PORT=1521
DB_SID=ORCLCDB
DB_ADMIN_USER=sys
DB_ADMIN_PASS=Oradoc_db1
DB_SCHEMA_USER=myapp
DB_SCHEMA_PASS=myapp123
```

### Scenario 3: Enterprise Oracle

```env
DB_HOST=oracle.company.com
DB_PORT=1521
DB_SID=PROD
DB_ADMIN_USER=sys
DB_ADMIN_PASS=${ORACLE_ADMIN_PASS}
DB_SCHEMA_USER=myapp
DB_SCHEMA_PASS=${ORACLE_APP_PASS}
```

### Scenario 4: Oracle Cloud

```env
DB_HOST=xxx-xxxxx.us-xxxx-1.oraclecloud.com
DB_PORT=1522
DB_SID=ORCL_TP
DB_ADMIN_USER=sys
DB_ADMIN_PASS=YourPasswordHere
DB_SCHEMA_USER=myapp
DB_SCHEMA_PASS=YourAppPassword
```

## ✅ Konfigürasyonu Test Et

```bash
# Bağlantıyı test et
sqlplus -v

# Admin bağlantısı test et
sqlplus /nolog << EOF
CONNECT sys/oracle@localhost:1521/xe AS SYSDBA
SELECT * FROM v\$instance;
EXIT;
EOF

# Schema bağlantısı test et (V001'den sonra)
sqlplus /nolog << EOF
CONNECT myapp/myapp123@localhost:1521/xe
SELECT * FROM user_tables;
EXIT;
EOF
```

## 🐛 Yaygın Hata ve Çözümler

### Error: "ORA-12514: TNS:listener does not currently know of service"

**Sebep:** DB_SID yanlış  
**Çözüm:**
```bash
# Kullanılabilir SID'leri listele
lsnrctl services

# Ya da listener.ora'yı kontrol et
cat $ORACLE_HOME/network/admin/listener.ora
```

### Error: "ORA-01017: invalid username/password"

**Sebep:** Admin şifresi yanlış  
**Çözüm:**
```bash
# SQL*Plus'ta şifreyi kontrol et
sqlplus / AS SYSDBA

# Ya da Oracle'ı baştan start et
lsnrctl stop
lsnrctl start
```

### Error: "ORA-12505: TNS:listener could not resolve the CONNECT_DATA"

**Sebep:** Host ya da Port yanlış  
**Çözüm:**
```bash
# Oracle listener'ı kontrol et
sqlplus /nolog
SHOW PARAMETERS service_names;
EXIT;
```

## 📚 Yardımcı Komutlar

```bash
# Veritabanı durumunu kontrol et
sqlplus / AS SYSDBA
SELECT status FROM v$instance;

# Tablespace'leri listele
SELECT tablespace_name FROM dba_tablespaces;

# User'ları listele
SELECT username FROM dba_users;

# Bağlantı stringini oluştur
tnsping xe

# Listener'ı yeniden başlat
lsnrctl stop
lsnrctl start
```

## 🎯 Adım Adım Örnek

```bash
# 1. Proje klasörüne git
cd dbadmin/to_do_list_app

# 2. .env.db oluştur
cat > .env.db << 'EOF'
DB_HOST=localhost
DB_PORT=1521
DB_SID=xe
DB_ADMIN_USER=sys
DB_ADMIN_PASS=oracle
DB_SCHEMA_USER=todo
DB_SCHEMA_PASS=welcome123
EOF

# 3. V001 çalıştır
sqlplus -s /nolog << 'EOF'
CONNECT sys/oracle@localhost:1521/xe AS SYSDBA
@migrations/001_schema_creation.sql
EXIT;
EOF

# 4. V002 çalıştır
sqlplus -s /nolog << 'EOF'
CONNECT todo/welcome123@localhost:1521/xe
@migrations/002_create_tables.sql
EXIT;
EOF

# 5. V003 çalıştır
sqlplus -s /nolog << 'EOF'
CONNECT todo/welcome123@localhost:1521/xe
@migrations/003_crud_procedures.sql
EXIT;
EOF

# 6. Kontrol et
sqlplus -s /nolog << 'EOF'
CONNECT todo/welcome123@localhost:1521/xe
SELECT COUNT(*) as tables FROM user_tables;
SELECT COUNT(*) as procedures FROM user_procedures;
EXIT;
EOF

# 7. .migration_status güncelle ve commit et
git add .env.db migrations/
git commit -m "Add database migrations v001-v003"
git push
```

## 🚀 Hızlı Start

Basitçe:

```bash
# 1. .env.db kopyala
cp DATABASE_ENV_TEMPLATE.md dbadmin/to_do_list_app/.env.db

# 2. Değerleri güncelle
nano dbadmin/to_do_list_app/.env.db

# 3. Manuel çalıştır
cd dbadmin/to_do_list_app

# V001 (DBA)
sqlplus / AS SYSDBA @migrations/001_schema_creation.sql

# V002 (Schema user)
sqlplus todo/welcome123@xe @migrations/002_create_tables.sql

# V003 (Schema user)
sqlplus todo/welcome123@xe @migrations/003_crud_procedures.sql

# Bitti! 🎉
```

---

**Kolay! Herhangi bir karmaşık configuration'a ihtiyaç yok! 🚀**
