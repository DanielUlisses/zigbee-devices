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
      manufacturerName: '_TZE600_vmpjkfkc\u0000',
    },
  ],
  model: 'TS000F_cover_with_2_switch_hybrid',
  vendor: 'Tuya',
  description: 'Hibrid Curtain/blind switch with 2 Gang switch"',
  options: [exposes.options.invert_cover()],
  extend: [
    tuya.modernExtend.tuyaBase({
      dp: true,
    }),
  ],
  exposes: [
    e.cover_position().setAccess("position", ea.STATE_SET),
    e.enum("calibration", ea.STATE_SET, ["START", "END"]).withDescription("Calibration"),
    e.enum("motor_steering", ea.STATE_SET, ["FORWARD", "BACKWARD"]).withDescription("Motor Steering"),
    e.numeric("quick_calibration", ea.STATE_SET).withValueMin(0).withValueMax(900).withUnit("s").withDescription("Set quick calibration"),
  ],
  endpoint: (device) => {
    return { l1: 1, l2: 1 };
  },
  meta: {
    multiEndpoint: true,
    tuyaDatapoints: [
      [
        1,
        "state",
        tuya.valueConverterBasic.lookup({
          OPEN: tuya.enum(0),
          STOP: tuya.enum(1),
          CLOSE: tuya.enum(2),
        }),
      ],
      [2, 'position', tuya.valueConverter.divideBy10],
      [
        3,
        "calibration",
        tuya.valueConverterBasic.lookup({
          START: tuya.enum(0),
          END: tuya.enum(1),
        }),
      ],
      [
        8,
        "motor_steering",
        tuya.valueConverterBasic.lookup({
          FORWARD: tuya.enum(0),
          BACKWARD: tuya.enum(1),
        }),
      ],
      [10, "quick_calibration", tuya.valueConverter.raw],
      [14, 'switch_type', tuya.valueConverterBasic.lookup({ '0': 'curtain', '1': 'switch' })],
    ],
  },
};

module.exports = definition;