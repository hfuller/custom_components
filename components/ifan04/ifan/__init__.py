import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan, output
from esphome.const import (
    CONF_OUTPUT,
    CONF_DIRECTION_OUTPUT,
    CONF_OUTPUT_ID,
    CONF_SPEED,
    CONF_SPEED_COUNT,
)
from .. import ifan_ns

IFan = ifan_ns.class_("IFan", cg.Component, fan.Fan)

CONFIG_SCHEMA = fan.FAN_SCHEMA.extend(
    {
        cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(IFan),
        cv.Required(CONF_OUTPUT): cv.use_id(output.FloatOutput),
        cv.Optional(CONF_DIRECTION_OUTPUT): cv.use_id(output.BinaryOutput),
        cv.Optional(CONF_SPEED): cv.invalid(
            "Configuring individual speeds is deprecated."
        ),
        cv.Optional(CONF_SPEED_COUNT, 3): cv.int_range(min=1),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    output_ = await cg.get_variable(config[CONF_OUTPUT])
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID], output_, config[CONF_SPEED_COUNT])
    await cg.register_component(var, config)
    await fan.register_fan(var, config)

    if CONF_DIRECTION_OUTPUT in config:
        direction_output = await cg.get_variable(config[CONF_DIRECTION_OUTPUT])
        cg.add(var.set_direction(direction_output))
