# v1.0.4 - Opravy podle Frida reverse engineering

## 🐛 Kritické opravy (na základě zachycení mobilní aplikace)

### Opravené režimy topení
- **Přidán režim MANUAL (0x01)** - zjištěno z Frida zachycení aplikace
- **Opraveno zapínání topení** - používá režim MANUAL místo ELEMENT_TEMP_MANUAL
- **Opravený formát režimu** - 4 bajty `[režim, 0x00, 0x00, 0x00]` místo 1 bajtu

### Opravený formát dat
- Little-endian formát už byl správně (v1.0.3)
- Formát teplot: `[current_low, current_high, target_low, target_high]`
- Hodnoty v desítkách stupňů (např. 40°C = 400 = 0x0190)

## 📊 Zjištěné hodnoty z Frida

**Zapnutí topení:**
```
UUID: d97352b3
Data: [0x01, 0x00, 0x00, 0x00]
Režim: MANUAL
```

**Vypnutí topení:**
```
UUID: d97352b3  
Data: [0x00, 0x00, 0x00, 0x00]
Režim: OFF
```

**Nastavení teploty 40°C:**
```
UUID: d97352b2
Data: [0x00, 0x00, 0x90, 0x01]
Hodnota: 400 (40.0°C × 10) v little-endian
```

**Nastavení teploty 50°C:**
```
UUID: d97352b2
Data: [0x00, 0x00, 0xF4, 0x01]
Hodnota: 500 (50.0°C × 10) v little-endian
```

## 🔧 Technické změny

1. `const.py`:
   - Přidán `OperatingMode.MANUAL = 1`

2. `api.py`:
   - `turn_on()` - používá `OperatingMode.MANUAL`
   - `set_mode()` - zapisuje 4 bajty místo 1
   - Zachován little-endian formát teplot

## 📦 Instalace

1. Odinstalujte starou verzi v HACS
2. Restartujte Home Assistant
3. Nainstalujte v1.0.4 z HACS
4. Restartujte Home Assistant
5. Přidejte integraci

## ⚠️ Důležité

Po aktualizaci je **nutný restart Home Assistant** a případně **nové přidání integrace** (odstranit starou, přidat novou).

---

Díky Frida reverse engineering mobilní aplikace Terma BlueLine Next za odhalení správných komunikačních protokolů! 🎉
