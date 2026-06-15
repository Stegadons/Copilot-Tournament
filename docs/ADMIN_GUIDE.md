
# ADMIN_GUIDE.md — Administrēšanas instrukcija

## 1. Ievads

Šī administrēšanas instrukcija ir paredzēta sistēmas **administratoriem** un **uzturētājiem**. Dokuments apraksta konfigurācijas, drošības, uzturēšanas un tipisko administratīvo darbību veikšanu turnīra pārvaldības tīmekļa sistēmā.

Dokuments papildina **USER_GUIDE.md** un **INSTALL.md**, koncentrējoties uz administrēšanas aspektiem.

---

## 2. Administratora loma un atbildības

Administrators ir atbildīgs par:
- sistēmas pieejamību un pareizu darbību;
- turnīra konfigurēšanu un uzturēšanu;
- lietotāju (admin) piekļuves kontroli;
- datu integritāti (JSON faili);
- turnīra atiestatīšanu un kļūdu gadījumu apstrādi.

---

## 3. Administratora piekļuve sistēmai

### 3.1. Pieslēgšanās

Administratora sadaļa ir pieejama adresē: `/admin/login`

Pēc veiksmīgas autentifikācijas tiek izveidota droša sesija, kas ļauj piekļūt visām administrēšanas funkcijām.

### 3.2. Izrakstīšanās

Izrakstīšanās notiek caur **Logout** izvēlni, kas:
- izdzēš sesijas datus;
- atgriež lietotāju publiskajā skatītāja sadaļā.

---

## 4. Konfigurācijas pārvaldība

### 4.1. config.json fails

Fails `config.json` ir galvenais sistēmas konfigurācijas avots.

Galvenie lauki:
- `tournament_name` – turnīra nosaukums;
- `secret_key` – Flask sesiju drošībai;
- `data_file` – ceļš uz turnīra datu failu;
- `admins` – administratoru kontu saraksts.

Piemērs:
```
{
  "tournament_name": "Mans turnīrs",
  "secret_key": "drošs_un_garš_noslēpums",
  "data_file": "data/tournament.json",
  "admins": [
    {
      "username": "admin",
      "password_hash": "pbkdf2:sha256:..."
    }
  ]
}
```

⚠️ Jebkuras izmaiņas `config.json` failā prasa aplikācijas restartēšanu.

### 4.2. Administratoru pārvaldība (CLI rīks)

Administratoru lietotāju pārvaldībai jāizmanto CLI rīks `tools\make-user.py`

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

CLI rīks:
- izveido lietotāju
- automātiski ģenerē paroles hash  
- modificē `config.json` ar vajadzīgajām vērtībām

Pēc config izmaiņām ir nepieciešams restart.

---

## 5. Docker vide

Sistēma pilnībā atbalsta Docker.

### Palaišana

```
docker compose up --build
```

### Uzvedība

- `config.json` tiek izveidots automātiski, ja neeksistē
- `data/` direktorija tiek izmantota datu glabāšanai
- dati tiek saglabāti ārpus containera (volume)

### Svarīgi

- config izmaiņām nepieciešams restart
- regulāri veiciet datu backup (`data/tournament.json`)

---

## 6. Turnīra dzīves cikla administrēšana

### 6.1. Turnīra inicializācija

Administratoram jānodrošina:
- korekts `tournament_name`;
- tukšs vai inicializēts `tournament.json` fails;
- spēlētāju pievienošana pirms turnīra sākuma.

### 6.2. Bracket ģenerēšanas kontrole

- Bracket drīkst ģenerēt tikai vienu reizi pirms 1. raunda sākuma.
- Pēc ģenerēšanas struktūra kļūst nemaināma.

### 6.3. Turnīra atiestatīšana

Pieejami divi režīmi:
- **Reset progress** – saglabā spēlētājus, dzēš raundus un rezultātus;
- **Reset all** – dzēš visu turnīra informāciju.

⚠️ Abas darbības ir neatgriezeniskas.

---

## 7. Datu pārvaldība un rezerves kopijas

### 7.1. Datu glabāšana

Visi turnīra dati tiek glabāti failā:
```
data/tournament.json
```

### 7.2. Rezerves kopijas (Backup)

Ieteicamā prakse:
- regulāri kopēt `tournament.json` failu;
- pirms turnīra reset izveidot rezerves kopiju;
- saglabāt kopijas ārpus projekta mapes.

---

## 8. Drošības apsvērumi

- Neizpaudiet `secret_key` trešajām personām;
- Neuzglabājiet paroles atklātā tekstā;
- Neizmantojiet sistēmu publiskā tīklā bez papildu aizsardzības;
- Produkcijas vidē izmantojiet HTTPS un WSGI serveri.

---

## 9. Biežāk sastopamās administratīvās problēmas

### Turnīrs neparādās skatītājiem
- Pārbaudiet turnīra statusu (`not_started / in_progress / finished`).

### Administrators nevar pieslēgties
- Pārbaudiet paroles hash `config.json`;
- Pārbaudiet, vai `secret_key` ir definēts;
- Restartējiet aplikāciju.

### Dati ir bojāti
- Atjaunojiet `tournament.json` no rezerves kopijas;
- Pārbaudiet JSON sintaksi.

---

## 10. Noslēgums

Šī administrēšanas instrukcija nodrošina visu nepieciešamo informāciju sistēmas drošai un korektai uzturēšanai. Kopā ar INSTALL.md un USER_GUIDE.md tā veido pilnīgu sistēmas ekspluatācijas dokumentāciju.
