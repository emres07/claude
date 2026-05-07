# 📚 Proje Örnekleri - Kopyala Yapıştır

Aşağıdaki örnekleri `projects.json` dosyasına yapıştır ve çalıştır.

---

## 1️⃣ TO DO LIST APP (Basit)

**Açıklama:** Basit bir todo uygulaması

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

**Çalıştır:**
```bash
python run_with_tmux.py --projects projects.json --attach
```

---

## 2️⃣ E-COMMERCE PLATFORM (Orta)

**Açıklama:** Tam özellikli e-ticaret platformu

```json
[
  {
    "name": "E-Commerce Platform",
    "description": "Build a complete e-commerce system with product catalog, shopping cart, order management, payment processing, user authentication, and admin dashboard for inventory management.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 3️⃣ SOCIAL MEDIA APP (Karmaşık)

**Açıklama:** Sosyal medya uygulaması

```json
[
  {
    "name": "Social Media Platform",
    "description": "Create a social networking platform with user profiles, posts, comments, likes, follows, messaging, notifications, search functionality, and real-time updates.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 4️⃣ BLOG PLATFORM

**Açıklama:** Blog yayıncılık sistemi

```json
[
  {
    "name": "Blog Platform",
    "description": "Develop a blogging platform with post creation, categories, tags, comments, search, user profiles, social sharing, and analytics dashboard.",
    "priority": "medium",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 5️⃣ PROJECT MANAGEMENT TOOL

**Açıklama:** Proje yönetim aracı

```json
[
  {
    "name": "Project Management Tool",
    "description": "Build a project management system with tasks, subtasks, teams, assignments, deadlines, progress tracking, file sharing, comments, and reporting.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 6️⃣ ONLINE LEARNING PLATFORM

**Açıklama:** Online öğrenme platformu

```json
[
  {
    "name": "Online Learning Platform",
    "description": "Create an educational platform with courses, lessons, video content, quizzes, assignments, student progress tracking, certificates, and instructor dashboard.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 7️⃣ RESTAURANT ORDERING SYSTEM

**Açıklama:** Restoran sipariş sistemi

```json
[
  {
    "name": "Restaurant Ordering System",
    "description": "Develop a restaurant management system with menu management, order placement, order tracking, delivery management, payment processing, customer reviews, and restaurant analytics.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 8️⃣ TRAVEL BOOKING PLATFORM

**Açıklama:** Seyahat rezervasyon sistemi

```json
[
  {
    "name": "Travel Booking Platform",
    "description": "Build a travel booking system with flight searches, hotel reservations, package deals, itinerary planning, payment processing, customer reviews, and travel recommendations.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 9️⃣ FITNESS TRACKING APP

**Açıklama:** Fitness ve spor takip uygulaması

```json
[
  {
    "name": "Fitness Tracking App",
    "description": "Create a fitness tracking application with workout logging, progress tracking, meal planning, calorie counting, exercise recommendations, goal setting, and social challenges.",
    "priority": "medium",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 🔟 INVENTORY MANAGEMENT SYSTEM

**Açıklama:** Envanter yönetim sistemi

```json
[
  {
    "name": "Inventory Management System",
    "description": "Develop an inventory management system with stock tracking, product management, supplier management, order management, warehouse tracking, and reporting analytics.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 🔟 + 1️⃣ MULTIPLE PROJECTS TOGETHER

**Açıklama:** Birden fazla proje aynı anda (Sekvansiyel olarak çalıştırılacak)

```json
[
  {
    "name": "TO DO LIST APP",
    "description": "Simple task management application with add, edit, delete, and mark complete features.",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  },
  {
    "name": "BLOG PLATFORM",
    "description": "Blogging system with posts, categories, comments, and search functionality.",
    "priority": "medium",
    "domains": ["backend", "frontend", "database"]
  },
  {
    "name": "FINANCE TRACKER",
    "description": "Personal finance application with expense tracking, budgeting, and financial reports.",
    "priority": "medium",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 🚀 NASIL KULLANILIR?

### Step 1: Örneği Kopyala
Yukarıdaki örneklerden birini seç ve kopyala.

### Step 2: projects.json'a Yapıştır

```bash
# Dosyayı aç
nano projects.json
# ya da Windows'ta:
notepad projects.json
```

Eski içeriği sil ve yeni örneği yapıştır.

### Step 3: Kaydet ve Çıkış

```bash
# nano'da:
Ctrl+O   # Kaydet
Enter
Ctrl+X   # Çık

# Notepad'de:
Ctrl+S   # Kaydet
```

### Step 4: Çalıştır

```bash
python run_with_tmux.py --projects projects.json --attach
```

---

## 💡 İpuçları

### Backend Sadece
Sadece backend kodlarını oluşturmak isterseniz:
```json
"domains": ["backend"]
```

### Frontend Sadece
Sadece frontend kodlarını oluşturmak isterseniz:
```json
"domains": ["frontend"]
```

### Database Sadece
Sadece database kodlarını oluşturmak isterseniz:
```json
"domains": ["database"]
```

### Tüm Projeler
Tüm domain'leri oluşturmak isterseniz (varsayılan):
```json
"domains": ["backend", "frontend", "database"]
```

---

## 📊 Prioriteler

```
"priority": "low"       # Düşük öncelik
"priority": "medium"    # Orta öncelik (varsayılan)
"priority": "high"      # Yüksek öncelik
```

---

## 🎯 ÖRNEK WORKFLOW

```bash
# 1. E-Commerce example'i seç
# projects.json'a yapıştır

# 2. Çalıştır
python run_with_tmux.py --projects projects.json --attach

# 3. Tmux'ta göreceksin:
# - Backend: Products, Orders, Payments için entities, services, controllers
# - Frontend: Product list, shopping cart, checkout pages ve components
# - Database: Products, Orders, Payments, Users tables ve procedures

# 4. İşlem bittiğinde:
Ctrl+B → D   # Ayrıl

# 5. Oluşturulan kodu incele:
ls backend/e_commerce_platform/
ls frontend/e_commerce_platform/
ls dbadmin/e_commerce_platform/
```

---

## ⚡ Hızlı Test

Minimal bir proje test etmek isterseniz:

```json
[
  {
    "name": "Test App",
    "description": "Quick test project for agent team",
    "priority": "low",
    "domains": ["backend", "frontend", "database"]
  }
]
```

---

## 🤔 Sorun mu Yaşıyorsun?

### Error: "projects.json not found"
Dosyanın aynı klasörde olduğundan emin ol:
```bash
ls -la projects.json
```

### Error: "Invalid JSON"
Dosyayı bir JSON validator ile kontrol et:
- Online: https://jsonlint.com/
- VS Code: Ctrl+K Ctrl+F

### Tmux görünmüyor
Tmux yüklü mü kontrol et:
```bash
which tmux
# Yoksa yükle:
sudo apt-get install tmux  # Linux
brew install tmux          # macOS
```

---

**Seçtiğin örneği çalıştırıp tmux'ta izle! 🚀**
