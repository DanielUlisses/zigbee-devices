# Repository Architecture & AI Agent Instructions

## Repository Overview

This repository contains Home Assistant custom components and Zigbee device converters for energy management and smart home automation.

### Repository Structure
```
zigbee-devices/
├── custom_components/              # Home Assistant custom integrations
│   ├── switch_energy_statistics_estimation/  # Energy tracking for multi-gang switches
│   └── energy_generation_report/   # Solar energy generation reporting
├── relay-2-types/                  # Zigbee device converters for Zigbee2MQTT
│   ├── 2-gang-switch-converter.mjs # 2-gang switch without neutral
│   └── 2type-switch-converter.mjs  # Alternative 2-gang implementation
├── .github/                        # GitHub Actions workflows & templates
│   ├── workflows/                  # CI/CD automation
│   └── instructions/               # AI agent guidance
├── DEVELOPMENT.md                  # Development environment setup
├── README.md                       # Project documentation
└── pyproject.toml                  # Python project configuration
```

## Component Architecture

### Switch Energy Statistics Estimation
- **Purpose**: Track energy consumption for multi-gang switches (1-8 gangs)
- **Technology Stack**: Home Assistant Custom Integration, Python 3.9+
- **Key Features**: Energy dashboard integration, configurable power per gang, historical tracking
- **Dependencies**: Home Assistant Core 2024.1+

### Energy Generation Report
- **Purpose**: Solar energy generation reporting with billing period management
- **Technology Stack**: Home Assistant Custom Integration, ApexCharts
- **Key Features**: Grid consumption tracking, interactive charts, service integration
- **Dependencies**: Home Assistant Core 2024.1+, ApexCharts Card

### Zigbee Device Converters
- **Purpose**: Custom device definitions for Zigbee2MQTT
- **Technology Stack**: JavaScript (Node.js), Zigbee Herdsman Converters
- **Target Devices**: Tuya multi-gang switches without neutral wire
- **Integration Point**: Zigbee2MQTT external converters

## Development Workflow

### Code Quality Standards
- **Formatter**: Black (88 character line length)
- **Import Sorting**: isort (black profile)
- **YAML Linting**: yamllint with relaxed line length (200 chars)
- **Pre-commit Hooks**: Automated formatting and validation

### Build & Release Process
- **Component Versioning**: Individual manifest.json versions
- **Release Strategy**: Component-specific GitHub releases with proper tags
- **HACS Integration**: Multi-component repository with release filters
- **CI/CD**: GitHub Actions for PR validation and automated releases

## AI Agent Guidance

### Context Understanding
When working with this repository, understand that:

1. **Multi-Component Nature**: This is a collection of independent Home Assistant components, each with its own versioning and release cycle
2. **Energy Focus**: Primary domain is energy management and consumption tracking
3. **Zigbee Integration**: Includes both Home Assistant integrations and Zigbee2MQTT converters
4. **Developer-Friendly**: Comprehensive tooling for development workflow automation

### Code Patterns to Recognize

#### Home Assistant Integration Patterns
```python
# Standard integration entry point
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from a config entry."""

# Entity pattern with unique_id and device_info
class EnergyEstimationSensor(SensorEntity):
    def __init__(self, config_entry, description):
        self._attr_unique_id = f"{config_entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(...)
```

#### Configuration Flow Patterns
```python
# Multi-step configuration with validation
class SwitchEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        # Handle gang count selection and power configuration
```

### File Naming Conventions
- **Components**: snake_case directory names
- **Python Files**: snake_case.py
- **Configuration**: lowercase with hyphens (e.g., .pre-commit-config.yaml)
- **Documentation**: UPPERCASE.md for root level, README.md for component docs

### Common Operations

#### Version Management
- Components use semantic versioning in manifest.json
- Release workflow creates component-specific tags (e.g., switch_energy_statistics_estimation-v1.2.3)
- HACS uses release_filter to detect component updates

#### Development Commands
```bash
make setup          # Initialize development environment
make format lint    # Format and check code quality
make commit-check   # Validate changes before commit
make help          # Show all available commands
```

### Testing Strategy
- **Manual Testing**: Use development environment with make commands
- **CI Validation**: GitHub Actions for structure validation and code quality
- **Integration Testing**: Test in Home Assistant development environment
- **Device Testing**: Physical Zigbee devices for converter validation

## Component-Specific Context

### Switch Energy Statistics Estimation
- **Entity Types**: Sensor entities for energy tracking
- **State Management**: Uses hass.data for persistent storage
- **Configuration**: Multi-step flow for gang count and power settings
- **Services**: Custom services for data management and export
- **Energy Integration**: Compatible with HA Energy Dashboard

### Energy Generation Report
- **Chart Integration**: ApexCharts for visualization
- **Billing Periods**: Flexible billing cycle management
- **Data Entry**: Service-based data input system
- **Export Features**: Data export capabilities

### Zigbee Converters
- **Device Fingerprints**: Tuya device identification patterns
- **Endpoint Mapping**: Multi-endpoint switch configurations
- **Datapoint Mapping**: Tuya-specific datapoint translations
- **Converter Structure**: Modern Zigbee2MQTT converter format

This documentation provides comprehensive context for AI agents to understand the repository structure, development patterns, and component relationships for more effective assistance.
