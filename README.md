# Home Assistant Energy Management Suite

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/releases)
[![GitHub stars](https://img.shields.io/github/stars/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/stargazers)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

A comprehensive collection of Home Assistant custom integrations and Zigbee device converters focused on energy management and smart home automation.

## 📦 What's Included

| Component | Purpose | Version | Documentation |
|-----------|---------|---------|---------------|
| 🔌 **Switch Energy Statistics** | Multi-gang switch energy tracking | [![Release](https://img.shields.io/github/v/release/danielulisses/zigbee-devices?filter=switch_energy_statistics_estimation-v*&label=version)](https://github.com/danielulisses/zigbee-devices/releases) | [📖 Docs](custom_components/switch_energy_statistics_estimation/README.md) |
| ⚡ **Energy Generation Report** | Solar generation reporting | [![Release](https://img.shields.io/github/v/release/danielulisses/zigbee-devices?filter=energy_generation_report-v*&label=version)](https://github.com/danielulisses/zigbee-devices/releases) | [📖 Docs](custom_components/energy_generation_report/README.md) |
| 🔄 **Zigbee Converters** | Tuya multi-gang switch support | Latest | [📁 Converters](relay-2-types/) |

## ✨ Key Features

### 🔌 Switch Energy Statistics Estimation
> **Track energy consumption for multi-gang switches with precision**

- ✅ **Multi-Gang Support**: 1-8 gang switches with individual power configuration
- 📊 **Energy Dashboard Integration**: Native Home Assistant Energy Dashboard compatibility
- 📈 **Historical Tracking**: Daily, weekly, and monthly consumption statistics
- ⚙️ **Configurable Power**: Set different power consumption per gang
- 💾 **Data Persistence**: Survives Home Assistant restarts
- 🛠️ **Service Management**: Built-in services for data export and management

**Perfect for**: Smart switches, relay modules, multi-gang wall switches

### ⚡ Energy Generation Report
> **Comprehensive solar energy reporting with advanced visualizations**

- 🏠 **Billing Period Management**: Flexible billing cycles for utility tracking
- 📊 **Interactive Charts**: ApexCharts integration for beautiful visualizations
- ⚖️ **Grid Balance Tracking**: Monitor consumption vs generation balance
- 📤 **Data Export**: Export capabilities for external analysis
- 🔌 **Service Integration**: Easy data entry through Home Assistant services
- 📈 **Cumulative Tracking**: Long-term energy balance monitoring

**Perfect for**: Solar installations, grid-tie systems, energy monitoring

### 🔄 Zigbee Device Converters
> **Extend Zigbee2MQTT support for specialized devices**

- 🏠 **Tuya Multi-Gang Switches**: Support for switches without neutral wire
- 🔌 **2-Gang Switch Support**: Specialized converters for 2-gang modules
- ⚡ **No-Neutral Compatibility**: Works with switches that don't require neutral
- 🔧 **Modern Converter Format**: Uses latest Zigbee2MQTT converter architecture

**Perfect for**: Zigbee2MQTT users, Tuya device integration, custom device support

## 🚀 Quick Start

### Prerequisites
- Home Assistant 2024.1 or later
- HACS installed and configured
- For Zigbee converters: Zigbee2MQTT setup

### Installation Methods

#### Method 1: HACS (Recommended)
1. **Add Repository**:
   - HACS → Integrations → ⋮ → Custom repositories
   - Add: `https://github.com/danielulisses/zigbee-devices`
   - Category: Integration

2. **Install Components**:
   - Search for "Switch Energy Statistics Estimation" or "Energy Generation Report"
   - Click Install → Restart Home Assistant

3. **Configure**:
   - Settings → Devices & Services → Add Integration
   - Search for your installed component

#### Method 2: Manual Installation
```bash
# Download specific component release
wget https://github.com/danielulisses/zigbee-devices/releases/download/[component-version]/[component].zip

# Extract to custom_components directory
unzip [component].zip -d /config/custom_components/

# Restart Home Assistant
```

#### Method 3: Git Clone (Development)
```bash
git clone https://github.com/danielulisses/zigbee-devices.git
cp -r zigbee-devices/custom_components/[component] /config/custom_components/
```

### Zigbee2MQTT Converters
```bash
# Copy converter to Zigbee2MQTT
cp relay-2-types/*.mjs /zigbee2mqtt/data/
# Restart Zigbee2MQTT
```

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
