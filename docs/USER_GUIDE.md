
# USER_GUIDE.md — Lietotāja rokasgrāmata

## 1. Ievads

Šī lietotāja rokasgrāmata apraksta turnīra pārvaldības tīmekļa sistēmas lietošanu gan **skatītājiem**, gan **administratoriem**. Dokuments paredzēts galalietotājiem un neprasa tehniskas priekšzināšanas.

## 2. Piekļuve sistēmai

### 2.1. Sistēmas atvēršana

Pēc aplikācijas palaišanas atveriet tīmekļa pārlūkā:

```
http://127.0.0.1:5000
```

Sistēma automātiski atvērs publisko skatītāja sadaļu.

---

## 3. Skatītāja rokasgrāmata (Viewer)

Skatītāja sadaļa ir **publiski pieejama** un neprasa autentifikāciju.

### 3.1. Turnīra statuss

- Ja turnīrs **nav sācies**, tiek parādīts informatīvs paziņojums:
  > “Pašreiz nav aktīva turnīra.”
- Ja turnīrs ir aktīvs vai pabeigts, tiek attēlots tā nosaukums un saturs.

### 3.2. Bracket apskate

Sadaļā **Bracketi** skatītājs var:
- redzēt visus raundus (1. raunds, pusfināli, fināls, 3. vietas spēle),
- redzēt spēlētāju pārus,
- identificēt automātiskās uzvaras (BYE).

Bracketi tiek **automātiski atjaunināti** pēc katras rezultātu ievades.

### 3.3. Rezultātu tabula

Sadaļā **Rezultāti** tiek attēlota turnīra rezultātu tabula:
- 1. vieta – fināla uzvarētājs
- 2. vieta – fināla zaudētājs
- 3. vieta – spēles par 3. vietu uzvarētājs
- 4. vieta – spēles par 3. vietu zaudētājs

Pārējie spēlētāji tiek kārtoti pēc:
1. uzvaru skaita,
2. punktu starpības,
3. alfabētiskās kārtības.

---

## 4. Administratora rokasgrāmata (Admin)

Administratora sadaļa ir pieejama tikai **autentificētiem lietotājiem**.

### 4.1. Pieslēgšanās

1. Atveriet adresi:
   ```
   /admin/login
   ```
2. Ievadiet lietotājvārdu un paroli (definēti `config.json`).
3. Pēc veiksmīgas pieslēgšanās tiek atvērts **Admin Dashboard**.

### 4.2. Vadības panelis (Dashboard)

Panelī redzams:
- turnīra statuss,
- spēlētāju skaits,
- navigācija uz galvenajām sadaļām.

### 4.3. Spēlētāju pārvaldība

Sadaļā **Spēlētāji** administrators var:
- pievienot jaunu spēlētāju (tikai vārds),
- labot spēlētāja vārdu,
- dzēst spēlētāju.

⚠️ Spēlētājus drīkst labot vai dzēst **tikai līdz 1. raunda sākumam**.

### 4.4. Bracket izveide

Sadaļā **Bracket** administrators var:
- ģenerēt bracket automātiski,
- ļaut sistēmai piešķirt BYE,
- manuāli koriģēt pārus pirms turnīra sākuma.

Pēc pirmā raunda sākuma bracket struktūra vairs nav maināma.

### 4.5. Rezultātu ievade

Sadaļā **Raundi / Rezultāti** administrators var:

**A) Ievadīt punktus**
- ievadīt rezultātus abiem spēlētājiem,
- sistēma automātiski nosaka uzvarētāju.

**B) Manuāli izvēlēties uzvarētāju**
- pieejams tikai, ja punkti nav ievadīti,
- izmanto gadījumos, kad skaitliskais rezultāts nav zināms.

Uzvarētājs automātiski tiek pārcelts uz nākamo raundu.

### 4.6. Turnīra atiestatīšana

Sadaļā **Reset** pieejami divi režīmi:
- **Atstatīt progresu** – dzēš spēles un rezultātus, saglabā spēlētājus;
- **Pilns reset** – dzēš visu turnīra informāciju.

⚠️ Reset darbības ir neatgriezeniskas.

---

## 5. Biežāk uzdotie jautājumi

**Vai skatītājam ir nepieciešams konts?**  
Nē, skatītāja sadaļa ir publiska.

**Vai var vadīt vairākus turnīrus vienlaicīgi?**  
Nē, sistēma paredzēta vienam aktīvam turnīram.

**Vai dati saglabājas pēc aplikācijas restartēšanas?**  
Jā, dati tiek glabāti JSON failos.

---

## 6. Noslēgums

Šī lietotāja rokasgrāmata nodrošina pilnu sistēmas lietošanas aprakstu gan skatītājiem, gan administratoriem. Papildu tehniskā informācija pieejama PPA.md un ADMIN_GUIDE.md dokumentos.
