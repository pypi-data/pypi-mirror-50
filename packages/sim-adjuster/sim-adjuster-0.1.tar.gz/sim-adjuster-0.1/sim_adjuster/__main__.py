"""
Example of how to import and use the brewblox service
"""

from brewblox_service import brewblox_logger, scheduler, service

from sim_adjuster import ferment_sim, mash_sim

LOGGER = brewblox_logger(__name__)


def main():
    app = service.create_app(default_name='sim_adjuster')
    scheduler.setup(app)
    service.furnish(app)

    ferment_sim.setup(app)
    mash_sim.setup(app)

    # service.run() will start serving clients async
    service.run(app)


if __name__ == '__main__':
    main()
