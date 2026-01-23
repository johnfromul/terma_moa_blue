# Řešení problému "Nic nenašel"

## Příčiny problému

Když Home Assistant hlásí "Nic nenašel" při přidávání integrace, může to být způsobeno několika věcmi:

### 1. Topná tyč není v párovacím režimu ❌

**Řešení:**
1. Stiskni a **přidrž tlačítko na topné tyči 5 sekund**
2. Uvolni, když začne **blikat modrá LED**
3. Máš **30 sekund** na přidání integrace
4. Zkus to znovu v HA: Nastavení → Zařízení a služby → + Přidat integraci → Terma MOA Blue

### 2. Topná tyč je mimo dosah Bluetooth 📡

**Kontrola:**
- Zkus přiblížit HA server k topné tyči
- Maximální dosah je cca 10 metrů bez překážek
- Zdi a kovové předměty snižují dosah

**Test dosahu:**
```bash
# V terminálu Home Assistant
bluetoothctl
scan on
# Počkej 10 sekund a hledej "MOA Blue" v seznamu
```

### 3. Bluetooth není správně nakonfigurován v HA 🔧

**Kontrola v HA:**
1. Nastavení → Zařízení a služby
2. Zkontroluj, jestli je integrace "Bluetooth" aktivní
3. Měla by zobrazovat nalezená zařízení

**Pokud Bluetooth integrace chybí:**
1. Přidej ji: Nastavení → Zařízení a služby → + Přidat integraci → Bluetooth
2. Restartuj Home Assistant

**V terminálu:**
```bash
# Zkontroluj, jestli běží Bluetooth
hciconfig

# Mělo by vypsat něco jako:
# hci0:   Type: Primary  Bus: USB
#         BD Address: XX:XX:XX:XX:XX:XX  ACL MTU: 1021:8  SCO MTU: 64:1
#         UP RUNNING
```

### 4. Topná tyč je spárovaná s mobilem 📱

**Problém:** Pokud je topná tyč aktivně připojená k mobilní aplikaci Terma, může odmítat nová spojení.

**Řešení:**
1. Zavři aplikaci Terma na mobilu
2. V mobilu: Nastavení → Bluetooth → Zapomeň zařízení "MOA Blue Terma"
3. Přepni topnou tyč do párovacího režimu
4. Zkus přidat v HA

### 5. Integrace se nenainstalovala správně 📦

**Kontrola v terminálu HA:**
```bash
ls -la /config/custom_components/terma_moa_blue/

# Mělo by vypsat:
# __init__.py
# api.py
# climate.py
# config_flow.py
# const.py
# coordinator.py
# manifest.json
# sensor.py
# strings.json
# translations/
```

**Pokud soubory chybí:**
1. Odinstaluj integraci v HACS
2. Restartuj HA
3. Nainstaluj znovu
4. Restartuj HA

## Krok za krokem řešení

### Krok 1: Zapni debug logi

Přidej do `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.terma_moa_blue: debug
    homeassistant.components.bluetooth: debug
```

Restartuj HA a sleduj logy:
```bash
tail -f /config/home-assistant.log | grep -i "terma\|bluetooth"
```

### Krok 2: Manuální Bluetooth scan

```bash
# V terminálu HA
bluetoothctl

# V bluetoothctl:
power on
scan on

# Hledej v outputu:
# [NEW] Device XX:XX:XX:XX:XX:XX MOA Blue Terma
```

**Pokud NEVIDÍŠ "MOA Blue Terma":**
- Topná tyč není v párovacím režimu
- Topná tyč je mimo dosah
- Topná tyč je vypnutá

**Pokud VIDÍŠ "MOA Blue Terma":**
- Poznamenej si MAC adresu (XX:XX:XX:XX:XX:XX)
- Pokračuj na Krok 3

### Krok 3: Zkontroluj HA Bluetooth integraci

1. Nastavení → Zařízení a služby → Bluetooth
2. Měl bys vidět náhledy nalezených BLE zařízení
3. Pokud tam je "MOA Blue", HA ho vidí ✅

### Krok 4: Zkontroluj logy po přidání integrace

Po kliknutí na "+ Přidat integraci → Terma MOA Blue" sleduj logy:

```bash
tail -f /config/home-assistant.log | grep terma_moa_blue
```

**Co hledat:**
```
DEBUG Found BLE device: MOA Blue Terma (XX:XX:XX:XX:XX:XX) - RSSI: -XX
INFO Found Terma device: MOA Blue Terma (XX:XX:XX:XX:XX:XX)
INFO Terma devices found: 1
```

**Pokud vidíš "Total BLE devices found: 0":**
- Bluetooth v HA nefunguje správně
- Zkus restartovat Bluetooth službu

**Pokud vidíš "Terma devices found: 0" ale "Total BLE devices found: X":**
- HA vidí BLE zařízení, ale topná tyč není mezi nimi
- Topná tyč není v párovacím režimu
- Topná tyč se nejmenuje "MOA Blue Terma" (zkontroluj přesný název)

### Krok 5: Manuální přidání (fallback)

Pokud nic nefunguje, zkus:

1. **Zjisti MAC adresu topné tyče**
   ```bash
   bluetoothctl
   scan on
   # Počkej a najdi MAC adresu
   ```

2. **Zkontroluj, jestli config_flow umožňuje manuální zadání**
   - V současné verzi to bohužel není
   - Budu muset přidat tuto funkci

## Nejčastější řešení (90% případů)

**Problém:** "Nic nenašel"

**Řešení:**
1. ✅ **Přepni topnou tyč do párovacího režimu** (tlačítko 5s, modrá LED bliká)
2. ✅ **Přibliž se k topné tyči** (max 5 metrů při prvním párování)
3. ✅ **Odpoj mobil** (zavři aplikaci Terma, zapomeň BT zařízení)
4. ✅ **Počkej 10 sekund** po přepnutí do párovacího režimu
5. ✅ **Zkus přidat integraci znovu**

## Co dělat, když nic nepomáhá

1. Pošli mi screenshot z logů: `tail -100 /config/home-assistant.log | grep -i "terma\|bluetooth"`
2. Pošli mi output z: `bluetoothctl scan on` (po 10 sekundách)
3. Pošli mi výpis: `ls -la /config/custom_components/terma_moa_blue/`

## Další vylepšení (připravím v další verzi)

- [ ] Přidat možnost manuálního zadání MAC adresy
- [ ] Přidat tlačítko "Rescan" přímo v config flow
- [ ] Přidat vizuální indikátor síly signálu (RSSI)
- [ ] Přidat timeout warning (pokud trvá skenování dlouho)
- [ ] Přidat fallback pro zařízení, která se nejmenují přesně "MOA Blue Terma"
