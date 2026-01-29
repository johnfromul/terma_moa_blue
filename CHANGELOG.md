# Changelog

Všechny významné změny v tomto projektu budou zdokumentovány v tomto souboru.

Formát je založený na [Keep a Changelog](https://keepachangelog.com/cs/1.0.0/),
a tento projekt dodržuje [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-23

### Přidáno
- První stabilní verze integrace Terma MOA Blue
- Podpora Bluetooth Low Energy komunikace s topnými tyčemi
- Dvě climate entity:
  - Ovládání podle pokojové teploty (15-30°C)
  - Ovládání podle teploty radiátoru (30-60°C)
- Pět senzorových entit:
  - Aktuální pokojová teplota
  - Cílová pokojová teplota
  - Aktuální teplota topné tyče
  - Cílová teplota topné tyče
  - Provozní režim
- Automatická detekce Bluetooth zařízení
- GUI konfigurace přes config flow
- Podpora párovacího režimu s kódem 123456
- Podpora všech provozních režimů:
  - OFF (vypnuto)
  - ROOM_TEMP_MANUAL (manuální řízení pokojové teploty)
  - ELEMENT_TEMP_MANUAL (manuální řízení teploty radiátoru)
  - ROOM_TEMP_SCHEDULE (pokojová teplota podle rozvrhu)
  - ELEMENT_TEMP_SCHEDULE (teplota radiátoru podle rozvrhu)
- Kompletní česká a anglická lokalizace
- Detailní dokumentace:
  - README s přehledem a příklady
  - INSTALL.md s podrobnými instalačními instrukcemi
  - EXAMPLES.md s příklady Lovelace karet a automatizací
  - Komentáře v kódu
- Příklady automatizací pro běžné scénáře
- Příklady Lovelace karet
- Podpora HACS instalace
- MIT licence

### Bezpečnost
- Ověření připojení před každou operací
- Automatické znovupřipojení při ztrátě spojení
- Validace teplotních limitů
- Bezpečnostní upozornění v dokumentaci
- Ochrana proti běhu naprázdno (upozornění v dokumentaci)

### Technické detaily
- Použití bleak>=0.21.0 pro BLE komunikaci
- Použití bleak-retry-connector>=3.1.0 pro spolehlivé připojení
- Implementace DataUpdateCoordinator pro efektivní správu dat
- Interval aktualizace: 30 sekund (konfigurovatelné)
- Podpora pro Home Assistant 2023.9.0+

### Inspirováno
- [terma-moa-blue-esphome](https://github.com/Andrew-a-g/terma-moa-blue-esphome) od Andrew-a-g
- [homebridge-TERMA-MOA-Blue](https://github.com/J1mbo/homebridge-TERMA-MOA-Blue) od J1mbo
- [ha-hudsonread-heater-control](https://github.com/mecorre1/ha-hudsonread-heater-control) od mecorre1
- [Home Assistant Community](https://community.home-assistant.io/t/terma-blue-line-bluetooth-radiators-and-heating-elements/81325)

## [Unreleased]

### Plánované funkce
- Podpora více topných tyčí najednou
- Podpora časových rozvrhů
- Podpora boost režimu s časovačem
- Statistiky spotřeby
- Automatické eco režimy
- Detekce otevřeného okna
- Integrace s teplotními senzory třetích stran
- Push notifikace při změně stavu

---

Formát data: YYYY-MM-DD
