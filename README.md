# Home Assistant Custom Components Collection

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/releases)
[![GitHub stars](https://img.shields.io/github/stars/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/stargazers)

A collection of Home Assistant custom integrations for energy management and device control.

## 🔌 Switch Energy Statistics Estimation

Track energy consumption of multi-gang switches (1-8 gangs) with estimated power consumption.

**Features:**
- Multi-gang switch support (1-8 gangs)
- Energy consumption tracking (daily, weekly, monthly)
- Home Assistant Energy Dashboard integration
- Configurable power consumption per gang
- Historical data persistence

[📖 Full Documentation](custom_components/switch_energy_statistics_estimation/README.md)

## ⚡ Energy Generation Report

Comprehensive solar energy generation reporting with interactive charts and billing period management.

**Features:**
- Solar energy tracking with flexible billing periods
- Grid consumption and injection monitoring
- Cumulative balance tracking with utility companies
- Interactive ApexCharts visualizations
- Service integration for easy data entry

[📖 Full Documentation](custom_components/energy_generation_report/README.md)

## 🚀 Installation via HACS

1. **Add Repository**: Add `https://github.com/danielulisses/zigbee-devices` as a custom repository in HACS
2. **Install**: Search for the component you want to install:
   - "Switch Energy Statistics Estimation"
   - "Energy Generation Report"
3. **Configure**: Add the integration through Settings → Devices & Services
4. **Restart**: Restart Home Assistant

## 📦 Manual Installation

1. Download the ZIP file for your desired component from the [Releases](https://github.com/danielulisses/zigbee-devices/releases) page
2. Extract to your `custom_components/` directory
3. Restart Home Assistant
4. Add the integration through Settings → Devices & Services

## 💡 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/danielulisses/zigbee-devices/issues).

## 📄 License

This project is licensed under the MIT License - see the individual component documentation for details.

## ⭐ Support

If you like these integrations, please give this repository a star! ⭐
