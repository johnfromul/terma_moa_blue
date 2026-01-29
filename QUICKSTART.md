# Rychlý start - Terma MOA Blue

## 5 kroků k funkční integraci

### 1️⃣ Instalace přes HACS (2 minuty)

1. Otevřete HACS v Home Assistant
2. Tři tečky → Custom repositories
3. Vložte: `https://github.com/honza/terma_moa_blue`
4. Kategorie: Integration → Add
5. Vyhledejte "Terma MOA Blue" → Download
6. Restartujte Home Assistant

### 2️⃣ Příprava topné tyče (30 sekund)

1. Ujistěte se, že je topná tyč zapnutá
2. **Stiskněte a přidržte tlačítko 5 sekund**
3. Počkejte, až začne **blikat modrá LED**
4. Máte 30 sekund na dokončení párování!

### 3️⃣ Přidání do Home Assistant (1 minuta)

1. **Nastavení** → **Zařízení a služby**
2. **+ Přidat integraci**
3. Vyhledejte: **Terma MOA Blue**
4. Vyberte zařízení ze seznamu
5. Hotovo! ✅

### 4️⃣ Ověření funkčnosti (30 sekund)

Zkontrolujte entity v Developer Tools → States:
- ✅ `climate.terma_moa_blue_pokojova_teplota`
- ✅ `climate.terma_moa_blue_teplota_topne_tyce`
- ✅ `sensor.terma_moa_blue_current_room_temperature`
- ✅ `sensor.terma_moa_blue_operating_mode`

### 5️⃣ První test (30 sekund)

Developer Tools → Services:
```yaml
service: climate.set_temperature
target:
  entity_id: climate.terma_moa_blue_pokojova_teplota
data:
  temperature: 22
  hvac_mode: heat
```

Klikněte **Call Service** - topná tyč by měla začít topení! 🔥

## Základní Lovelace karta (copy & paste)

```yaml
type: thermostat
entity: climate.terma_moa_blue_pokojova_teplota
```

## První automatizace

Ranní zapnutí v 6:00:

```yaml
automation:
  - alias: "Topení koupelna - ráno"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 24
          hvac_mode: heat
```

## Řešení problémů - rychlé tipy

### ❌ "No devices found"
→ Topná tyč není v párovacím režimu - přidržte tlačítko 5s

### ❌ "Unable to connect"
→ Odpojte mobilní aplikaci Terma, resetujte topnou tyč

### ❌ Integrace se nezobrazuje
→ Vymažte cache prohlížeče (Ctrl+F5), restartujte HA

### ❌ "Already configured"  
→ Odstraňte starou integraci v Zařízení a služby

## Další kroky

📚 **Detailní dokumentace:** [README.md](README.md)  
🛠️ **Instalační instrukce:** [INSTALL.md](INSTALL.md)  
💡 **Příklady použití:** [EXAMPLES.md](EXAMPLES.md)  

## Potřebujete pomoc?

🐛 [Nahlásit problém](https://github.com/honza/terma_moa_blue/issues)  
💬 [Diskuze na fóru](https://community.home-assistant.io/)

---

**Celkový čas instalace: ~5 minut** ⏱️
