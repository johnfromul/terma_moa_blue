# Detailní instalační instrukce

## Příprava

### 1. Kontrola Bluetooth adaptéru

Nejprve se ujistěte, že váš Home Assistant má funkční Bluetooth:

```bash
# V terminálu Home Assistant spusťte:
hcitool dev
```

Měli byste vidět váš Bluetooth adaptér. Pokud ne, musíte nainstalovat nebo povolit Bluetooth.

### 2. Příprava topné tyče

1. Ujistěte se, že topná tyč je zapojena do elektrické sítě
2. Ujistěte se, že radiátor je správně naplněn kapalinou
3. Nikdy nezapínejte topnou tyč naprázdno!

## Instalace přes HACS (doporučeno)

### Krok 1: Instalace HACS

Pokud ještě nemáte HACS nainstalovaný:

1. Navštivte https://hacs.xyz/docs/setup/download
2. Následujte instalační instrukce
3. Restartujte Home Assistant

### Krok 2: Přidání custom repository

1. Otevřete HACS v Home Assistant (`Nastavení` → `HACS`)
2. Klikněte na tři tečky v pravém horním rohu
3. Vyberte `Custom repositories`
4. Vložte URL: `https://github.com/honza/terma_moa_blue`
5. V kategorii vyberte `Integration`
6. Klikněte `Add`

### Krok 3: Instalace integrace

1. V HACS vyhledejte "Terma MOA Blue"
2. Klikněte na kartu integrace
3. Klikněte `Download`
4. Restartujte Home Assistant

## Ruční instalace

### Krok 1: Stažení souborů

```bash
cd /config
mkdir -p custom_components
cd custom_components
git clone https://github.com/honza/terma_moa_blue.git
```

nebo stáhněte ZIP a rozbalte:

```bash
cd /config/custom_components
wget https://github.com/honza/terma_moa_blue/archive/refs/heads/main.zip
unzip main.zip
mv terma_moa_blue-main terma_moa_blue
```

### Krok 2: Kontrola struktury

Ujistěte se, že máte správnou strukturu:

```
custom_components/
└── terma_moa_blue/
    ├── __init__.py
    ├── api.py
    ├── climate.py
    ├── config_flow.py
    ├── const.py
    ├── coordinator.py
    ├── manifest.json
    ├── sensor.py
    ├── strings.json
    └── translations/
        ├── cs.json
        └── en.json
```

### Krok 3: Restart

Restartujte Home Assistant.

## Konfigurace

### Krok 1: Přepnutí do párovacího režimu

Topná tyč musí být v párovacím režimu pro první připojení:

1. **Stiskněte a přidržte** tlačítko na topné tyči po dobu **cca 5 sekund**
2. Uvolněte tlačítko, když začne **blikat modrá LED**
3. Párovací režim je aktivní po dobu **30 sekund**
4. Během tohoto času musíte dokončit párování

**Poznámka:** Pokud je topná tyč spárována s mobilní aplikací Terma, musíte ji nejprve odpárovat.

### Krok 2: Přidání integrace

1. Přejděte do `Nastavení` → `Zařízení a služby`
2. Klikněte na `+ Přidat integraci`
3. Vyhledejte **Terma MOA Blue**

#### Automatická detekce

Pokud je topná tyč v dosahu a v párovacím režimu, měla by být automaticky detekována:

1. Vyberte ji ze seznamu
2. Potvrďte přidání

#### Ruční výběr

Pokud automatická detekce nefunguje:

1. Klikněte na tlačítko pro ruční výběr
2. Vyberte zařízení ze seznamu Bluetooth zařízení
3. MAC adresa je ve formátu: `XX:XX:XX:XX:XX:XX`

### Krok 3: Dokončení konfigurace

Po úspěšném přidání se vytvoří:
- 2× Climate entity (pokojová a radiátorová teplota)
- 5× Sensor entity (teploty a režim)

## Ověření funkčnosti

### Kontrola v Developer Tools

1. Přejděte do `Developer Tools` → `States`
2. Vyhledejte entity začínající na `climate.terma_moa_blue_`
3. Měli byste vidět aktuální stav (teploty, režim)

### Testování ovládání

1. Přejděte do `Developer Tools` → `Services`
2. Vyberte službu `climate.set_temperature`
3. Vyberte entitu `climate.terma_moa_blue_pokojova_teplota`
4. Nastavte teplotu (např. 22°C)
5. Klikněte `Call Service`

Topná tyč by měla začít topení a LED by měly indikovat aktivitu.

## Řešení problémů při instalaci

### Integrace se nezobrazuje v seznamu

**Řešení:**
1. Zkontrolujte, že soubory jsou ve správné složce
2. Restartujte Home Assistant
3. Vymažte cache prohlížeče (Ctrl+F5)

### "No devices found"

**Řešení:**
1. Ujistěte se, že topná tyč je zapnutá
2. Přepněte ji do párovacího režimu
3. Zkontrolujte dosah Bluetooth
4. Zkuste restartovat Bluetooth:
   ```bash
   sudo systemctl restart bluetooth
   ```

### "Already configured"

**Řešení:**
1. Přejděte do `Nastavení` → `Zařízení a služby`
2. Najděte starou instanci Terma MOA Blue
3. Klikněte na tři tečky a vyberte `Odstranit`
4. Restartujte Home Assistant
5. Zkuste znovu

### "Unable to connect"

**Řešení:**
1. Odpojte topnou tyč od mobilní aplikace Terma
2. Resetujte Bluetooth párování na topné tyči (odpojte od sítě, počkejte 10s, zapojte)
3. Přepněte do párovacího režimu
4. Zkuste připojení znovu

### Chyba v logu: "bleak not found"

**Řešení:**
```bash
# V Home Assistant kontejneru nebo venv:
pip install bleak>=0.21.0 bleak-retry-connector>=3.1.0
```

## Pokročilá konfigurace

### Změna intervalu aktualizace

Pokud chcete změnit, jak často se aktualizují data (výchozí je 30s):

1. Upravte soubor `const.py`
2. Změňte řádek: `UPDATE_INTERVAL = 30` na požadovanou hodnotu v sekundách
3. Restartujte Home Assistant

**Poznámka:** Nižší hodnota znamená častější aktualizace, ale také vyšší zatížení Bluetooth.

### Debug logging

Pro detailní logy:

1. Přidejte do `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.terma_moa_blue: debug
   ```
2. Restartujte Home Assistant
3. Logy najdete v `Settings` → `System` → `Logs`

## Bezpečnostní upozornění

⚠️ **DŮLEŽITÉ BEZPEČNOSTNÍ INFORMACE**

1. **Nikdy nezapínejte topnou tyč naprázdno** - radiátor musí být plně naplněn kapalinou
2. **Maximální teplota** - nepřekračujte maximální teplotu 60°C pro topnou tyč
3. **Pravidelná kontrola** - kontrolujte hladinu kapaliny v radiátoru
4. **Elektrická bezpečnost** - instalaci provádějte pouze kvalifikovaný elektrikář
5. **Dohled nad dětmi** - držte děti mimo dosah topného tělesa

## Podpora

Pokud máte problémy:

1. Zkontrolujte logy Home Assistant
2. Vyhledejte podobný problém v Issues na GitHubu
3. Vytvořte nový issue s:
   - Popisem problému
   - Logy z Home Assistant
   - Verzí Home Assistant
   - Model topné tyče

## Další kroky

Po úspěšné instalaci:

1. Vytvořte automatizace (viz README.md)
2. Přidejte do Lovelace dashboard
3. Nastavte scény pro různé části dne
4. Využijte Google Assistant / Alexa integraci
