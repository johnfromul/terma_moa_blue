# Terma MOA Blue Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integrace topných tyčí Terma MOA Blue do Home Assistant přes Bluetooth Low Energy.

## Funkce

- ✅ Automatická detekce Bluetooth zařízení
- ✅ Dvě climate entity (ovládání pokojové a topné teploty)
- ✅ Teplotní senzory (aktuální a cílové teploty)
- ✅ Senzor provozního režimu
- ✅ Podpora českého a anglického jazyka
- ✅ Plná integrace s Home Assistant včetně automatizací

## Požadavky

- Home Assistant 2023.9 nebo novější
- Bluetooth adaptér (integrovaný nebo USB)
- Topná tyč Terma MOA Blue

## Instalace přes HACS

### Přidání vlastního repozitáře

1. Otevřete HACS v Home Assistant
2. Klikněte na tři tečky v pravém horním rohu
3. Vyberte "Custom repositories"
4. Přidejte URL tohoto repozitáře: `https://github.com/johnfromul/terma_moa_blue`
5. Vyberte kategorii "Integration"
6. Klikněte na "Add"

### Instalace integrace

1. V HACS vyhledejte "Terma MOA Blue"
2. Klikněte na "Download"
3. Restartujte Home Assistant

## Konfigurace

### Párování topné tyče

Před prvním připojením musíte topnou tyč přepnout do párovacího režimu:

1. Stiskněte a přidržte tlačítko na topné tyči po dobu cca 5 sekund
2. Modrá LED začne blikat - zařízení je v párovacím režimu
3. Párovací režim trvá 30 sekund

Výchozí párovací kód je: **123456**

### Přidání do Home Assistant

1. Přejděte do **Nastavení** → **Zařízení a služby**
2. Klikněte na **+ Přidat integraci**
3. Vyhledejte **Terma MOA Blue**
4. Vyberte vaši topnou tyč ze seznamu nalezených zařízení
5. Dokončete konfiguraci

Pokud není zařízení automaticky nalezeno, ujistěte se, že:
- Topná tyč je zapnutá a v dosahu Bluetooth
- Zařízení je v párovacím režimu
- Bluetooth adaptér je funkční

## Entity

Po instalaci budou vytvořeny následující entity:

### Climate (Termostaty)

- **Pokojová teplota** - ovládání podle teploty místnosti (15-30°C)
- **Teplota topné tyče** - ovládání podle teploty radiátoru (30-60°C)

### Senzory

- **Aktuální pokojová teplota** - současná teplota v místnosti
- **Cílová pokojová teplota** - nastavená cílová teplota místnosti
- **Aktuální teplota topné tyče** - současná teplota radiátoru
- **Cílová teplota topné tyče** - nastavená cílová teplota radiátoru
- **Provozní režim** - aktuální režim topné tyče

### Provozní režimy

- `OFF` - Vypnuto
- `ROOM_TEMP_MANUAL` - Manuální řízení podle teploty místnosti
- `ELEMENT_TEMP_MANUAL` - Manuální řízení podle teploty radiátoru
- `ROOM_TEMP_SCHEDULE` - Podle rozvrhu (teplota místnosti)
- `ELEMENT_TEMP_SCHEDULE` - Podle rozvrhu (teplota radiátoru)

## Příklady automatizací

### Zapnutí topení ráno

```yaml
automation:
  - alias: "Topení koupelna - ranní zapnutí"
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

### Vypnutí topení v noci

```yaml
automation:
  - alias: "Topení koupelna - noční vypnutí"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: climate.turn_off
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
```

### Boost režim na 2 hodiny

```yaml
automation:
  - alias: "Topení koupelna - boost režim"
    trigger:
      - platform: state
        entity_id: input_boolean.bathroom_boost
        to: "on"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 26
          hvac_mode: heat
      - delay:
          hours: 2
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 21
```

## Řešení problémů

### Zařízení se nepřipojí

1. Ujistěte se, že topná tyč je v párovacím režimu (modrá LED bliká)
2. Zkontrolujte, že není topná tyč spárovaná s mobilní aplikací Terma
3. Restartujte Home Assistant
4. Zkuste odpárovat a spárovat znovu

### Chyba "Error reading characteristic"

To obvykle znamená chybu autentizace:
1. Přepněte topnou tyč do párovacího režimu
2. Odstraňte integraci v Home Assistant
3. Přidejte ji znovu

### Časté odpojování

- Zkontrolujte dosah Bluetooth signálu
- Přesuňte Bluetooth adaptér blíže k topné tyči
- Minimalizujte interference na frekvenci 2.4 GHz

### Nefunkční čtení teploty

Pokud se nezobrazují aktuální teploty:
1. Počkejte 30 sekund na první aktualizaci
2. Zkontrolujte logy Home Assistant
3. Restartujte integraci

## Technické detaily

### BLE Charakteristiky

| UUID | Popis |
|------|-------|
| `d97352b0-d19e-11e2-9e96-0800200c9a66` | Service UUID |
| `d97352b1-d19e-11e2-9e96-0800200c9a66` | Pokojová teplota (aktuální + cílová) |
| `d97352b2-d19e-11e2-9e96-0800200c9a66` | Teplota topné tyče (aktuální + cílová) |
| `d97352b3-d19e-11e2-9e96-0800200c9a66` | Provozní režim |

### Kódování teplot

Teploty jsou kódovány jako 4 bajty:
- Bajty 0-1: Aktuální teplota × 10
- Bajty 2-3: Cílová teplota × 10

Příklad: 21.5°C = 215 = 0x00 0xD7

## Příspěvky

Příspěvky jsou vítány! Pokud najdete chybu nebo máte nápad na vylepšení:

1. Vytvořte issue
2. Pošlete pull request

## Poděkování

Tato integrace je založena na:
- [terma-moa-blue-esphome](https://github.com/Andrew-a-g/terma-moa-blue-esphome) od Andrew-a-g
- [homebridge-TERMA-MOA-Blue](https://github.com/J1mbo/homebridge-TERMA-MOA-Blue) od J1mbo
- [ha-hudsonread-heater-control](https://github.com/mecorre1/ha-hudsonread-heater-control) od mecorre1
- [Home Assistant Community](https://community.home-assistant.io/t/terma-blue-line-bluetooth-radiators-and-heating-elements/81325) za reverse engineering protokolu

## Licence

MIT License

## Upozornění

Toto je neoficiální integrace a není schválena ani podporována společností Terma. Používání na vlastní riziko. Vždy dodržujte bezpečnostní pokyny při práci s elektrickými topnými zařízeními.

**DŮLEŽITÉ:** Radiátory musí být naplněny správným množstvím kapaliny. Nikdy nezapínejte topnou tyč naprázdno!
