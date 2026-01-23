{% if installed %}
## Změny v této verzi

### Verze 1.0.0

- ✅ První stabilní verze
- ✅ Plná podpora Bluetooth Low Energy komunikace
- ✅ Dvě climate entity (pokojová a radiátorová teplota)
- ✅ Pět senzorů (aktuální a cílové teploty, režim)
- ✅ Automatická detekce zařízení
- ✅ Podpora českého a anglického jazyka
- ✅ Kompletní dokumentace a příklady

{% else %}
## Vítejte v integraci Terma MOA Blue!

Tato integrace umožňuje ovládat topné tyče Terma MOA Blue přímo z Home Assistant přes Bluetooth.

### Funkce

- 🔌 **Snadná instalace** - automatická detekce Bluetooth zařízení
- 🌡️ **Dvě climate entity** - ovládání podle pokojové nebo radiátorové teploty
- 📊 **Senzory** - aktuální a cílové teploty, provozní režim
- 🔄 **Automatizace** - plná podpora Home Assistant automatizací
- 🇨🇿 **Čeština** - kompletní podpora českého jazyka
- 📖 **Dokumentace** - detailní návody a příklady

### Před instalací

Ujistěte se, že:
- Máte funkční Bluetooth adaptér v Home Assistant
- Topná tyč je zapnutá a naplněná kapalinou
- Znáte MAC adresu topné tyče (nebo ji můžete najít automaticky)

### Po instalaci

1. Přejděte do **Nastavení** → **Zařízení a služby**
2. Klikněte **+ Přidat integraci**
3. Vyhledejte **Terma MOA Blue**
4. Přepněte topnou tyč do párovacího režimu (přidržte tlačítko 5s)
5. Vyberte zařízení ze seznamu

### Užitečné odkazy

- 📚 [Kompletní dokumentace](https://github.com/honza/terma_moa_blue/blob/main/README.md)
- 🛠️ [Instalační instrukce](https://github.com/honza/terma_moa_blue/blob/main/INSTALL.md)
- 💡 [Příklady použití](https://github.com/honza/terma_moa_blue/blob/main/EXAMPLES.md)
- 🐛 [Nahlásit problém](https://github.com/honza/terma_moa_blue/issues)

### Upozornění

⚠️ **BEZPEČNOST:** Nikdy nezapínejte topnou tyč naprázdno! Radiátor musí být vždy plně naplněn kapalinou.

{% endif %}
