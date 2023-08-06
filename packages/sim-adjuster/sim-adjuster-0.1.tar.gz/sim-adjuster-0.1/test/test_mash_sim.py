"""
Basic tests for the mash endpoints
"""

import pytest

from sim_adjuster import mash_sim


async def response(request):
    retv = await request
    assert retv.status == 200
    return await retv.json()


@pytest.fixture
async def app(app):
    mash_sim.setup(app)
    return app


async def test_mash(app, client):
    ferment_args = {'heater_value': 100, 'mash_pumping': True}

    res = await response(client.post('/mash/run', json=ferment_args))
    hlt = res['hlt_temp']
    assert hlt > 60  # heating

    res = await response(client.post('/mash/run', json=ferment_args))
    assert res['hlt_temp'] > hlt
