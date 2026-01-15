# HACS Multi-Component Repository

This repository contains multiple Home Assistant custom integrations:

## Components Available

### 🔌 Switch Energy Statistics Estimation
Track energy consumption for multi-gang switches (1-8 gangs) with historical data.

**HACS Installation:**
1. Go to HACS → Integrations  
2. Click ⋮ → Custom repositories
3. Add: `https://github.com/danielulisses/zigbee-devices`
4. Category: Integration
5. Search for "Switch Energy Statistics Estimation"

### ⚡ Energy Generation Report  
Solar energy reporting with billing period management and cumulative balance tracking.

**HACS Installation:**
1. Go to HACS → Integrations
2. Click ⋮ → Custom repositories  
3. Add: `https://github.com/danielulisses/zigbee-devices`
4. Category: Integration
5. Search for "Energy Generation Report"

## Repository Structure

```
custom_components/
├── switch_energy_statistics_estimation/    # Switch Energy Component
│   ├── hacs.json                          # HACS config for switch component
│   └── ...
└── energy_generation_report/              # Energy Report Component  
    ├── hacs.json                          # HACS config for energy component
    └── ...
```

Each component has its own:
- Version tracking via component-specific tags (`switch-stats-v*`, `energy-report-v*`)
- Release artifacts (separate ZIP files)
- HACS configuration with release filters
- Documentation and examples

## Installation Methods

### Via HACS (Recommended)
Add this repository as a custom HACS integration. Each component will appear separately in the HACS interface with proper version tracking.

### Manual Installation  
Download the component-specific ZIP file from the [Releases](https://github.com/danielulisses/zigbee-devices/releases) page and extract to your `custom_components/` directory.