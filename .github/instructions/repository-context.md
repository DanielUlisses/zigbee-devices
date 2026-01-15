# Repository Architecture & AI Agent Instructions

## Repository Overview

This repository contains Zigbee device converters for Zigbee2MQTT, focused on specialized Tuya devices and multi-gang switches.

### Repository Structure
```
zigbee-devices/
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

### Zigbee Device Converters
- **Purpose**: Custom device definitions for Zigbee2MQTT
- **Technology Stack**: JavaScript (Node.js), Zigbee Herdsman Converters
- **Target Devices**: Tuya multi-gang switches without neutral wire
- **Integration Point**: Zigbee2MQTT external converters

## Related Repositories

### Separate Home Assistant Integrations
This repository was split from a multi-component structure. The Home Assistant custom components are now in separate repositories:

- **[Switch Energy Statistics Estimation](https://github.com/danielulisses/switch-energy-statistics-estimation)**: Multi-gang switch energy tracking
- **[Energy Generation Report](https://github.com/danielulisses/energy-generation-report)**: Solar generation reporting with interactive charts

## Development Workflow

### Code Quality Standards
- **Formatter**: Black (88 character line length) - for any Python utilities
- **YAML Linting**: yamllint with relaxed line length (200 chars)
- **JavaScript**: Modern ESM format for converters

### Build & Release Process
- **Converter Versioning**: Git tags for converter updates
- **Release Strategy**: GitHub releases for converter collections
- **Integration Point**: Direct file copying to Zigbee2MQTT

## AI Agent Guidance

### Context Understanding
When working with this repository, understand that:

1. **Zigbee Focus**: Primary focus is Zigbee2MQTT device converters
2. **Tuya Specialization**: Specialized support for Tuya devices without neutral wire
3. **Modern Architecture**: Uses latest Zigbee2MQTT converter patterns
4. **Separated Components**: Home Assistant integrations moved to separate repositories

### Code Patterns to Recognize

#### Zigbee2MQTT Converter Patterns
```javascript
// Standard converter definition
const definition = {
    fingerprint: [{
        modelID: 'TS000F',
        manufacturerName: '_TZ3000_pe6rtun6',
    }],
    model: 'TS000F_2_gang_switch', 
    vendor: 'Tuya',
    description: '2 gang switch module without neutral wire',
    exposes: [
        e.switch().withEndpoint("l1").setAccess("state", ea.STATE_SET),
        e.switch().withEndpoint("l2").setAccess("state", ea.STATE_SET),
    ],
    extend: [tuya.modernExtend.tuyaBase({dp: true})],
    meta: {
        multiEndpoint: true,
        tuyaDatapoints: [
            [1, "state_l1", tuya.valueConverter.onOff],
            [2, "state_l2", tuya.valueConverter.onOff],
        ],
    },
};

module.exports = definition;
```

### File Naming Conventions
- **Converters**: kebab-case.mjs (e.g., 2-gang-switch-converter.mjs)
- **Documentation**: UPPERCASE.md for root level
- **Configuration**: lowercase with hyphens

### Common Operations

#### Device Converter Development
```bash
# Test converter syntax
node -c relay-2-types/converter-name.mjs

# Check Zigbee2MQTT logs for device recognition
tail -f /var/log/zigbee2mqtt.log
```

#### Device Identification Process
1. **Monitor Logs**: Check Zigbee2MQTT logs for unrecognized devices
2. **Extract Fingerprint**: Note modelID and manufacturerName
3. **Create Converter**: Use existing patterns as templates
4. **Test Device**: Verify endpoints and functionality work correctly

### Testing Strategy
- **Syntax Validation**: Node.js syntax checking for converters
- **Device Testing**: Physical Zigbee devices for converter validation
- **Zigbee2MQTT Integration**: Test converter loading and device recognition

## Converter-Specific Context

### Tuya Multi-Gang Switches
- **Device Fingerprints**: Tuya device identification patterns
- **Endpoint Mapping**: Multi-endpoint switch configurations
- **No-Neutral Support**: Specialized wiring configurations
- **Datapoint Mapping**: Tuya-specific datapoint translations
- **Power-On Behavior**: Control switch behavior after power loss

### Modern Converter Architecture
- **ESM Format**: Uses modern JavaScript module syntax
- **Zigbee Herdsman**: Built on latest converter framework
- **Tuya Extensions**: Modern tuya.modernExtend.tuyaBase usage
- **Endpoint Management**: Proper multi-endpoint handling

This documentation provides context for AI agents to understand the repository's specialized focus on Zigbee device converters and its relationship to the separated Home Assistant integration repositories.
