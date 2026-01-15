/**
 * Energy Generation Report Card Editor
 * 
 * Configuration editor for the custom card
 */

class EnergyGenerationReportCardEditor extends HTMLElement {

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    this._config = config;
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  get _entities() {
    return this._config?.entities || [];
  }

  get _title() {
    return this._config?.title || 'Energy Generation Report';
  }

  get _show_toolbar() {
    return this._config?.show_toolbar !== false;
  }

  get _chart_type() {
    return this._config?.chart_type || 'mixed';
  }

  get _period_months() {
    return this._config?.period_months || 12;
  }

  render() {
    if (!this._hass) {
      return;
    }

    // Get all energy generation report entities
    const entities = Object.keys(this._hass.states)
      .filter(entity => entity.startsWith('sensor.') &&
        this._hass.states[entity].attributes.sensor_type)
      .map(entity => ({
        value: entity,
        label: this._hass.states[entity].attributes.friendly_name || entity
      }));

    this.shadowRoot.innerHTML = `
      <style>
        .card-config {
          padding: 16px;
        }
        
        .form-group {
          margin-bottom: 16px;
        }
        
        .form-group label {
          display: block;
          margin-bottom: 4px;
          font-weight: 500;
          color: var(--primary-text-color);
        }
        
        .form-group input,
        .form-group select,
        .form-group ha-entity-picker {
          width: 100%;
          padding: 8px;
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          background: var(--card-background-color);
          color: var(--primary-text-color);
          font-size: 14px;
        }
        
        .form-group ha-switch {
          margin-top: 8px;
        }
        
        .entities-list {
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          padding: 8px;
          min-height: 100px;
          background: var(--card-background-color);
        }
        
        .entity-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 4px 8px;
          margin: 2px 0;
          background: var(--primary-color);
          color: var(--text-primary-color);
          border-radius: 4px;
          font-size: 14px;
        }
        
        .entity-item button {
          background: none;
          border: none;
          color: var(--text-primary-color);
          cursor: pointer;
          padding: 2px 6px;
          border-radius: 2px;
        }
        
        .entity-item button:hover {
          background: rgba(255,255,255,0.2);
        }
        
        .add-entity {
          margin-top: 8px;
        }
      </style>

      <div class="card-config">
        
        <div class="form-group">
          <label>Title</label>
          <input
            type="text"
            .value="${this._title}"
            @input="${this._titleChanged}"
            placeholder="Energy Generation Report"
          />
        </div>

        <div class="form-group">
          <label>Entities</label>
          <div class="entities-list">
            ${this._entities.map((entity, index) => `
              <div class="entity-item">
                <span>${this._hass.states[entity]?.attributes?.friendly_name || entity}</span>
                <button @click="${() => this._removeEntity(index)}">×</button>
              </div>
            `).join('')}
            ${this._entities.length === 0 ? '<em>No entities selected</em>' : ''}
          </div>
          
          <div class="add-entity">
            <ha-entity-picker
              .hass="${this._hass}"
              .value=""
              .includeDomains="${['sensor']}"
              .entityFilter="${entity => entity.startsWith('sensor.') &&
        this._hass.states[entity].attributes.sensor_type}"
              @value-changed="${this._entityChanged}"
              placeholder="Add energy generation report entity"
            ></ha-entity-picker>
          </div>
        </div>

        <div class="form-group">
          <label>Chart Type</label>
          <select .value="${this._chart_type}" @change="${this._chartTypeChanged}">
            <option value="bar">Bar Chart</option>
            <option value="area">Area Chart</option>
            <option value="mixed">Mixed Chart</option>
          </select>
        </div>

        <div class="form-group">
          <label>Period Months to Show</label>
          <input
            type="number"
            min="1"
            max="60"
            .value="${this._period_months}"
            @input="${this._periodMonthsChanged}"
          />
        </div>

        <div class="form-group">
          <label>
            <ha-switch
              .checked="${this._show_toolbar}"
              @change="${this._showToolbarChanged}"
            ></ha-switch>
            Show Toolbar
          </label>
        </div>

      </div>
    `;
  }

  _titleChanged(ev) {
    if (!this._config || !this._hass) {
      return;
    }

    this._config = {
      ...this._config,
      title: ev.target.value,
    };

    this._configChanged();
  }

  _entityChanged(ev) {
    if (!this._config || !this._hass) {
      return;
    }

    const entity = ev.detail.value;
    if (!entity || this._entities.includes(entity)) {
      return;
    }

    this._config = {
      ...this._config,
      entities: [...this._entities, entity],
    };

    this._configChanged();

    // Clear the entity picker
    ev.target.value = '';
  }

  _removeEntity(index) {
    if (!this._config || !this._hass) {
      return;
    }

    const entities = [...this._entities];
    entities.splice(index, 1);

    this._config = {
      ...this._config,
      entities,
    };

    this._configChanged();
  }

  _chartTypeChanged(ev) {
    if (!this._config || !this._hass) {
      return;
    }

    this._config = {
      ...this._config,
      chart_type: ev.target.value,
    };

    this._configChanged();
  }

  _periodMonthsChanged(ev) {
    if (!this._config || !this._hass) {
      return;
    }

    this._config = {
      ...this._config,
      period_months: parseInt(ev.target.value, 10),
    };

    this._configChanged();
  }

  _showToolbarChanged(ev) {
    if (!this._config || !this._hass) {
      return;
    }

    this._config = {
      ...this._config,
      show_toolbar: ev.target.checked,
    };

    this._configChanged();
  }

  _configChanged() {
    // Fire the config-changed event
    const event = new CustomEvent('config-changed', {
      detail: { config: this._config },
      bubbles: true,
      composed: true,
    });

    this.dispatchEvent(event);
  }
}

customElements.define('energy-generation-report-card-editor', EnergyGenerationReportCardEditor);