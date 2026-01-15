/**
 * Energy Generation Report Card
 * 
 * Custom Lovelace card for displaying energy generation reports
 * with interactive charts using ApexCharts
 */

class EnergyGenerationReportCard extends HTMLElement {

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._config = {};
    this._hass = null;
    this._entities = [];
  }

  static async getConfigElement() {
    await import("./energy-generation-report-card-editor.js");
    return document.createElement("energy-generation-report-card-editor");
  }

  static getStubConfig() {
    return {
      type: "custom:energy-generation-report-card",
      entities: [],
      title: "Energy Generation Report",
      show_toolbar: true,
      chart_type: "mixed", // bar, area, mixed
      period_months: 12
    };
  }

  setConfig(config) {
    if (!config) {
      throw new Error("Invalid configuration");
    }

    this._config = {
      show_toolbar: true,
      chart_type: "mixed",
      period_months: 12,
      title: "Energy Generation Report",
      ...config
    };

    if (!this._config.entities || this._config.entities.length === 0) {
      throw new Error("You need to define at least one energy generation report entity");
    }

    this._entities = this._config.entities;
  }

  set hass(hass) {
    this._hass = hass;
    this.updateCard();
  }

  connectedCallback() {
    this.loadApexCharts();
  }

  async loadApexCharts() {
    if (window.ApexCharts) {
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/apexcharts@latest/dist/apexcharts.min.js';
    script.onload = () => this.updateCard();
    document.head.appendChild(script);
  }

  updateCard() {
    if (!this._hass || !window.ApexCharts) return;

    const entity = this._hass.states[this._entities[0]];
    if (!entity) return;

    const periodsData = entity.attributes.periods_data || {};

    this.shadowRoot.innerHTML = `
      <style>
        .card-content {
          padding: 16px;
        }
        
        .card-header {
          font-size: 1.2em;
          font-weight: 500;
          margin-bottom: 16px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .toolbar {
          display: flex;
          gap: 8px;
          margin-bottom: 16px;
        }

        .toolbar button {
          padding: 8px 16px;
          border: 1px solid var(--divider-color);
          background: var(--card-background-color);
          color: var(--primary-text-color);
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }

        .toolbar button.active {
          background: var(--primary-color);
          color: var(--text-primary-color);
          border-color: var(--primary-color);
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 16px;
          margin-bottom: 20px;
        }

        .metric-card {
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          padding: 16px;
          text-align: center;
        }

        .metric-title {
          font-size: 0.9em;
          color: var(--secondary-text-color);
          margin-bottom: 8px;
        }

        .metric-value {
          font-size: 1.5em;
          font-weight: bold;
          color: var(--primary-text-color);
        }

        .metric-unit {
          font-size: 0.8em;
          color: var(--secondary-text-color);
          margin-left: 4px;
        }

        .chart-container {
          margin-top: 20px;
          min-height: 300px;
        }

        .no-data {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 40px;
          font-style: italic;
        }

        .balance-positive {
          color: var(--success-color, #4caf50);
        }

        .balance-negative {
          color: var(--error-color, #f44336);
        }
      </style>

      <ha-card>
        <div class="card-content">
          <div class="card-header">
            <span>${this._config.title}</span>
            ${this._config.show_toolbar ? this.renderAddDataButton() : ''}
          </div>

          ${this._config.show_toolbar ? this.renderToolbar() : ''}
          
          ${this.renderMetrics(periodsData)}
          
          <div class="chart-container" id="chart-container">
            ${Object.keys(periodsData).length === 0 ?
        '<div class="no-data">No billing data available. Add your first billing period data to see charts.</div>' :
        '<div id="chart"></div>'
      }
          </div>
        </div>
      </ha-card>
    `;

    if (Object.keys(periodsData).length > 0) {
      this.renderChart(periodsData);
    }
  }

  renderAddDataButton() {
    return `
      <button class="add-data-btn" onclick="this.getRootNode().host.openAddDataDialog()">
        Add Billing Data
      </button>
    `;
  }

  renderToolbar() {
    return `
      <div class="toolbar">
        <button class="${this._config.chart_type === 'bar' ? 'active' : ''}" 
                onclick="this.getRootNode().host.setChartType('bar')">
          Bar Chart
        </button>
        <button class="${this._config.chart_type === 'area' ? 'active' : ''}"
                onclick="this.getRootNode().host.setChartType('area')">
          Area Chart  
        </button>
        <button class="${this._config.chart_type === 'mixed' ? 'active' : ''}"
                onclick="this.getRootNode().host.setChartType('mixed')">
          Mixed Chart
        </button>
      </div>
    `;
  }

  renderMetrics(periodsData) {
    if (Object.keys(periodsData).length === 0) {
      return '<div class="no-data">No data available</div>';
    }

    // Get latest period data
    const latestPeriod = Object.values(periodsData)
      .sort((a, b) => new Date(b.end_date) - new Date(a.end_date))[0];

    return `
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-title">Solar Generation</div>
          <div class="metric-value">
            ${latestPeriod.solar_generation.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Grid Consumption</div>
          <div class="metric-value">
            ${latestPeriod.grid_consumption.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Grid Injection</div>
          <div class="metric-value">
            ${latestPeriod.grid_injection.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Total Consumption</div>
          <div class="metric-value">
            ${latestPeriod.total_consumption.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Solar Consumption</div>
          <div class="metric-value">
            ${latestPeriod.solar_consumption.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Cumulative Balance</div>
          <div class="metric-value ${latestPeriod.cumulative_balance >= 0 ? 'balance-positive' : 'balance-negative'}">
            ${latestPeriod.cumulative_balance.toFixed(1)}
            <span class="metric-unit">kWh</span>
          </div>
        </div>
      </div>
    `;
  }

  renderChart(periodsData) {
    const chartElement = this.shadowRoot.getElementById('chart');
    if (!chartElement || !window.ApexCharts) return;

    // Sort periods by end date
    const sortedPeriods = Object.values(periodsData)
      .sort((a, b) => new Date(a.end_date) - new Date(b.end_date))
      .slice(-this._config.period_months);

    const categories = sortedPeriods.map(period => {
      const date = new Date(period.end_date);
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    });

    let series = [];
    let chartType = this._config.chart_type;

    if (chartType === 'bar' || chartType === 'mixed') {
      series.push({
        name: 'Solar Generation',
        type: 'column',
        data: sortedPeriods.map(p => p.solar_generation.toFixed(1))
      });

      series.push({
        name: 'Grid Consumption',
        type: 'column',
        data: sortedPeriods.map(p => p.grid_consumption.toFixed(1))
      });

      series.push({
        name: 'Grid Injection',
        type: 'column',
        data: sortedPeriods.map(p => p.grid_injection.toFixed(1))
      });

      series.push({
        name: 'Solar Consumption',
        type: 'column',
        data: sortedPeriods.map(p => p.solar_consumption.toFixed(1))
      });
    }

    if (chartType === 'area' || chartType === 'mixed') {
      series.push({
        name: 'Cumulative Balance',
        type: chartType === 'mixed' ? 'line' : 'area',
        data: sortedPeriods.map(p => p.cumulative_balance.toFixed(1))
      });
    }

    const options = {
      series: series,
      chart: {
        height: 350,
        type: chartType === 'mixed' ? 'line' : chartType,
        toolbar: {
          show: true,
          tools: {
            download: true,
            selection: false,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: false,
            reset: true
          }
        }
      },
      colors: ['#FFA726', '#42A5F5', '#66BB6A', '#AB47BC', '#EF5350'],
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          endingShape: 'rounded'
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: chartType === 'mixed' ? [0, 0, 0, 0, 3] : 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: categories,
        title: {
          text: 'Billing Periods'
        }
      },
      yaxis: {
        title: {
          text: 'Energy (kWh)'
        }
      },
      fill: {
        opacity: chartType === 'area' ? 0.6 : 0.8
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + " kWh";
          }
        }
      },
      legend: {
        position: 'top',
        horizontalAlign: 'left'
      }
    };

    if (this.chart) {
      this.chart.destroy();
    }

    this.chart = new ApexCharts(chartElement, options);
    this.chart.render();
  }

  setChartType(type) {
    this._config.chart_type = type;
    this.updateCard();
  }

  openAddDataDialog() {
    if (!this._hass) return;

    const entity = this._hass.states[this._entities[0]];
    if (!entity) return;

    const configEntryId = entity.attributes.config_entry_id;

    this._hass.callService('energy_generation_report', 'add_billing_data', {
      config_entry_id: configEntryId,
      end_date: new Date().toISOString().split('T')[0],
      grid_consumption_reading: 0,
      grid_injection_reading: 0
    });
  }

  getCardSize() {
    return 6;
  }
}

customElements.define('energy-generation-report-card', EnergyGenerationReportCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'energy-generation-report-card',
  name: 'Energy Generation Report Card',
  description: 'A card to display energy generation reports with interactive charts'
});

console.info(
  `%c ENERGY-GENERATION-REPORT-CARD %c v1.0.0 `,
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray',
);