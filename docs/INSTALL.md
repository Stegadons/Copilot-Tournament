
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

Failā `config.json` ir jānorāda:
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

⚠️ Paroles nekad nedrīkst glabāt atklātā tekstā.

### 4.2. Paroles hash ģenerēšana

Paroles hash jāģenerē pirms ievietošanas `config.json`.

**Izmantojot Python (Flask utilītu)**
```
from werkzeug.security import generate_password_hash
print(generate_password_hash("mana_parole"))
```

**CLI komanda**
```
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('mana_parole'))"
```

## 2.5. Datu faila inicializācija

Pārliecinieties, ka eksistē fails:
```
data/tournament.json
```

Ja fails neeksistē, izveidojiet to ar sākotnējo saturu:
```
{
  "name": "",
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
http://127.0.0.1:5000
```

---

# 3. Uzstādīšana ar Docker Compose

## 3.1. docker-compose.yml piemērs
```
version: '3.9'
services:
  app:
    image: tournament-app:latest
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
```

## 3.2. Datu persistences princips

Docker vidē ir jānodrošina **persistēti gan turnīra dati, gan konfigurācija**.

### Ieteicamā volume konfigurācija

```
volumes:
  - ./data:/app/data
  - ./config.json:/app/config.json
```
### Paskaidrojums
- `./data/` – saglabā turnīra stāvokli (`tournament.json`)
- `./config.json` – saglabā admin kontus, paroles hash un `secret_key`
- Abi faili saglabājas starp konteineru restarta reizēm

⚠️ `config.json` nedrīkst iekļaut Docker image iekšpusē kā statisku failu produkcijā.

## 3.3. Palaišana
```
docker compose up -d
```

---

# 4. Docker image build (CI plūsmai)

## 4.1. Dockerfile piemērs
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 4.2. Image build
```
docker build -t tournament-app:latest .
```

## 4.3. CI izmantošana
- Image var būvēt CI (GitHub Actions, GitLab CI)
- Pēc build iespējams publicēt Docker Registry

---

# 8. Piekļuve sistēmai

- **Skatītājs:** pieejams bez autentifikācijas
- **Administrators:**
  - Atveriet `/admin/login`
  - Ievadiet lietotājvārdu un paroli no `config.json`

---

# 9. Biežāk sastopamās problēmas

## Aplikācija nepalaižas
- Pārbaudiet Python versiju
- Pārbaudiet, vai ir aktivizēta virtuālā vide
- Pārbaudiet, vai visas atkarības ir uzinstalētas

## Login nedarbojas
- Pārbaudiet paroles hash `config.json`
- Pārliecinieties, ka `secret_key` ir definēts

---

# 10. Piezīmes

- Sistēma paredzēta **vienam aktīvam turnīram**
- Datu glabāšana JSON failos nav paredzēta augstai vienlaicīgai slodzei
- Produkcijas vidē ieteicams izmantot WSGI serveri (piem., gunicorn)
