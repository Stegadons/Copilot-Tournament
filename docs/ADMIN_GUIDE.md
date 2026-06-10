
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

Administratora sadaļa ir pieejama adresē:

```
/admin/login
```

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

### 4.2. Paroles hash ģenerēšana

Paroles hash jāģenerē pirms ievietošanas `config.json`.

#### Izmantojot Python (Flask utilītu)

```
from werkzeug.security import generate_password_hash
print(generate_password_hash("mana_parole"))
```

**Rezultāts**
Iegūto hash ievietojiet config.json laukā `password_hash`.

⚠️ Nekad neglabājiet paroles atklātā tekstā.

#### Paroles hash ģenerēšana ar CLI (ieteicamais variants administratoriem)

Šis variants ir paredzēts administratoriem, DevOps un CI/CD vidēm, kur nav vēlams veidot atsevišķus skriptus vai palaist Flask aplikāciju.

**CLI komanda**
```
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('mana_parole'))"
```

**Pielietojums**
- Rezultātā iegūto hash ievieto `config.json` laukā `password_hash`
- Var izmantot lokāli, serverī vai CI pipeline laikā

**Priekšrocības**
- Nav jāveido papildu faili
- Nav atkarīgs no aplikācijas palaišanas
- Ideāli piemērots Docker / CI vidēm

⚠️ Nekad neglabājiet paroles atklātā tekstā.

---

## 5. Administratoru kontu pārvaldība

### 5.1. Jauna administratora pievienošana

Lai pievienotu jaunu administratoru:
1. Izveidojiet paroles hash (piem., izmantojot Flask utilītas).
2. Pievienojiet jaunu objektu masīvā `admins`.
3. Saglabājiet failu un restartējiet aplikāciju.

### 5.2. Administratora dzēšana

- Dzēsiet attiecīgo ierakstu no `admins` masīva.
- Pārliecinieties, ka sistēmā paliek vismaz viens administrators.

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
