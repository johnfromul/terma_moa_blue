# Lovelace Configuration Examples

## Basic Thermostat Card

```yaml
type: thermostat
entity: climate.terma_wireless_element
```

## Detailed Card with Graphs

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.terma_wireless_room
  
  - type: entities
    title: Details
    entities:
      - entity: sensor.terma_wireless_current_room_temperature
        name: Current Temperature
      - entity: sensor.terma_wireless_target_room_temperature
        name: Target Temperature
      - entity: sensor.terma_wireless_operating_mode
        name: Mode
  
  - type: history-graph
    title: Temperature History
    hours_to_show: 24
    entities:
      - entity: sensor.terma_wireless_current_room_temperature
        name: Room Temperature
      - entity: sensor.terma_wireless_current_element_temperature
        name: Element Temperature
```

## Card with Both Thermostats

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-climate-card
    entity: climate.terma_wireless_room
    name: Room Temperature
    icon: mdi:home-thermometer
    show_temperature_control: true
    hvac_modes:
      - heat
      - 'off'
    collapsible_controls: false
  
  - type: custom:mushroom-climate-card
    entity: climate.terma_wireless_element
    name: Element Temperature
    icon: mdi:radiator
    show_temperature_control: true
    hvac_modes:
      - heat
      - 'off'
    collapsible_controls: false
```

**Note:** Mushroom cards require the [mushroom](https://github.com/piitaya/lovelace-mushroom) custom card from HACS.

## Simple Quick Control Card

```yaml
type: entities
title: Bathroom Heating
entities:
  - type: custom:slider-entity-row
    entity: climate.terma_wireless_room
    name: Temperature
    toggle: true
```

**Note:** Slider card requires [slider-entity-row](https://github.com/thomasloven/lovelace-slider-entity-row).

## Card with Temperature Preset Buttons

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.terma_wireless_room
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Eco (18°C)
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_wireless_room
            temperature: 18
            hvac_mode: heat
      
      - type: button
        name: Comfort (22°C)
        icon: mdi:home
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_wireless_room
            temperature: 22
            hvac_mode: heat
      
      - type: button
        name: Boost (26°C)
        icon: mdi:fire
        tap_action:
          action: call-service
          service: climate.set_temperature
          service_data:
            entity_id: climate.terma_wireless_room
            temperature: 26
            hvac_mode: heat
      
      - type: button
        name: Turn Off
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: climate.turn_off
          service_data:
            entity_id: climate.terma_wireless_room
```

## Mini Graph Card

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.terma_wireless_current_room_temperature
    name: Room Temperature
    color: '#3498db'
  - entity: sensor.terma_wireless_target_room_temperature
    name: Target Temperature
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

**Note:** Mini-graph card requires [mini-graph-card](https://github.com/kalkih/mini-graph-card).

## Apex Charts (Advanced Visualization)

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Bathroom Heating - History
  show_states: true
  colorize_states: true
graph_span: 24h
update_interval: 1min
series:
  - entity: sensor.terma_wireless_current_room_temperature
    name: Room Temperature
    stroke_width: 2
    type: line
    color: '#2ecc71'
    curve: smooth
  - entity: sensor.terma_wireless_target_room_temperature
    name: Target Temperature
    stroke_width: 2
    type: line
    color: '#e74c3c'
    curve: stepline
  - entity: sensor.terma_wireless_current_element_temperature
    name: Element
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

**Note:** Apex charts card requires [apexcharts-card](https://github.com/RomRider/apexcharts-card).

## Conditional Card (Show Only When Heating)

```yaml
type: conditional
conditions:
  - entity: climate.terma_wireless_room
    state_not: 'off'
card:
  type: entities
  title: Heating is On
  entities:
    - entity: sensor.terma_wireless_current_room_temperature
      name: Current
    - entity: sensor.terma_wireless_target_room_temperature
      name: Target
    - entity: sensor.terma_wireless_operating_mode
      name: Mode
```

## Complete Bathroom Dashboard

```yaml
type: vertical-stack
cards:
  # Main thermostat
  - type: thermostat
    entity: climate.terma_wireless_room
  
  # Quick buttons
  - type: horizontal-stack
    cards:
      - type: button
        name: Eco
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: script.bathroom_heating_eco
      - type: button
        name: Comfort
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
  
  # Status and temperatures
  - type: entities
    title: Status
    show_header_toggle: false
    entities:
      - entity: sensor.terma_wireless_operating_mode
        name: Mode
        icon: mdi:cog
      - type: divider
      - entity: sensor.terma_wireless_current_room_temperature
        name: Room Temperature
        icon: mdi:thermometer
      - entity: sensor.terma_wireless_current_element_temperature
        name: Element Temperature
        icon: mdi:radiator
  
  # Graph
  - type: history-graph
    title: History (24h)
    hours_to_show: 24
    refresh_interval: 60
    entities:
      - entity: sensor.terma_wireless_current_room_temperature
        name: Room
      - entity: sensor.terma_wireless_target_room_temperature
        name: Target
```

And corresponding scripts in `configuration.yaml`:

```yaml
script:
  bathroom_heating_eco:
    alias: Bathroom - Eco Mode
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 18
          hvac_mode: heat
  
  bathroom_heating_comfort:
    alias: Bathroom - Comfort Mode
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 22
          hvac_mode: heat
  
  bathroom_heating_boost:
    alias: Bathroom - 2 Hour Boost
    sequence:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 26
          hvac_mode: heat
      - delay:
          hours: 2
      - service: script.bathroom_heating_comfort
```

## Automation Examples

### Morning Heating Schedule

```yaml
automation:
  - alias: "Bathroom Morning Heat"
    description: "Heat bathroom before morning shower"
    trigger:
      - platform: time
        at: "06:00:00"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.terma_wireless_element
        data:
          hvac_mode: heat
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_element
        data:
          temperature: 55
      - delay:
          minutes: 45
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.terma_wireless_element
        data:
          hvac_mode: "off"
```

### Temperature-Based Control

```yaml
automation:
  - alias: "Maintain Bathroom Temperature"
    description: "Keep bathroom at comfortable temperature"
    trigger:
      - platform: numeric_state
        entity_id: sensor.terma_wireless_current_room_temperature
        below: 20
    condition:
      - condition: state
        entity_id: binary_sensor.bathroom_occupied
        state: "on"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 22
          hvac_mode: heat
```

### Away Mode

```yaml
automation:
  - alias: "Away Mode - Lower Heating"
    description: "Reduce heating when away from home"
    trigger:
      - platform: state
        entity_id: person.home_owner
        to: "not_home"
        for:
          hours: 2
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 16
          hvac_mode: heat
  
  - alias: "Home Mode - Normal Heating"
    description: "Restore normal heating when returning home"
    trigger:
      - platform: state
        entity_id: person.home_owner
        to: "home"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_room
        data:
          temperature: 22
          hvac_mode: heat
```
