"""
Mash simulation
"""

from aiohttp import web
from brewblox_service import brewblox_logger, features

LOGGER = brewblox_logger(__name__)
routes = web.RouteTableDef()


def setup(app: web.Application):
    features.add(app, MashAdjuster(app))
    app.router.add_routes(routes)


class MashAdjuster(features.ServiceFeature):

    def __init__(self, app: web.Application):
        super().__init__(app)
        self.reset()

        self.env_temp = 20

        # typical for a 40 liter batch and a 45cm kettle
        self.mash_volume = 28
        self.hlt_volume = 28

        self.specific_heat = 4.2

        # heat capacity water * density of water * 20L volume (in kJ per degree C).
        self.hlt_capacity = self.specific_heat * 1 * self.hlt_volume
        self.mash_capacity = self.specific_heat * 1 * self.mash_volume

        # 3200W, in kW.
        self.hlt_heater_power = 3.2

        # ratio of temperature difference picked up in HLT coil
        self.coil_transfer = 0.6

        # 8 liter per minute, in L/s
        self.flow_rate = 8/60

        # 10W per degree
        self.kettle_env_transfer = 0.01

        # losses between mash tun and coil
        self.mash_to_coil_loss = 0.01
        self.coil_to_mash_loss = 0.01

    @property
    def vals(self):
        return dict(
            mash_temp=self.mash_temp,
            hlt_temp=self.hlt_temp,
            coil_in_temp=self.coil_in_temp,
            coil_out_temp=self.coil_out_temp,
            mash_in_temp=self.mash_in_temp,
        )

    async def startup(self, _):
        ...

    async def shutdown(self, _):
        ...

    def reset(self):
        self.mash_temp = 60.0
        self.hlt_temp = 60.0
        self.coil_in_temp = 20
        self.coil_out_temp = 20
        self.mash_in_temp = 20

    def run(self, heater_value, mash_pumping):
        mash_temp_new = self.mash_temp
        hlt_temp_new = self.hlt_temp

        if mash_pumping:
            self.coil_in_temp = self.mash_temp - (self.mash_temp - self.env_temp) * self.mash_to_coil_loss
            self.coil_out_temp = self.coil_in_temp + (self.hlt_temp - self.coil_in_temp) * self.coil_transfer
            self.mash_in_temp = self.coil_out_temp - (self.coil_out_temp - self.env_temp) * self.coil_to_mash_loss

            # coil transfer
            mash_temp_new = (self.mash_temp * (self.mash_volume - self.flow_rate) +
                             self.mash_in_temp * self.flow_rate) / self.mash_volume
            hlt_temp_new -= (self.coil_out_temp - self.coil_in_temp) * self.flow_rate / self.hlt_volume

        # heater
        hlt_temp_new += self.hlt_heater_power * heater_value / (100 * self.hlt_capacity)

        # environment loss
        mash_temp_new -= (self.mash_temp - self.env_temp) * self.kettle_env_transfer / self.mash_capacity
        hlt_temp_new -= (self.hlt_temp - self.env_temp) * self.kettle_env_transfer / self.hlt_capacity

        self.hlt_temp = hlt_temp_new
        self.mash_temp = mash_temp_new


@routes.post('/mash/reset')
async def mash_reset(request: web.Request) -> web.Response:
    """
    ---
    summary: Reset mash temperatures
    tags:
        - Adjuster
    operationId: mash.reset
    produces:
    - application/json
    """
    adjuster = features.get(request.app, MashAdjuster)
    adjuster.reset()
    return web.json_response(adjuster.vals)


@routes.post('/mash/run')
async def mash_run(request: web.Request) -> web.Response:
    """
    ---
    summary: Run mash adjustments
    tags:
        - Adjuster
    operationId: mash.run
    produces:
    - application/json
    parameters:
    -
        name: body
        in: body
        description: object
        required: true
        schema:
            type: object
            properties:
                heater_value:
                    type: number
                mash_pumping:
                    type: boolean
    """
    args = await request.json()
    adjuster = features.get(request.app, MashAdjuster)
    adjuster.run(args['heater_value'], args['mash_pumping'])
    return web.json_response(adjuster.vals)
