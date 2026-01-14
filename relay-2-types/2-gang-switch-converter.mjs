const fz = require('zigbee-herdsman-converters/converters/fromZigbee');
const tz = require('zigbee-herdsman-converters/converters/toZigbee');
const exposes = require('zigbee-herdsman-converters/lib/exposes');
const reporting = require('zigbee-herdsman-converters/lib/reporting');
const modernExtend = require('zigbee-herdsman-converters/lib/modernExtend');
const e = exposes.presets;
const ea = exposes.access;
const tuya = require('zigbee-herdsman-converters/lib/tuya');

const definition = {
  fingerprint: [
    {
      modelID: 'TS000F',
      manufacturerName: '_TZ3000_pe6rtun6',
    },
  ],
  model: 'TS000F_2_gang_switch',
  vendor: 'Tuya',
  description: '2 gang switch module without neutral wire""',
  exposes: [e.switch().withEndpoint("l1").setAccess("state", ea.STATE_SET), e.switch().withEndpoint("l2").setAccess("state", ea.STATE_SET), e.power_on_behavior().withAccess(ea.STATE_SET),],
  extend: [tuya.modernExtend.tuyaBase({ dp: true })],
  meta: {
    multiEndpoint: true,
    multiEndpointSkip: ["power_on_behavior"],
    tuyaDatapoints: [
      [1, "state_l1", tuya.valueConverter.onOff],
      [2, "state_l2", tuya.valueConverter.onOff],
      [14, "power_on_behavior", tuya.valueConverter.powerOnBehavior],
    ],
  },
  endpoint: (device) => {
    return { l1: 1, l2: 1 };
  },
};

module.exports = definition;