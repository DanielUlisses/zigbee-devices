# Energy Generation Report

A comprehensive Home Assistant custom component for tracking and visualizing energy generation, consumption, and billing cycles with interactive charts.

## Features

- **Solar Energy Tracking**: Monitor daily solar energy production from any Home Assistant energy sensor
- **Billing Period Management**: Flexible billing periods with customizable start/end dates
- **Automatic Calculations**: 
  - Monthly solar generation
  - Grid consumption and injection
  - Total energy consumption
  - Solar consumption (self-use)
  - Cumulative balance tracking
- **Interactive Charts**: Beautiful ApexCharts visualizations with multiple chart types
- **Balance Management**: Track energy credits/debits with utility company including minimum billing amounts
- **Data Persistence**: Stores billing data locally in Home Assistant
- **Service Integration**: Easy data entry through Home Assistant services

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations" 
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Install the "Energy Generation Report" integration
6. Restart Home Assistant

### Manual Installation

1. Download the `energy_generation_report` folder
2. Copy it to your `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Integration Setup

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Energy Generation Report"
4. Configure the following:

   - **Name**: Display name for your energy report
   - **Solar Energy Sensor**: Select your daily solar production sensor
   - **Initial Grid Consumption Reading**: Starting meter reading for grid consumption
   - **Initial Grid Injection Reading**: Starting meter reading for grid injection
   - **Minimum Billing Amount**: Minimum kWh charged by utility (default: 100 kWh)
   - **Initial Balance**: Starting credit/debt balance with utility
   - **Billing Period Length**: Default days per billing period (default: 30)

### Adding Billing Data

Use the service `energy_generation_report.add_billing_data` to add monthly billing information:

```yaml
service: energy_generation_report.add_billing_data
data:
  config_entry_id: "your_config_entry_id"
  end_date: "2024-01-15"
  grid_consumption_reading: 12450.5
  grid_injection_reading: 8320.2
```

You can find your `config_entry_id` in the sensor attributes.

## Lovelace Card

### Installation

1. Add the JavaScript files to your Lovelace resources:

```yaml
resources:
  - url: /local/community/energy_generation_report/energy-generation-report-card.js
    type: module
```

### Card Configuration

```yaml
type: custom:energy-generation-report-card
entities:
  - sensor.energy_generation_report_monthly_solar_generation
title: "My Energy Report"
chart_type: mixed  # bar, area, or mixed
period_months: 12
show_toolbar: true
```

### Card Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entities` | list | **Required** | List of energy generation report sensors |
| `title` | string | "Energy Generation Report" | Card title |
| `chart_type` | string | "mixed" | Chart type: `bar`, `area`, or `mixed` |
| `period_months` | number | 12 | Number of months to show in charts |
| `show_toolbar` | boolean | true | Show chart type selection toolbar |

## Sensors

The integration creates the following sensors:

- **Monthly Solar Generation**: Total solar energy generated in the current period
- **Monthly Grid Consumption**: Energy consumed from grid in the current period  
- **Monthly Grid Injection**: Energy injected to grid in the current period
- **Monthly Total Consumption**: Total energy consumed (grid + solar - injection)
- **Monthly Solar Consumption**: Solar energy consumed directly (solar - injection)
- **Cumulative Energy Balance**: Running balance of credits/debits with utility

## Services

### `energy_generation_report.add_billing_data`

Add billing period data.

**Parameters:**
- `config_entry_id`: ID of the energy report integration instance
- `end_date`: End date of billing period (YYYY-MM-DD)
- `grid_consumption_reading`: Cumulative meter reading for grid consumption
- `grid_injection_reading`: Cumulative meter reading for grid injection

### `energy_generation_report.update_billing_data`

Update existing billing period data.

**Parameters:** Same as `add_billing_data`

### `energy_generation_report.delete_billing_data`

Delete billing period data.

**Parameters:**
- `config_entry_id`: ID of the energy report integration instance
- `end_date`: End date of billing period to delete

### `energy_generation_report.add_solar_data`

Add solar generation data for a specific date.

**Parameters:**
- `config_entry_id`: ID of the energy report integration instance
- `date`: Date for solar data (YYYY-MM-DD)
- `solar_generation_kwh`: Solar energy generated on this date

### `energy_generation_report.update_solar_data`

Update existing solar generation data for a specific date.

**Parameters:** Same as `add_solar_data`

### `energy_generation_report.delete_solar_data`

Delete solar generation data for a specific date.

**Parameters:**
- `config_entry_id`: ID of the energy report integration instance
- `date`: Date of solar data to delete

### `energy_generation_report.add_solar_period_data`

Add solar generation data for an entire period, automatically distributed evenly across all days.

**Parameters:**
- `config_entry_id`: ID of the energy report integration instance
- `start_date`: First date of the period (YYYY-MM-DD)
- `end_date`: Last date of the period (YYYY-MM-DD)
- `total_solar_generation_kwh`: Total solar energy for the entire period (will be divided equally among days)

## How It Works

### Data Collection

1. **Solar Data**: The component monitors your selected solar sensor daily and accumulates production for each billing period
2. **Billing Data**: You manually input meter readings from your utility bill each month
3. **Calculations**: The component calculates consumption, injection, and balance changes automatically

### Balance Calculation

The cumulative balance represents your net energy position with the utility:

- **Positive Balance**: You have energy credits (injected more than consumed)
- **Negative Balance**: You owe energy costs (consumed more than injected)

The minimum billing amount (typically 100 kWh) is automatically subtracted from grid consumption when calculating balance changes.

### Period Management

- Each billing period is defined by its end date
- The next period automatically starts the day after the previous period ends
- Default period length is configurable but can be overridden by actual billing dates

## Troubleshooting

### No Solar Data

- Ensure your solar sensor is properly configured and reporting daily values
- Check that the sensor resets daily (not cumulative)
- Verify the sensor has the `energy` device class

### Missing Charts

- Ensure ApexCharts is loaded (card will load it automatically)
- Check browser console for JavaScript errors
- Verify you have billing data entered

### Incorrect Calculations

- Verify initial meter readings are correct
- Check that billing data is entered in chronological order
- Ensure meter readings are cumulative values, not period values

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide Home Assistant logs when reporting bugs

## License

This project is licensed under the MIT License.