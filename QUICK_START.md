# 🚀 Hızlı Başlangıç - Proje Girişi ve Tmux İzleme

Adım adım rehber: Proje tanımla → Tmux'ta izle → Kodları incele

---

## 📋 Step 1: Proje Dosyası Oluştur

### Seçenek A: Mevcut projects.json Kullan

`projects.json` dosyasını aç ve editle:

```json
[
  {
    "name": "TO DO LIST APP",
    "description": "Implement TO DO list application with add, edit, delete, and mark complete functionalities.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

### Seçenek B: Yeni Proje Ekle

Dosyayı aç ve yeni proje ekle:

```json
[
  {
    "name": "E-Commerce Platform",
    "description": "Build e-commerce platform with products, orders, payments, and user management",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  },
  {
    "name": "Blog App",
    "description": "Create blogging platform with posts, comments, categories and search functionality",
    "priority": "medium",
    "domains": ["backend", "frontend", "database"]
  }
]
```

### Seçenek C: İnteraktif Mode (Komut Satırında Gir)

Komut satırında projeyi canlı olarak gir:

```bash
python run_with_tmux.py --interactive --attach
```

---

## 🎯 Step 2: Tmux ile Çalıştır

### Sadece Çalıştır (Arka planda)
```bash
python run_with_tmux.py --projects projects.json
```

**Çıktı:**
```
🚀 Creating tmux session 'agent_team'...
🛠️  Setting up tmux session...

==============================================================================
🤖 AGENT TEAM ORCHESTRATOR
==============================================================================

📋 Running: python main.py --projects projects.json 2>&1 | tee .agent_logs/orchestrator.log

✅ Agents started in tmux panes!

📊 Monitor Status:
  • Session: agent_team
  • Logs: .agent_logs/
  • Commands:
    - Attach: tmux attach-session -t agent_team
    - Kill: tmux kill-session -t agent_team
    - List panes: tmux list-panes -t agent_team -a

💡 To attach to the session, run:
   tmux attach-session -t agent_team
```

### Çalıştır ve Hemen Bağlan (Önerilen)
```bash
python run_with_tmux.py --projects projects.json --attach
```

---

## 👀 Step 3: Tmux'ta İzle

### Terminal'de Göreceksen:

```
╔═════════════════════════════════════════════════════════════════╗
║                 🚀 AGENT TEAM MONITORING                        ║
╚═════════════════════════════════════════════════════════════════╝

┌──────────────────────────────┬──────────────────────────────┐
│                              │                              │
│ 📋 ORCHESTRATOR PANE         │ 🔧 TASK CREATOR PANE        │
│                              │                              │
│ 🚀 Processing Project: TO DO │ 📋 Breaking project into    │
│    LIST APP                  │    domain tasks...          │
│ Priority: HIGH               │ ✓ Main task created:        │
│ Description: Implement...    │   Backend Development...    │
│                              │ ✓ Main task created:        │
│ 📋 Task Creator Agent is     │   Frontend Development...   │
│    breaking project...       │ ✓ Main task created:        │
│ ✓ Main task created:         │   Database Design...        │
│ ✓ Main task created:         │                              │
│                              │                              │
├──────────────────────────────┼──────────────────────────────┤
│                              │                              │
│ ☕ BACKEND AGENT PANE        │ 🎨 FRONTEND AGENT PANE      │
│                              │                              │
│ 🔧 Backend Agent is creating │ 🎨 Frontend Agent is        │
│    Java/Spring Boot code...  │    creating React code...   │
│ ✓ Backend API Implementation │ ✓ Setup Next.js Project     │
│ ✓ Database Schema & Mapping  │ ✓ Create Base Components    │
│ Generated: pom.xml...        │ Generated: package.json...  │
│                              │                              │
├──────────────────────────────┴──────────────────────────────┤
│                                                              │
│ 💾 DATABASE AGENT PANE                                       │
│                                                              │
│ 💾 Database Agent is creating Oracle/PL-SQL code...         │
│ ✓ Database Schema Design                                    │
│ ✓ Query Optimization                                        │
│ Generated: migrations/ folder with:                         │
│   - 001_schema_creation.sql                                 │
│   - 002_create_tables.sql                                   │
│   - 003_crud_procedures.sql                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎮 Step 4: Tmux Komutları - İzleme

### Pane'ler Arasında Dolaş

**Tmux'ta bu tuş kombinasyonlarını kullan:**

```
Ctrl+B (basılı tut) → Sonra:

1. Backend Agent'e git:
   Ctrl+B → 1

2. Frontend Agent'e git:
   Ctrl+B → 2

3. Database Agent'e git:
   Ctrl+B → 4  (ya da 5)

4. Üst pane'e git:
   Ctrl+B → ↑

5. Alt pane'e git:
   Ctrl+B → ↓

6. Sol pane'e git:
   Ctrl+B → ←

7. Sağ pane'e git:
   Ctrl+B → →
```

### Detaylı İnceleme

```
Ctrl+B → z          # Pane'i büyült (full screen)
Ctrl+B → z          # Tekrar normalleştir
Ctrl+B → [          # Scroll mode (kaydırma)
     ↑ ↓            # OK tuşlarıyla scroll et
     Page Up/Down   # Daha hızlı kaydırma
     /error         # "error" ara
     n              # Sonraki eşleşmeyi bul
Escape              # Scroll moddan çık
```

### Session'dan Ayrıl (Işlemler Devam Eder!)

```
Ctrl+B → D          # Session'dan ayrıl (işlem durmuyor)
```

Tekrar bağlan:
```bash
tmux attach-session -t agent_team
```

---

## 📊 Step 5: Gerçek Zamanlı Log İzleme

### Terminal'de Özel Agent'i İzle

**Tmux'ta işlem görürken, başka bir terminal açıp:**

```bash
# Backend Agent'in işini izle
tail -f .agent_logs/backend_agent.log

# Frontend Agent'in işini izle
tail -f .agent_logs/frontend_agent.log

# Database Agent'in işini izle
tail -f .agent_logs/database_agent.log

# Hataları bul
tail -f .agent_logs/backend_agent.log | grep -i "error"
```

### Tüm Logları Göster

```bash
python run_with_tmux.py --logs
```

**Çıktı:**
```
======================================================================
📋 AGENT LOGS
======================================================================

──────────────────────────────────────────────────────────────────────
📌 TASK CREATOR
──────────────────────────────────────────────────────────────────────
2024-05-07 10:30:45 [INFO] task_creator: Initialized Task Creator Agent (role: task_creator)
2024-05-07 10:30:45 [INFO] task_creator: Created 3 main tasks from project: TO DO LIST APP
2024-05-07 10:30:46 [INFO] task_creator: Saved task to tasks/backend_development_todo_list_app.md

──────────────────────────────────────────────────────────────────────
📌 BACKEND
──────────────────────────────────────────────────────────────────────
2024-05-07 10:30:47 [INFO] backend_agent: Initialized Backend Agent (role: backend_developer)
2024-05-07 10:30:47 [INFO] backend_agent: Created 5 backend subtasks
...
```

---

## 🎯 ÖRNEK WORKFLOW

### Örnek 1: TO DO LIST APP ile Başla

**Terminal 1:**
```bash
cd /path/to/project
python run_with_tmux.py --projects projects.json --attach
```

**Tmux'ta görürsün:**
```
✓ Backend Development yapılıyor
  - User Entity oluşturuluyor
  - Task Entity oluşturuluyor
  - Repositories oluşturuluyor
  
✓ Frontend Development yapılıyor
  - Components oluşturuluyor
  - Pages oluşturuluyor
  
✓ Database Design yapılıyor
  - Schema oluşturuluyor
  - Tables oluşturuluyor
  - Procedures oluşturuluyor
```

**Terminal 2 (isteğe bağlı - detaylı izleme):**
```bash
# Backend'in Entity'lerini oluşturdığunu görmek
tail -f .agent_logs/backend_agent.log | grep "entity"

# Output:
# Generated entity: User
# Generated entity: Task
# Generated entity: Audit
```

### Örnek 2: İnteraktif Mode ile Yeni Proje

```bash
python run_with_tmux.py --interactive --attach
```

**Sorular cevapla:**
```
🚀 AGENT TEAM PROJECT INPUT
=================================================================================

📝 Project name: E-Commerce Platform

📝 Project description: Build complete e-commerce system with products, shopping cart, orders and payments

⭐ Select priority:
  1. Low
  2. Medium (default)
  3. High
Choose (1-3) [default: 2]: 3

🔧 Select domains (comma-separated or all):
  backend   - Java, Spring Boot, Hibernate, Maven
  frontend  - React, Next.js, Vite, TypeScript, Axios
  database  - Oracle, PL/SQL, Schema, CRUD
  all       - Include all domains (default)
Choose [default: all]: all

✅ Project configured:
   Name: E-Commerce Platform
   Description: Build complete e-commerce system...
   Priority: HIGH
   Domains: backend, frontend, database
```

**Tmux otomatik başlarsa:**
- E-Commerce Platform için tüm task'lar oluşturulur
- 5 pane'de gerçek zamanlı izlersin
- Backend, Frontend, Database kodları paralel olarak üretilir

---

## 🔍 Step 6: Oluşturulan Kodları İncele

### Klasör Yapısı

```bash
# Proje klasörlerini gör
ls -la

# Çıktı:
backend/
frontend/
dbadmin/
subtasks/
tasks/
.agent_logs/
projects.json
```

### Backend Kodları

```bash
# Backend kodlarını gör
ls -la backend/todo_list_app/src/main/java/com/example/todolistapp/

# Entity'leri kontrol et
cat backend/todo_list_app/src/main/java/com/example/todolistapp/entity/User.java

# Controller'ları kontrol et
cat backend/todo_list_app/src/main/java/com/example/todolistapp/controller/UserController.java
```

### Frontend Kodları

```bash
# Frontend kodlarını gör
ls -la frontend/todo_list_app/src/components/

# Component'leri kontrol et
cat frontend/todo_list_app/src/components/Button.tsx

# Pages'i kontrol et
cat frontend/todo_list_app/src/pages/dashboard.tsx
```

### Database Kodları

```bash
# Migrations'ı gör
ls -la dbadmin/todo_list_app/migrations/

# Schema creation script'i
cat dbadmin/todo_list_app/migrations/001_schema_creation.sql

# Tables script'i
cat dbadmin/todo_list_app/migrations/002_create_tables.sql

# Procedures script'i
cat dbadmin/todo_list_app/migrations/003_crud_procedures.sql
```

### Subtask Klasörleri

```bash
# Backend subtask'larını gör
ls -la backend/todo_list_app/subtasks/
# 01_setup_spring_boot/
# 02_create_entities_repositories/
# 03_implement_services_business_logic/
# 04_build_rest_controllers_apis/
# 05_add_security_exception_handling/

# Her subtask'ta ne var
cat backend/todo_list_app/subtasks/02_create_entities_repositories/README.md
ls -la backend/todo_list_app/subtasks/02_create_entities_repositories/entities/
```

---

## 📝 Step 7: Tmux Session'ı Kapatma

### Seçenek 1: Detach Sonra Kill

```bash
# Tmux'ta
Ctrl+B → D          # Session'dan ayrıl

# Terminal'de
tmux kill-session -t agent_team
```

### Seçenek 2: Komut ile Direkt

```bash
python run_with_tmux.py --kill
```

### Seçenek 3: Tmux içinde

```bash
Ctrl+B → :
kill-session
```

---

## ✅ Kontrol Listesi

Baştan sona adımlar:

```
□ 1. projects.json dosyasını oluştur/düzenle
□ 2. Terminal aç
□ 3. python run_with_tmux.py --projects projects.json --attach çalıştır
□ 4. Tmux'ta 5 pane'i gör
□ 5. Ctrl+B → 1,2,3,4,5 ile pane'ler arasında dolaş
□ 6. İşleri gerçek zamanlı izle
□ 7. Ctrl+B → [ ile logları scroll et
□ 8. Ayrı terminal'de tail -f .agent_logs/*.log ile detaylı izle
□ 9. İşlem bittikten sonra Ctrl+B → D ile ayrıl
□ 10. Oluşturulan kodları backend/, frontend/, dbadmin/ içinde incele
```

---

## 🎨 Örnek: TO DO LIST APP Projesi Baştan Sona

```bash
# 1. Terminal'i aç ve proje klasörüne git
cd /path/to/claude_projects

# 2. projects.json'a bak (zaten var)
cat projects.json
# [{"name": "TO DO LIST APP", "description": "...", ...}]

# 3. Tmux ile çalıştır
python run_with_tmux.py --projects projects.json --attach

# 4. Tmux pane'lerinde göreceksin:
# - Orchestrator: "Processing Project: TO DO LIST APP"
# - Task Creator: "Breaking project into domain tasks"
# - Backend: "Creating User, Task, Audit entities"
# - Frontend: "Creating Button, Form, Card components"
# - Database: "Creating schema and tables"

# 5. Pane'ler arasında dolaş
Ctrl+B → 1    # Backend görmek
Ctrl+B → 2    # Frontend görmek
Ctrl+B → 4    # Database görmek

# 6. Tmux'tan ayrıl
Ctrl+B → D

# 7. Oluşturulan kodları incele
ls backend/todo_list_app/
ls frontend/todo_list_app/
ls dbadmin/todo_list_app/

# 8. Taskları gör
ls tasks/
ls subtasks/backend/
ls subtasks/frontend/
ls subtasks/database/
```

---

## 💡 İpuçları

- **Hızlı Switch**: `Ctrl+B → o` = Sonraki pane'e git
- **Last Active**: `Ctrl+B → ;` = Son aktif pane'ye dön
- **Zoom**: `Ctrl+B → z` = Pane'i büyütüp küçült
- **List Panes**: `tmux list-panes -t agent_team`
- **Detach & Reattach**: İşlemler durmuyor, rahat şekilde ayrılıp tekrar bağlanabilirsin

---

**Başarılar! Tmux ile agent işlerini kolaylıkla izleyebilirsin! 🚀**
