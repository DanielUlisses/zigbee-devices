# Switch Energy Statistics Estimation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/releases)
[![GitHub stars](https://img.shields.io/github/stars/danielulisses/zigbee-devices.svg?style=for-the-badge)](https://github.com/danielulisses/zigbee-devices/stargazers)

A Home Assistant custom integration for tracking energy consumption of multi-gang switches (1-8 gangs) with estimated power consumption.

## Quick Start with HACS

1. **Add to HACS**: Add `https://github.com/danielulisses/zigbee-devices` as a custom repository in HACS
2. **Install**: Search for "Switch Energy Statistics Estimation" and install
3. **Configure**: Add the integration and configure your switch and power settings
4. **Monitor**: View your energy data in Home Assistant's Energy Dashboard

## Features

- 🔌 **Multi-gang Support**: 1-8 gang switches
- ⚡ **Flexible Power Settings**: Individual power configuration per gang
- 📊 **Multiple Time Periods**: Daily, weekly, and monthly tracking
- 🏠 **Energy Dashboard**: Full integration with HA Energy Dashboard
- 💾 **Data Persistence**: Historical data survives restarts
- 🛠️ **Management Services**: Reset, export, and modify energy data
- 🎛️ **Easy Configuration**: Simple UI setup through integrations

## Supported Devices

- Multi-gang wall switches (Sonoff 4CH, etc.)
- Smart switches with multiple channels
- Light entities used as switches
- Any Home Assistant switch/light entity

---

**For complete documentation, installation instructions, and examples, see the [full README](custom_components/switch_energy_statistics_estimation/README.md).**