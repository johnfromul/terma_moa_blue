class KoupelnaThermostatCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._dragging = false;
    this._tempToSet = null;
    this._isUpdating = false;
    this._timer = null;
    this._lastAngle = null;
  }

  set hass(hass) {
    this._hass = hass;
    if (this._dragging || this._isUpdating) return;
    this._render();
  }

  setConfig(config) { 
    this._config = config; 
  }

  _calculateTemp(e) {
    const svg = this.shadowRoot.querySelector('#main-svg');
    const rect = svg.getBoundingClientRect();
    const clientX = (e.touches ? e.touches[0].clientX : e.clientX);
    const clientY = (e.touches ? e.touches[0].clientY : e.clientY);
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + (rect.height * (150/380));
    const x = clientX - centerX;
    const y = clientY - centerY;
    let angle = Math.atan2(y, x) * 180 / Math.PI + 90;
    if (angle < 0) angle += 360;
    let a = (angle < 135) ? angle + 360 : angle;

    const ARC_START = 220;
    const ARC_END = 500;
    const ARC_MID = (ARC_START + ARC_END) / 2; // 360

    // Dead zone handling: if angle is outside the arc range,
    // clamp to nearest endpoint based on which half of the dead zone we're in
    if (a < ARC_START || a > ARC_END) {
      // We're in the dead zone (500 -> 580 aka 220)
      // Use proximity to decide: if closer to END, clamp to 60; if closer to START, clamp to 30
      // But also use last known angle to prevent jumps during drag
      if (this._dragging && this._lastAngle !== null) {
        // If we were near the top end (high temp) and crossed into dead zone, stay at 60
        if (this._lastAngle > ARC_MID) {
          this._lastAngle = ARC_END;
          return 60;
        }
        // If we were near the bottom end (low temp) and crossed into dead zone, stay at 30
        this._lastAngle = ARC_START;
        return 30;
      }
      // Not dragging or no history - use geometric proximity
      if (a > ARC_END && a <= ARC_END + 40) return 60;
      if (a < ARC_START && a >= ARC_START - 40) return 30;
      return (a > ARC_MID) ? 60 : 30;
    }

    this._lastAngle = a;
    const ratio = (a - ARC_START) / (ARC_END - ARC_START);
    return Math.round(30 + (ratio * 30));
  }

  _updateVisuals(temp) {
    const angle = 220 + ((temp - 30) / 30) * 280;
    const rad = (angle - 90) * Math.PI / 180;
    const hx = 150 + 115 * Math.cos(rad);
    const hy = 150 + 115 * Math.sin(rad);
    const handle = this.shadowRoot.getElementById('handle');
    const handleText = this.shadowRoot.getElementById('handle-text');
    if (handle && handleText) {
      handle.setAttribute('cx', hx);
      handle.setAttribute('cy', hy);
      handleText.setAttribute('x', hx);
      handleText.setAttribute('y', hy + 5);
      handleText.textContent = temp;
    }
  }

  _render() {
    if (!this._hass) return;
    const tt = parseFloat(this._hass.states['input_number.koupelna_thermostat_temp_tyce']?.state) || 30;
    const tm = parseFloat(this._hass.states['input_number.koupelna_thermostat_temp_mistnost']?.state) || 24;
    const ta = parseFloat(this._hass.states['sensor.ble_temperature_atc_horni_koupelna']?.state) || 0;
    const hyst = parseFloat(this._hass.states['input_number.koupelna_thermostat_hystereze']?.state) || 1;
    
    const isEnabled = this._hass.states['input_boolean.koupelna_thermostat_enabled']?.state === 'on';
    const isHeating = this._hass.states['climate.terma_wireless_element_temperature_2']?.state === 'heat';
    const activeColor = isHeating ? '#ff9800' : '#444';

    const angle = 220 + ((tt - 30) / 30) * 280;
    const rad = (angle - 90) * Math.PI / 180;
    const hx = 150 + 115 * Math.cos(rad);
    const hy = 150 + 115 * Math.sin(rad);

    const arc = (s, e, r) => {
      const sr = (s - 90) * Math.PI / 180;
      const er = (e - 90) * Math.PI / 180;
      return `M ${150 + r * Math.cos(sr)} ${150 + r * Math.sin(sr)} A ${r} ${r} 0 0 1 ${150 + r * Math.cos(er)} ${150 + r * Math.sin(er)}`;
    };

    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; width: 100%; user-select: none; }
        ha-card { background: #1a1a1a !important; border-radius: 28px; padding: 16px; display: flex; flex-direction: column; align-items: center; }
        .card-header { width: 100%; padding: 8px 0px 16px 0px; color: var(--secondary-text-color); font-size: 16px; font-weight: 500; text-align: center; align-self: center; }
        .main-container { width: 300px; margin: 0 auto; position: relative; }
        svg { display: block; width: 300px; height: 380px; touch-action: none; overflow: visible; }
        .clickable { cursor: pointer; transition: all 0.2s ease; }
        .clickable:hover { opacity: 0.8; }
        .icon-area { cursor: pointer; pointer-events: auto; }
        .heating-bg { 
          fill: url(#grad); 
          opacity: ${isHeating ? 1 : 0}; 
          transition: opacity 0.5s ease-in-out;
        }
      </style>
      <ha-card>
        ${this._config.name ? `<div class="card-header">${this._config.name}</div>` : ''}
        <div class="main-container">
          <svg viewBox="0 0 300 380" id="main-svg">
            <defs>
              <radialGradient id="grad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                <stop offset="0%" style="stop-color:#ff9800;stop-opacity:0.15" />
                <stop offset="100%" style="stop-color:#ff9800;stop-opacity:0" />
              </radialGradient>
            </defs>

            <circle cx="150" cy="150" r="110" class="heating-bg" />

            <path d="${arc(220, 285.3, 115)}" fill="none" stroke="#FFD700" stroke-width="22"/>
            <path d="${arc(285.3, 341.3, 115)}" fill="none" stroke="#FFB900" stroke-width="22"/>
            <path d="${arc(341.3, 397.3, 115)}" fill="none" stroke="#FF8C00" stroke-width="22"/>
            <path d="${arc(397.3, 453.3, 115)}" fill="none" stroke="#E65100" stroke-width="22"/>
            <path d="${arc(453.3, 500, 115)}" fill="none" stroke="#D32F2F" stroke-width="22"/>
            
            <text x="150" y="110" text-anchor="middle" fill="${isHeating ? '#ff9800' : '#888'}" font-size="14" font-weight="bold" font-family="Arial">
              ${isHeating ? 'TOPÍ' : (isEnabled ? 'PŘIPRAVENO' : 'VYPNUTO')}
            </text>
            
            <text x="150" y="165" text-anchor="middle" fill="white" font-size="56" font-family="Arial">${tm}<tspan font-size="24" dy="-20">°C</tspan></text>
            <text x="135" y="200" text-anchor="middle" fill="#888" font-size="15" font-family="Arial">🌡 ${ta.toFixed(1)} °C</text>
            
            <circle id="drag-area" cx="150" cy="150" r="140" fill="transparent" class="clickable"/>
            
            <g id="btn-hysteresis" class="icon-area">
              <rect x="170" y="180" width="70" height="35" fill="transparent" />
              <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.47,5.34 14.86,5.08L14.47,2.44C14.43,2.19 14.22,2 13.97,2H9.97C9.72,2 9.5,2.19 9.47,2.44L9.08,5.08C8.47,5.34 7.9,5.66 7.38,6.05L4.89,5.05C4.67,4.96 4.4,5.05 4.27,5.27L2.27,8.73C2.15,8.95 2.2,9.22 2.39,9.37L4.5,11C4.47,11.34 4.44,11.67 4.44,12C4.44,12.33 4.47,12.65 4.5,12.97L2.39,14.63C2.2,14.78 2.15,15.05 2.27,15.27L4.27,18.73C4.4,18.95 4.67,19.03 4.89,18.94L7.38,17.94C7.9,18.33 8.47,18.65 9.08,18.91L9.47,21.56C9.5,21.81 9.72,22 9.97,22H13.97C14.22,22 14.43,21.81 14.47,21.56L14.86,18.91C15.47,18.65 16.04,18.33 16.56,17.94L19.05,18.94C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z" fill="#888" transform="translate(178, 188) scale(0.65)"/>
              <text x="198" y="201" text-anchor="start" fill="#888" font-size="12" font-family="Arial" font-weight="bold">H: ${hyst}</text>
            </g>

            <g class="clickable" id="btn-minus-group">
              <circle cx="120" cy="265" r="24" fill="#2a2a2a" stroke="#444" stroke-width="1"/>
              <text x="120" y="274" text-anchor="middle" fill="white" font-size="28" style="pointer-events:none;">−</text>
            </g>
            <g class="clickable" id="btn-plus-group">
              <circle cx="180" cy="265" r="24" fill="#2a2a2a" stroke="#444" stroke-width="1"/>
              <text x="180" y="274" text-anchor="middle" fill="white" font-size="28" style="pointer-events:none;">+</text>
            </g>
            
            <g class="clickable" id="btn-on">
              <circle cx="100" cy="335" r="30" fill="${isEnabled ? '#333' : '#222'}" />
              <path d="M12,18.5C10.07,18.5 8.5,16.93 8.5,15C8.5,13.07 10.07,11.5 12,11.5C13.93,11.5 15.5,13.07 15.5,15C15.5,16.93 13.93,18.5 12,18.5M12,2C12,2 6,7 6,12C6,15.31 8.69,18 12,18C15.31,18 18,15.31 18,12C18,7 12,2Z" 
                    fill="${activeColor}" transform="translate(85, 320) scale(1.2)" />
            </g>

            <g class="clickable" id="btn-off">
              <circle cx="200" cy="335" r="30" fill="${!isEnabled ? '#D32F2F' : '#222'}" opacity="${!isEnabled ? 0.8 : 1}" />
              <path d="M16.56,5.44L15.11,6.89C16.84,7.94 18,9.83 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12C6,9.83 7.16,7.94 8.88,6.88L7.44,5.44C5.36,6.88 4,9.28 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12C20,9.28 18.64,6.88 16.56,5.44M13,3H11V13H13" 
                    fill="${!isEnabled ? 'white' : '#888'}" transform="translate(185, 320) scale(1.2)" />
            </g>
            
            <circle id="handle" cx="${hx}" cy="${hy}" r="21" fill="#fff" stroke="#1a1a1a" stroke-width="4" style="pointer-events:none;"/>
            <text id="handle-text" x="${hx}" y="${hy + 5}" text-anchor="middle" fill="#000" font-size="12" font-weight="bold" style="pointer-events:none;">${tt}</text>
          </svg>
        </div>
      </ha-card>
    `;
    this._setupListeners();
  }

  _setupListeners() {
    const root = this.shadowRoot;
    const dragZone = root.querySelector('#drag-area');

    const start = (e) => {
      if (e.target.closest('#btn-hysteresis') || e.target.closest('#btn-minus-group') || e.target.closest('#btn-plus-group') || e.target.closest('#btn-on') || e.target.closest('#btn-off')) return;
      // Inner dead zone: ignore clicks inside the arc ring (radius < 93 in SVG coords)
      const svg = this.shadowRoot.querySelector('#main-svg');
      const rect = svg.getBoundingClientRect();
      const scale = rect.width / 300; // SVG viewBox is 300 wide
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + (rect.height * (150 / 380));
      const dx = e.clientX - cx;
      const dy = e.clientY - cy;
      const distFromCenter = Math.sqrt(dx * dx + dy * dy) / scale;
      if (distFromCenter < 93) return;
      this._dragging = true;
      this._isUpdating = true;
      this._lastAngle = null;
      if (this._timer) clearTimeout(this._timer);
      if (dragZone.setPointerCapture) dragZone.setPointerCapture(e.pointerId);
      this._tempToSet = this._calculateTemp(e);
      this._updateVisuals(this._tempToSet);
    };

    const move = (e) => { if (this._dragging) { this._tempToSet = this._calculateTemp(e); this._updateVisuals(this._tempToSet); } };

    const stop = (e) => {
      if (this._dragging) {
        this._dragging = false;
        this._lastAngle = null;
        if (dragZone.releasePointerCapture) dragZone.releasePointerCapture(e.pointerId);
        this._hass.callService('input_number', 'set_value', { entity_id: 'input_number.koupelna_thermostat_temp_tyce', value: this._tempToSet });
        this._timer = setTimeout(() => { this._isUpdating = false; this._render(); }, 2000);
      }
    };

    dragZone.addEventListener('pointerdown', start);
    dragZone.addEventListener('pointermove', move);
    dragZone.addEventListener('pointerup', stop);

    root.querySelector('#btn-hysteresis').onclick = (e) => {
      const event = new Event("hass-more-info", { bubbles: true, composed: true });
      event.detail = { entityId: 'input_number.koupelna_thermostat_hystereze' };
      this.dispatchEvent(event);
    };

    root.querySelector('#btn-plus-group').onclick = () => this._callService('input_number', 'increment', 'input_number.koupelna_thermostat_temp_mistnost');
    root.querySelector('#btn-minus-group').onclick = () => this._callService('input_number', 'decrement', 'input_number.koupelna_thermostat_temp_mistnost');
    root.querySelector('#btn-on').onclick = () => this._callService('input_boolean', 'turn_on', 'input_boolean.koupelna_thermostat_enabled');
    root.querySelector('#btn-off').onclick = () => this._callService('input_boolean', 'turn_off', 'input_boolean.koupelna_thermostat_enabled');
  }

  _callService(domain, service, entity) { this._hass.callService(domain, service, { entity_id: entity }); }
}
customElements.define('koupelna-thermostat-card', KoupelnaThermostatCard);