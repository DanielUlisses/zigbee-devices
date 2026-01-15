# Zigbee Device Converters

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/releases)
[![GitHub stars](https://img.shields.io/github/stars/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/stargazers)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

Custom Zigbee device converters for Zigbee2MQTT, focused on specialized Tuya multi-gang switches and relay modules.

## 📦 What's Included

### 🔄 Zigbee Device Converters
> **Extend Zigbee2MQTT support for specialized devices**

| Device Type | Purpose | Compatibility |
|-------------|---------|---------------|
| 🔌 **2-Gang Switch** | Tuya switches without neutral wire | Zigbee2MQTT |
| ⚡ **Multi-Gang Relays** | Various gang configurations | Modern converter format |
| 🏠 **No-Neutral Support** | Specialized wiring configurations | Latest Z2M architecture |

**Perfect for**: Zigbee2MQTT users, Tuya device integration, custom device support

## ✨ Key Features

### 🔄 Modern Zigbee2MQTT Converters
- ✅ **Tuya Multi-Gang Switches**: Support for switches without neutral wire
- ✅ **2-Gang Switch Support**: Specialized converters for 2-gang modules  
- ✅ **No-Neutral Compatibility**: Works with switches that don't require neutral
- ✅ **Modern Converter Format**: Uses latest Zigbee2MQTT converter architecture
- ✅ **Device Fingerprints**: Proper device identification patterns
- ✅ **Endpoint Mapping**: Multi-endpoint switch configurations

## 🚀 Installation

### Zigbee2MQTT Converters

1. **Locate your Zigbee2MQTT data directory**:
   ```bash
   # Common locations:
   /opt/zigbee2mqtt/data/
   /config/zigbee2mqtt/
   ```

2. **Copy converter files**:
   ```bash
   # Download converters
   wget https://github.com/danielulisses/zigbee-devices/raw/main/relay-2-types/2-gang-switch-converter.mjs
   
   # Copy to Zigbee2MQTT directory
   cp *.mjs /path/to/zigbee2mqtt/data/
   ```

3. **Restart Zigbee2MQTT**:
   ```bash
   # Docker
   docker restart zigbee2mqtt
   
   # Home Assistant Add-on
   # Restart via Supervisor
   ```

4. **Verify Installation**:
   - Check Zigbee2MQTT logs for converter loading
   - Devices should now be recognized with proper capabilities

## 🔧 Development

### Converter Development
```bash
# Test converter syntax
node -c relay-2-types/2-gang-switch-converter.mjs

# Validate structure
zigbee2mqtt --help # Check if converters load
```

### Adding New Devices
1. **Identify Device**: Get modelID and manufacturerName from Zigbee2MQTT logs
2. **Create Converter**: Use existing converters as templates
3. **Test**: Verify device recognition and functionality
4. **Contribute**: Submit PR with new converter

## 💬 Support & Community

### 🔗 Related Repositories

For Home Assistant custom integrations, check out our separate repositories:
- 🔌 **[Switch Energy Statistics Estimation](https://github.com/danielulisses/switch-energy-statistics-estimation)** - Multi-gang switch energy tracking
- ⚡ **[Energy Generation Report](https://github.com/danielulisses/energy-generation-report)** - Solar generation reporting with interactive charts

### 🐛 Issues & Bug Reports
Found a bug with a converter? Have a device request? 
[🔗 Open an Issue](https://github.com/danielulisses/zigbee-devices/issues/new)

### 💡 Device Requests  
Need support for a new Zigbee device? 
[💭 Request Device Support](https://github.com/danielulisses/zigbee-devices/discussions)

### ⭐ Show Support
If these converters are helpful, please:
- ⭐ **Star this repository**
- 🍴 **Share with the Zigbee2MQTT community** 
- 💝 **Contribute new device converters**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Made with ❤️ for the Zigbee2MQTT community**

## 🔧 Supported Devices

### Tuya 2-Gang Switch (No Neutral)
- **Model**: TS000F_2_gang_switch
- **Manufacturer**: _TZ3000_pe6rtun6
- **Features**: 2 independent switch endpoints, power-on behavior control
- **Converter**: [2-gang-switch-converter.mjs](relay-2-types/2-gang-switch-converter.mjs)

### Alternative 2-Gang Implementation  
- **Converter**: [2type-switch-converter.mjs](relay-2-types/2type-switch-converter.mjs)
- **Use Case**: Alternative implementation for compatibility testing

## 📚 Documentation

### Converter Structure
```javascript
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
        e.power_on_behavior().withAccess(ea.STATE_SET),
    ],
    extend: [tuya.modernExtend.tuyaBase({dp: true})],
    meta: {
        multiEndpoint: true,
        multiEndpointSkip: ["power_on_behavior"],
        tuyaDatapoints: [
            [1, "state_l1", tuya.valueConverter.onOff],
            [2, "state_l2", tuya.valueConverter.onOff],
            [14, "power_on_behavior", tuya.valueConverter.powerOnBehavior],
        ],
    },
};
```

### Device Identification
1. **Check Zigbee2MQTT logs** for unrecognized devices
2. **Note the modelID and manufacturerName** from the logs
3. **Test with existing converters** or create new ones
4. **Submit feedback** for device compatibility

## � Development & Contributing

This repository uses a comprehensive development workflow with automated formatting and quality checks.

### Quick Development Setup
```bash
# One-command setup
make setup

# View all available commands
make help

# Format and validate your code
make format lint

# Check if ready for commit
make commit-check
```

### Development Standards
- **Code Formatting**: Black (88 character line length)
- **Import Sorting**: isort (black profile)
- **YAML Linting**: yamllint with relaxed line length
- **Pre-commit Hooks**: Automated validation on commit
- **Component Versioning**: Independent semantic versioning per component

### Architecture Overview
```
zigbee-devices/
├── custom_components/           # Home Assistant integrations
│   ├── switch_energy_statistics_estimation/
│   └── energy_generation_report/
├── relay-2-types/              # Zigbee2MQTT converters
├── .github/workflows/          # CI/CD automation
│   ├── release.yml            # Component-specific releases
│   └── pr-validation.yml      # Code quality validation
├── DEVELOPMENT.md             # Detailed development guide
└── pyproject.toml            # Python project configuration
```

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the established patterns
4. Test with: `make commit-check`
5. Submit a pull request

📖 **Detailed Development Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)

## � Support & Community

### 🐛 Issues & Bug Reports
Found a bug? Have a feature request?
[🔗 Open an Issue](https://github.com/danielulisses/zigbee-devices/issues/new)

### 💡 Feature Requests
We welcome suggestions for new features or improvements!
[💭 Suggest a Feature](https://github.com/danielulisses/zigbee-devices/discussions)

### 📚 Documentation
- **Component Docs**: Each component has detailed README files
- **Development Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)
- **Example Configurations**: Check component `/examples.md` files

### 🏷️ Releases & Versioning
This repository uses component-specific versioning:
- **Format**: `component_name-v1.2.3`
- **Individual Releases**: Each component releases independently
- **HACS Integration**: Automatic component detection via release filters

### ⭐ Show Support
If these integrations are helpful, please:
- ⭐ **Star this repository**
- 🍴 **Share with the community**
- 💝 **Contribute improvements**

---

## 📄 License

This project is licensed under the MIT License - see individual component documentation for specific details.

**Made with ❤️ for the Home Assistant community**
