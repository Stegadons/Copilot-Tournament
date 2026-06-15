
# INSTALL.md — Uzstādīšanas instrukcija

# 1. Priekšnosacījumi

Pirms sistēmas uzstādīšanas pārliecinieties, ka Jūsu vidē ir pieejams:
- Operētājsistēma: Windows, Linux vai macOS
- Python **3.9 vai jaunāks**
- Flask 2.3 vai jaunāks
- pip (Python pakotņu pārvaldnieks)
- Tīmekļa pārlūks (Chrome, Firefox, Edge vai Safari)

Python versiju var pārbaudīt ar komandu:
```
python --version
```

---

# 2. Uzstādīšana lokāli

## 2.1. Projekta iegūšana

Lejupielādējiet vai nokopējiet projekta mapes struktūru uz savu datoru, piemēram:

```
tournament_app/
```

Ja projekts tiek izmantots no ZIP arhīva, izsaiņojiet to vēlamajā direktorijā.

## 2.2. Virtuālās vides izveide (ieteicams)

Lai izolētu projekta atkarības, ieteicams izmantot Python virtuālo vidi.

### Linux / macOS
```
python -m venv venv
source venv/bin/activate
```

### Windows
```
python -m venv venv
venv\Scripts\Activate.ps1
```

## 2.3. Atkarību instalēšana

Projekta saknes direktorijā izpildiet:
```
pip install -r requirements.txt
```

Ja `requirements.txt` nav pieejams, nepieciešamā minimālā atkarība ir:
```
flask>=2.3
```

## 2.4. Konfigurācija

### config.json

Failā `config.json` norāda:
- turnīra nosaukums
- Flask `secret_key`
- administratora lietotājvārds un paroles hash
- datu faila ceļš

Piemērs:
```
{
  "tournament_name": "Mans turnīrs",
  "secret_key": "random_secret_key",
  "data_file": "data/tournament.json",
  "admins": [
    {
      "username": "admin",
      "password_hash": "pbkdf2:sha256:..."
    }
  ]
}
```

Ja konfigurācijas fails neeksistē, tas tiek izveidots automātiski, ar noklusēto saturu:
```
{
  "secret_key": "change-me",
  "data_file": "data/tournament.json",
  "admins": [],
  "tournament_name": "Turnīrs"
}
```

### 4.2. Paroles hash ģenerēšana

Paroles hash ģenerēšanai tiek imantota Python Flask utilīta:

```
from werkzeug.security import generate_password_hash
print(generate_password_hash("mana_parole"))
```

#### CLI rīks `tools/make-user.py`

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

CLI rīks:
- izveido/dzēš lietotāju
- automātiski ģenerē paroles hash  
- modificē `config.json` ar norādītajām vērtībām

Pēc config izmaiņām ir nepieciešams restart.

## 2.5. Datu faila inicializācija

Pārliecinieties, ka eksistē fails:
```
data/tournament.json
```

Ja fails neeksistē, tas tiek izveidots automātiski ar sākotnējo saturu:
```
{
  "status": "not_started",
  "players": [],
  "rounds": []
}
```

## 2.6. Aplikācijas palaišana

No projekta saknes direktorijas palaidiet:
```
python app.py
```

Ja viss ir konfigurēts korekti, konsolē redzēsiet Flask starta paziņojumu.

Pēc tam atveriet pārlūkā:
```
http://localhost:5000
```

---

# 3. Uzstādīšana ar Docker Compose

## 3.1. docker-compose.yml piemērs
```
services:
  web:
    build: .
    container_name: copilot-tournament
    environment:
      - FLASK_ENV=production
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## 3.2. Datu persistences princips

- `config.json` tiek izveidots automātiski, ja neeksistē (netiek persistēts)
- `data/` direktorija tiek izmantota datu glabāšanai
- dati tiek saglabāti ārpus containera (volume)

### Ieteicamā volume konfigurācija

```
volumes:
  - ./data:/app/data
```
### Paskaidrojums
- `./data/` – saglabā turnīra stāvokli (`tournament.json`)
- folderī esošie faili saglabājas starp konteineru restarta reizēm

⚠️ `config.json` nav iekļauts Docker image iekšpusē kā statisks fails produkcijā.

## 3.3. Palaišana

Klonē GitHub repozitoriju
```
git clone https://github.com/Stegadons/Copilot-Tournament.git .
```

Palaiž aplikāciju
```
docker compose up --build
```

Konfigurē SECRET_KEY, izveido lietotāju
```
docker exec -it copilot-tournament python tools/make-user.py set-secret <tavs secret>
docker exec -it copilot-tournament python tools/make-user.py add admin
```

---

# 4. Docker image build (CI plūsmai)

## 4.1. Dockerfile piemērs
```
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
```

## 4.2. Image build
```
docker build -t copilot-tournament:latest .
```

## 4.3. CI izmantošana
- Image var būvēt CI (GitHub Actions, GitLab CI)
- Pēc build iespējams publicēt Docker Registry

---

# 5. Piekļuve sistēmai

- **Skatītājs:** pieejams bez autentifikācijas
- **Administrators:**
  - Atveriet `/admin/login`
  - Ievadiet lietotājvārdu un paroli no `config.json`

---

# 6. Biežāk sastopamās problēmas

## Aplikācija nepalaižas
- Pārbaudiet Python versiju
- Pārbaudiet, vai ir aktivizēta virtuālā vide
- Pārbaudiet, vai visas atkarības ir uzinstalētas

## Login nedarbojas
- Pārbaudiet paroles hash `config.json`
- Pārliecinieties, ka `secret_key` ir definēts

---

# 7. Piezīmes

- Sistēma paredzēta **vienam aktīvam turnīram**
- Datu glabāšana JSON failos nav paredzēta augstai vienlaicīgai slodzei
- Produkcijas vidē ieteicams izmantot WSGI serveri (piem., gunicorn)
