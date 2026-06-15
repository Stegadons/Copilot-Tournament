| :warning: WARNING                                  |
| -------------------------------------------------- |
| :robot: AI generated content, use at your own risk |

> [!NOTE]  
> Application was initially made to test multi-agent software development "company".  
> Also, because I couldn't find any lightweight system (or fully featured one, that meets my requirements) to make tournament at party more fun. 
> 
> :warning: System is preconfigured with 2 admin users - `admin1:admin123` and `admin2:supersecret`

---

# Tournament Bracket Web Application

## Projekta apraksts
Šis projekts ir tīmekļa lietojumprogramma turnīru organizēšanai un pārvaldībai, balstīta uz *single elimination* principu ar automātisku spēli par 3. vietu. Sistēma paredzēta gan publiskai skatīšanai, gan administratīvai pārvaldībai.

Projekts izstrādāts kā mācību / neliela mēroga produkcijas risinājums, izmantojot vienkāršu, uzturamu arhitektūru bez relāciju datubāzes.

## Galvenās iespējas
- Publiska turnīra skatīšana (bracketi, rezultātu tabula)
- Administratora autentifikācija
- Spēlētāju pievienošana un rediģēšana
- Automātiska bracket ģenerēšana ar BYE atbalstu
- Manuāla bracket korekcija pirms turnīra sākuma
- Rezultātu ievade (ar punktiem vai manuālu uzvarētāja izvēli)
- Automātiska nākamo raundu ģenerēšana
- Spēle par 3. vietu
- Turnīra daļēja vai pilna atiestatīšana

## Palaišanas iespējas

### Python (lokāli)
```
python app.py
```
Piekļuve: http://localhost:5000

### Docker (build+run)

```bash
docker build -t copilot-tournament .
docker run -p 5000:5000 copilot-tournament
```
Piekļuve: http://localhost:5000

### Docker compose (ar datu persistēšanu)

```bash
docker compose up -d --build
```
Piekļuve: http://localhost:5000

`.data/` direktorija tiek izmantota kā Docker volume, lai saglabātu turnīra datus


## Pieslēgšanās
- Skatītājs: publiski
- Administrators: /admin/login

Sīkāk skatīt [INSTALL.md](docs/INSTALL.md) un [USER_GUIDE.md](docs/USER_GUIDE.md)

## Tehnoloģijas
- **Backend:** Python 3, Flask
- **Frontend:** HTML5, Bootstrap
- **Datu glabāšana:** JSON faili
- **Autentifikācija:** Flask sessions + konfigurācijas fails
- **CLI tool lietotāju pārvaldībai:** Python (Flask)

## Dokumentācija
Projektā ir pieejami sekojoši dokumenti:
- **PPS.md** – Programmatūras prasību specifikācija
- **PPA.md** – Programmatūras projektējuma apraksts
- **README.md** – Šis fails
- **INSTALL.md** – Uzstādīšanas instrukcija
- **USER_GUIDE.md** – Lietotāja instrukcija
- **ADMIN_GUIDE.md** – Administrēšanas instrukcija

## Mērķauditorija
- Studenti un pasniedzēji
- Nelielu turnīru organizatori
- Programmatūras izstrādes mācību projekti

## Licencēšana
Projekts paredzēts izglītības un demonstrācijas nolūkiem, ja vien nav norādīts citādi.
