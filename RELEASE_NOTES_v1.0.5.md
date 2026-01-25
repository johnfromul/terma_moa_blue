# v1.0.5 - FIX: Dočasná BLE připojení místo permanentních

## 🔥 KRITICKÁ OPRAVA - Connection Management

### Hlavní problém
Topné tyče **netolerují permanentní BLE připojení**. Verze 1.0.4 a starší používaly `establish_connection` s trvalým spojením, což způsobovalo:
- `EOFError` - okamžité odpojení
- `out of connection slots` - vyčerpání BLE slotů
- 615+ odpojení během krátké doby

### Řešení: Connect-Use-Disconnect pattern
Integrace nyní používá **dočasná připojení**:
1. **Připoj se** k topné tyči
2. **Proveď operaci** (čti/zapiš data)
3. **Okamžitě odpoj**

### Změny v kódu

**api.py - kompletní přepsání:**
```python
# PŘED (v1.0.4):
self._client = await establish_connection(...)  # Trvalé spojení
await self._client.read_gatt_char(...)

# PO (v1.0.5):
async with BleakClient(address) as client:  # Dočasné spojení
    await client.read_gatt_char(...)
    # Automaticky se odpojí po operaci
```

**coordinator.py:**
- Odstraněn `register_disconnect_callback`
- Odstraněn `async_shutdown` disconnect
- Koordinátor pouze volá `device.update()` každých 120s

**const.py:**
- `UPDATE_INTERVAL = 120` (zvýšeno z 30s na 2 minuty)
- Důvod: Topné tyče potřebují čas mezi připojeními

## 📊 Testování

Po této změně by měly zmizet chyby:
```
❌ Failed to connect: EOFError
❌ out of connection slots
❌ Device disconnected (615×)
```

A měly by fungovat:
```
✅ Připojení k topné tyči
✅ Čtení teplot a režimu
✅ Nastavování teploty
✅ Zapínání/vypínání
```

## ⚠️ Důležité poznámky

1. **Update interval je 120s** - stav se aktualizuje každé 2 minuty (ne 30s)
2. **Žádné realtimové aktualizace** - topné tyče nepoužívají notifications
3. **Jedna operace = jedno připojení** - každý set_temperature vytvoří nové spojení

## 📦 Instalace

```bash
# 1. Odstraň starou integraci kompletně
# HA: Nastavení → Zařízení a služby → Terma MOA Blue → Odstranit (obě topné tyče)

# 2. HACS: Odinstaluj a nainstaluj v1.0.5
# Restartuj HA

# 3. Přidej integraci znovu
# Topná tyč do párovacího režimu (5s, modrá LED)
# Nastavení → + Přidat integraci → Terma MOA Blue
```

## 🔧 Technické detaily

### Před (v1.0.4):
- Permanentní BLE spojení
- 30s update interval  
- `establish_connection` + callbacks
- **Nefunguje** - topné tyče okamžitě odpojují

### Po (v1.0.5):
- Dočasná BLE spojení
- 120s update interval
- `async with BleakClient` pattern
- **Mělo by fungovat** - stejný pattern jako mobilní app

---

Tato verze by měla **konečně vyřešit** všechny connection problémy! 🎉
