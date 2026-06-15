## ADMIN_GUIDE.md — Administrēšanas instrukcija

### 1. Ievads
  
Šī administrēšanas instrukcija ir paredzēta sistēmas **administratoriem** un **uzturētājiem**. Dokuments apraksta konfigurācijas, drošības, uzturēšanas un tipisko administratīvo darbību veikšanu turnīra pārvaldības tīmekļa sistēmā.  
Dokuments papildina **USER_GUIDE.md** un **INSTALL.md**, koncentrējoties uz administrēšanas aspektiem.

---

### 2. Administratora loma un atbildības

Administrators ir atbildīgs par:
- sistēmas pieejamību un pareizu darbību;
- turnīra konfigurēšanu un uzturēšanu;
- lietotāju (admin) piekļuves kontroli;
- datu integritāti (JSON faili);
- turnīra atiestatīšanu un kļūdu gadījumu apstrādi.

---

### 3. Administratora piekļuve sistēmai

#### 3.1. Pieslēgšanās

Administratora sadaļa: `/admin/login`

Pēc veiksmīgas autentifikācijas tiek izveidota sesija.

#### 3.2. Izrakstīšanās

Logout izdzēš sesiju un atgriež uz publisko sadaļu.

---

### 4. Konfigurācijas pārvaldība

#### 4.1. config.json

Fails **config.json** ir galvenais konfigurācijas avots.

Struktūra:

```
{
  "tournament_name": "Turnīrs",
  "secret_key": "secret",
  "data_file": "data/tournament.json",
  "admins": [
    {
      "username": "admin",
      "password_hash": "..."
    }
  ]
}
```

⚠️ Izmaiņas prasa aplikācijas restartu.

---

### 4.2. Administratoru pārvaldība (CLI rīks)

Projektā izmantot CLI rīku:

```
tools/make-user.py
```

#### Komandas:

```
# Parādīt visus administratorus
python tools/make-user.py list

# Pievienot lietotāju
python tools/make-user.py add <username>

# Dzēst lietotāju
python tools/make-user.py delete <username>

# Mainīt paroli
python tools/make-user.py set-password <username>

# Uzstādīt SECRET_KEY
python tools/make-user.py set-secret
```

✅ Automātiski ģenerē paroles hash  
✅ Atliek tikai ievadīt paroli  
✅ Drošs un Docker-friendly

---

### 5. Docker vide

Sistēma pilnībā atbalsta Docker.

#### Palaišana

```
docker compose up --build
```

#### Uzvedība

- `config.json` tiek izveidots automātiski, ja nav
- `data/` direktorija tiek izmantota datu glabāšanai
- dati tiek saglabāti ārpus containera (volume)

#### Svarīgi

- config izmaiņām nepieciešams restart
- regulāri veic datu backup (`data/tournament.json`)

---

### 6. Turnīra administrēšana

#### 6.1. Inicializācija

- iestatīt nosaukumu
- pievienot spēlētājus

#### 6.2. Bracket ģenerēšana

- tikai pirms turnīra sākuma

#### 6.3. Reset

- Reset progress — saglabā spēlētājus
- Reset all — dzēš visu

⚠️ Darbības neatgriezeniskas

---

### 7. Datu pārvaldība

Fails:

```
data/tournament.json
```

#### Backup

- kopēt pirms reset
- glabāt ārpus projekta

---

### 8. Drošība

- neizpaust secret_key
- neglabāt parole plaintext
- izmantot HTTPS produkcijā

---

### 9. Problēmu risināšana

#### Login nedarbojas

- pārbaudīt lietotāju
- pārģenerēt paroli ar CLI

#### Dati bojāti

- atjaunot no backup

---

### 10. Noslēgums

Dokuments nodrošina pilnu sistēmas administrēšanu kopā ar pārējiem dokumentiem.
