"""
Fermenter simulation
"""

from aiohttp import web
from brewblox_service import brewblox_logger, features

LOGGER = brewblox_logger(__name__)
routes = web.RouteTableDef()


def setup(app: web.Application):
    features.add(app, FermentAdjuster(app))
    app.router.add_routes(routes)


class FermentAdjuster(features.ServiceFeature):

    def __init__(self, app: web.Application):
        super().__init__(app)
        self.reset()

        # heat capacity water * density of water * 20L volume (in kJ per kelvin).
        self.beer_capacity = 4.2 * 1.0 * 20

        # heat capacity of dry air * density of air * 200L volume (in kJ per kelvin).
        # Moist air has only slightly higher heat capacity, 1.02 when saturated at 20C.
        self.air_capacity = 1.005 * 1.225 * 0.200

        # just a guess
        self.wall_capacity = 5.0

        # also a guess, to simulate that heater first heats itself, then starts heating the air
        self.heater_capacity = 1.0

        # 100W, in kW.
        self.heater_power = 0.1

        # 100W, in kW. Assuming 200W at 50% efficiency
        self.cooler_power = 0.1

        self.air_beer_transfer = 1.0/300
        self.wall_air_transfer = 1.0/300
        self.heater_air_transfer = 1.0/30
        self.env_wall_transfer = 0.001  # losses to environment

        self.heater_to_beer = 0.0  # ratio of heater transferred directly to beer instead of fridge air
        self.heater_to_air = 1.0 - self.heater_to_beer

    @property
    def temps(self):
        return dict(
            air_temp=self.air_temp,
            beer_temp=self.beer_temp,
            wall_temp=self.wall_temp,
            heater_temp=self.heater_temp,
        )

    async def startup(self, _):
        ...

    async def shutdown(self, _):
        ...

    def reset(self):
        self.beer_temp = 20.0
        self.air_temp = 20.0
        self.wall_temp = 20.0
        self.env_temp = 20.0
        self.heater_temp = 20.0

    def run(self, heater_active, cooler_active):
        beer_temp_new = self.beer_temp
        air_temp_new = self.air_temp
        wall_temp_new = self.wall_temp
        heater_temp_new = self.heater_temp

        if heater_active:
            heater_temp_new += self.heater_power / self.heater_capacity

        if cooler_active:
            wall_temp_new -= self.cooler_power / self.wall_capacity

        air_temp_new += (self.heater_temp - self.air_temp) * self.heater_air_transfer / self.air_capacity
        air_temp_new += (self.wall_temp - self.air_temp) * self.wall_air_transfer / self.air_capacity
        air_temp_new += (self.beer_temp - self.air_temp) * self.air_beer_transfer / self.air_capacity

        beer_temp_new += (self.air_temp - self.beer_temp) * self.air_beer_transfer / self.beer_capacity

        heater_temp_new += (self.air_temp - self.heater_temp) * self.heater_air_transfer / self.heater_capacity

        wall_temp_new += (self.env_temp - self.wall_temp) * self.env_wall_transfer / self.wall_capacity

        self.air_temp = air_temp_new
        self.beer_temp = beer_temp_new
        self.wall_temp = wall_temp_new
        self.heater_temp = heater_temp_new


@routes.post('/ferment/reset')
async def ferment_reset(request: web.Request) -> web.Response:
    """
    ---
    summary: Reset ferment temperatures
    tags:
        - Adjuster
    operationId: ferment.reset
    produces:
    - application/json
    """
    adjuster = features.get(request.app, FermentAdjuster)
    adjuster.reset()
    return web.json_response(adjuster.temps)


@routes.post('/ferment/run')
async def ferment_run(request: web.Request) -> web.Response:
    """
    ---
    summary: Run fermentation adjustments
    tags:
        - Adjuster
    operationId: ferment.run
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
                heater_active:
                    type: boolean
                cooler_active:
                    type: boolean
    """
    args = await request.json()
    adjuster = features.get(request.app, FermentAdjuster)
    adjuster.run(args['heater_active'], args['cooler_active'])
    return web.json_response(adjuster.temps)
