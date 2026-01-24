# Příklady konfigurace pro Lovelace

## Základní termostat karta

```yaml
type: thermostat
entity: climate.terma_moa_blue_pokojova_teplota
```

## Detailní karta s grafy

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.terma_moa_blue_pokojova_teplota
  
  - type: entities
    title: Detaily
    entities:
      - entity: sensor.terma_moa_blue_current_room_temperature
        name: Aktuální teplota
      - entity: sensor.terma_moa_blue_target_room_temperature
        name: Cílová teplota
      - entity: sensor.terma_moa_blue_operating_mode
        name: Režim
  
  - type: history-graph
    title: Teplota - historie
    hours_to_show: 24
    entities:
      - entity: sensor.terma_moa_blue_current_room_temperature
        name: Pokojová teplota
      - entity: sensor.terma_moa_blue_current_element_temperature
        name: Teplota radiátoru
```

## Karta s oběma termostaty

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-climate-card
    entity: climate.terma_moa_blue_pokojova_teplota
    name: Pokojová teplota
    icon: mdi:home-thermometer
    show_temperature_control: true
    hvac_modes:
      - heat
      - 'off'
    collapsible_controls: false
  
  - type: custom:mushroom-climate-card
    entity: climate.terma_moa_blue_teplota_topne_tyce
    name: Teplota radiátoru
    icon: mdi:radiator
    show_temperature_control: true
    hvac_modes:
      - heat
      - 'off'
    collapsible_controls: false
```

**Poznámka:** Pro mushroom karty potřebujete [mushroom](https://github.com/piitaya/lovelace-mushroom) custom kartu z HACS.

## Jednoduchá karta pro rychlé ovládání

```yaml
type: entities
title: Topení koupelna
entities:
  - type: custom:slider-entity-row
    entity: climate.terma_moa_blue_pokojova_teplota
    name: Teplota
    toggle: true
```

**Poznámka:** Pro slider kartu potřebujete [slider-entity-row](https://github.com/thomasloven/lovelace-slider-entity-row).

## Karta s tlačítky preset teplot

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.terma_moa_blue_pokojova_teplota
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Eco (18°C)
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_moa_blue_pokojova_teplota
            temperature: 18
            hvac_mode: heat
      
      - type: button
        name: Komfort (22°C)
        icon: mdi:home
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_moa_blue_pokojova_teplota
            temperature: 22
            hvac_mode: heat
      
      - type: button
        name: Boost (26°C)
        icon: mdi:fire
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_moa_blue_pokojova_teplota
            temperature: 26
            hvac_mode: heat
      
      - type: button
        name: Vypnout
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: climate.turn_off
          service_data:
            entity_id: climate.terma_moa_blue_pokojova_teplota
```

## Mini graf karta

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.terma_moa_blue_current_room_temperature
    name: Pokojová teplota
    color: '#3498db'
  - entity: sensor.terma_moa_blue_target_room_temperature
    name: Cílová teplota
    color: '#e74c3c'
    show_line: false
    show_points: true
hours_to_show: 24
line_width: 2
font_size: 75
animate: true
show:
  name: true
  icon: true
  state: true
  legend: false
```

**Poznámka:** Pro mini-graph kartu potřebujete [mini-graph-card](https://github.com/kalkih/mini-graph-card).

## Apex Charts (pokročilá vizualizace)

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Topení koupelna - historie
  show_states: true
  colorize_states: true
graph_span: 24h
update_interval: 1min
series:
  - entity: sensor.terma_moa_blue_current_room_temperature
    name: Pokojová teplota
    stroke_width: 2
    type: line
    color: '#2ecc71'
    curve: smooth
  - entity: sensor.terma_moa_blue_target_room_temperature
    name: Cílová teplota
    stroke_width: 2
    type: line
    color: '#e74c3c'
    curve: stepline
  - entity: sensor.terma_moa_blue_current_element_temperature
    name: Radiátor
    stroke_width: 2
    type: line
    color: '#f39c12'
    curve: smooth
yaxis:
  - min: 15
    max: 30
    decimals: 1
    apex_config:
      tickAmount: 6
```

**Poznámka:** Pro apex charts kartu potřebujete [apexcharts-card](https://github.com/RomRider/apexcharts-card).

## Conditional card (zobrazit jen když topí)

```yaml
type: conditional
conditions:
  - entity: climate.terma_moa_blue_pokojova_teplota
    state_not: 'off'
card:
  type: entities
  title: Topení je zapnuté
  entities:
    - entity: sensor.terma_moa_blue_current_room_temperature
      name: Aktuální
    - entity: sensor.terma_moa_blue_target_room_temperature
      name: Cílová
    - entity: sensor.terma_moa_blue_operating_mode
      name: Režim
```

## Kompletní dashboard pro koupelnu

```yaml
type: vertical-stack
cards:
  # Hlavní termostat
  - type: thermostat
    entity: climate.terma_moa_blue_pokojova_teplota
  
  # Rychlá tlačítka
  - type: horizontal-stack
    cards:
      - type: button
        name: Eco
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: script.bathroom_heating_eco
      - type: button
        name: Komfort
        icon: mdi:home
        tap_action:
          action: call-service
          service: script.bathroom_heating_comfort
      - type: button
        name: Boost 2h
        icon: mdi:fire
        tap_action:
          action: call-service
          service: script.bathroom_heating_boost
  
  # Status a teploty
  - type: entities
    title: Status
    show_header_toggle: false
    entities:
      - entity: sensor.terma_moa_blue_operating_mode
        name: Režim
        icon: mdi:cog
      - type: divider
      - entity: sensor.terma_moa_blue_current_room_temperature
        name: Pokojová teplota
        icon: mdi:thermometer
      - entity: sensor.terma_moa_blue_current_element_temperature
        name: Teplota radiátoru
        icon: mdi:radiator
  
  # Graf
  - type: history-graph
    title: Historie (24h)
    hours_to_show: 24
    refresh_interval: 60
    entities:
      - entity: sensor.terma_moa_blue_current_room_temperature
        name: Pokojová
      - entity: sensor.terma_moa_blue_target_room_temperature
        name: Cílová
```

A příslušné scripty v `configuration.yaml`:

```yaml
script:
  bathroom_heating_eco:
    alias: Koupelna - Eco režim
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 18
          hvac_mode: heat
  
  bathroom_heating_comfort:
    alias: Koupelna - Komfortní režim
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 22
          hvac_mode: heat
  
  bathroom_heating_boost:
    alias: Koupelna - Boost 2 hodiny
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_moa_blue_pokojova_teplota
        data:
          temperature: 26
          hvac_mode: heat
      - delay:
          hours: 2
      - service: script.bathroom_heating_comfort
```
