# Example configurations for Energy Generation Report

## Lovelace Card Examples

### Basic Configuration
```yaml
type: custom:energy-generation-report-card
entities:
  - sensor.energy_generation_report_monthly_solar_generation
```

### Full Configuration
```yaml
type: custom:energy-generation-report-card
entities:
  - sensor.energy_generation_report_monthly_solar_generation
title: "Solar Energy Dashboard"
chart_type: mixed
period_months: 24
show_toolbar: true
```

### Multiple Reports
```yaml
type: vertical-stack
cards:
  - type: custom:energy-generation-report-card
    entities:
      - sensor.house_energy_generation_report_monthly_solar_generation
    title: "House Solar Report"
    chart_type: bar
    period_months: 12

  - type: custom:energy-generation-report-card
    entities:
      - sensor.garage_energy_generation_report_monthly_solar_generation
    title: "Garage Solar Report"
    chart_type: area
    period_months: 6
```

## Automation Examples

### Monthly Billing Reminder
```yaml
automation:
  - alias: "Monthly Energy Bill Reminder"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: "{{ now().day == 15 }}"  # Remind on 15th of each month
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Energy Bill Reminder"
          message: "Don't forget to enter your monthly energy meter readings!"
          data:
            actions:
              - action: "OPEN_ENERGY_DASHBOARD"
                title: "Open Dashboard"
```

### Auto-populate Grid Readings (if you have smart meter sensors)
```yaml
automation:
  - alias: "Auto Add Energy Billing Data"
    trigger:
      - platform: time
        at: "23:59:00"
    condition:
      - condition: template
        value_template: "{{ now().day == 14 }}"  # Run on 14th (bill period ends 15th)
    action:
      - service: energy_generation_report.add_billing_data
        data:
          config_entry_id: "your_config_entry_id_here"
          end_date: "{{ (now().replace(day=15)).strftime('%Y-%m-%d') }}"
          grid_consumption_reading: "{{ states('sensor.your_grid_consumption_meter') | float }}"
          grid_injection_reading: "{{ states('sensor.your_grid_injection_meter') | float }}"
```

### Add Historical Solar Data
```yaml
script:
  add_historical_solar_data:
    alias: "Add Historical Solar Generation Data"
    sequence:
      # January 1st, 2024 - 45.2 kWh
      - service: energy_generation_report.add_solar_data
        data:
          config_entry_id: "your_config_entry_id"
          date: "2024-01-01"
          solar_generation_kwh: 45.2

      # January 2nd, 2024 - 38.7 kWh
      - service: energy_generation_report.add_solar_data
        data:
          config_entry_id: "your_config_entry_id"
          date: "2024-01-02"
          solar_generation_kwh: 38.7
```

### Add Solar Data for Full Period (Distributed)
```yaml
script:
  add_solar_period_data:
    alias: "Add Solar Generation for Entire Month"
    sequence:
      # Add 850 kWh for entire January 2024 (will be split across 31 days = ~27.4 kWh/day)
      - service: energy_generation_report.add_solar_period_data
        data:
          config_entry_id: "your_config_entry_id"
          start_date: "2024-01-01"
          end_date: "2024-01-31"
          total_solar_generation_kwh: 850.0

      # Add 720 kWh for first half of February (will be split across 14 days = ~51.4 kWh/day)
      - service: energy_generation_report.add_solar_period_data
        data:
          config_entry_id: "your_config_entry_id"
          start_date: "2024-02-01"
          end_date: "2024-02-14"
          total_solar_generation_kwh: 720.0
```

## Service Call Examples

### Add Billing Data via Script
```yaml
script:
  add_january_billing:
    alias: "Add January Energy Bill"
    sequence:
      - service: energy_generation_report.add_billing_data
        data:
          config_entry_id: "01234567890abcdef"
          end_date: "2024-01-15"
          grid_consumption_reading: 45678.9
          grid_injection_reading: 12345.6
```

### Bulk Import Historical Data
```yaml
script:
  import_historical_data:
    alias: "Import Historical Energy Data"
    sequence:
      # December 2023
      - service: energy_generation_report.add_billing_data
        data:
          config_entry_id: "your_config_entry_id"
          end_date: "2023-12-15"
          grid_consumption_reading: 42000.0
          grid_injection_reading: 8500.0

      # January 2024
      - service: energy_generation_report.add_billing_data
        data:
          config_entry_id: "your_config_entry_id"
          end_date: "2024-01-15"
          grid_consumption_reading: 43200.5
          grid_injection_reading: 9850.2

      # February 2024
      - service: energy_generation_report.add_billing_data
        data:
          config_entry_id: "your_config_entry_id"
          end_date: "2024-02-15"
          grid_consumption_reading: 44150.8
          grid_injection_reading: 11200.7

      # Add historical solar data if sensor wasn't available
      - service: energy_generation_report.add_solar_data
        data:
          config_entry_id: "your_config_entry_id"
          date: "2023-12-01"
          solar_generation_kwh: 42.5

      - service: energy_generation_report.add_solar_data
        data:
          config_entry_id: "your_config_entry_id"
          date: "2023-12-02"
          solar_generation_kwh: 38.9

      # Or add entire month at once (1240 kWh across 31 days = 40 kWh/day)
      - service: energy_generation_report.add_solar_period_data
        data:
          config_entry_id: "your_config_entry_id"
          start_date: "2023-11-01"
          end_date: "2023-11-30"
          total_solar_generation_kwh: 1240.0
```

## Dashboard Layout Example

### Energy Tab in Lovelace
```yaml
title: Energy Management
path: energy
icon: mdi:lightning-bolt
cards:
  - type: horizontal-stack
    cards:
      - type: entity
        entity: sensor.energy_generation_report_monthly_solar_generation
        name: "This Month Solar"

      - type: entity
        entity: sensor.energy_generation_report_monthly_total_consumption
        name: "This Month Usage"

      - type: entity
        entity: sensor.energy_generation_report_cumulative_balance
        name: "Energy Balance"

  - type: custom:energy-generation-report-card
    entities:
      - sensor.energy_generation_report_monthly_solar_generation
    title: "Annual Energy Overview"
    chart_type: mixed
    period_months: 12
    show_toolbar: true

  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.energy_generation_report_monthly_solar_generation
        name: "Solar Generation"
        min: 0
        max: 2000
        severity:
          green: 1000
          yellow: 500
          red: 0

      - type: gauge
        entity: sensor.energy_generation_report_cumulative_balance
        name: "Energy Balance"
        min: -500
        max: 500
        severity:
          green: 0
          yellow: -200
          red: -400

  - type: entities
    title: "Quick Actions"
    entities:
      - entity: script.add_current_billing_data
        name: "Add This Month's Bill"
        icon: mdi:plus-circle
        tap_action:
          action: call-service
          service: script.turn_on
          service_data:
            entity_id: script.add_current_billing_data
```

## Integration with Energy Dashboard

You can integrate these sensors with Home Assistant's built-in Energy dashboard:

1. Go to Settings → Dashboards → Energy
2. Configure Energy Sources:
   - Solar Production: Use your original solar sensor
   - Grid Consumption: Use your grid consumption sensor
   - Return to Grid: Use your grid injection sensor

3. The Energy Generation Report complements this by providing:
   - Historical period comparisons
   - Balance tracking with utility company
   - Custom billing period alignment
   - Advanced visualization options

## Tips for Best Results

1. **Consistent Timing**: Enter billing data on the same day each month
2. **Verify Readings**: Double-check meter readings for accuracy
3. **Monitor Daily**: Check that your solar sensor is updating daily
4. **Regular Backups**: Export your configuration including the integration data
5. **Chart Analysis**: Use different chart types to identify trends and patterns
