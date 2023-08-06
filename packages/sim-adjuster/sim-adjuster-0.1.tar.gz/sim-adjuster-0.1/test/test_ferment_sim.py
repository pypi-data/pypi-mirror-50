"""
Basic tests for the ferment endpoints
"""

import pytest

from sim_adjuster import ferment_sim


async def response(request):
    retv = await request
    assert retv.status == 200
    return await retv.json()


@pytest.fixture
async def app(app):
    ferment_sim.setup(app)
    return app


async def test_ferment_heat(app, client):
    ferment_args = {'heater_active': True, 'cooler_active': False}

    res = await response(client.post('/ferment/run', json=ferment_args))
    heater = res['heater_temp']
    wall = res['wall_temp']
    air = res['air_temp']
    beer = res['beer_temp']
    assert heater > 20
    assert wall == pytest.approx(20)
    assert air == pytest.approx(20)
    assert beer == pytest.approx(20)

    res = await response(client.post('/ferment/run', json=ferment_args))
    assert res['heater_temp'] > heater
    assert res['air_temp'] > air  # air is warmed by heater
    assert res['beer_temp'] == pytest.approx(beer)  # beer is warmed by air

    res = await response(client.post('/ferment/run', json=ferment_args))
    assert res['air_temp'] > air
    assert res['beer_temp'] > beer


async def test_ferment_cool(app, client):
    ferment_args = {'heater_active': False, 'cooler_active': True}

    res = await response(client.post('/ferment/reset'))
    heater = res['heater_temp']
    wall = res['wall_temp']
    air = res['air_temp']
    beer = res['beer_temp']
    assert heater == pytest.approx(20)
    assert wall == pytest.approx(20)
    assert air == pytest.approx(20)
    assert beer == pytest.approx(20)

    res = await response(client.post('/ferment/run', json=ferment_args))
    assert res['heater_temp'] == pytest.approx(heater)
    assert res['wall_temp'] < wall
    assert res['air_temp'] == pytest.approx(air)
    assert res['beer_temp'] == pytest.approx(beer)

    res = await response(client.post('/ferment/run', json=ferment_args))
    assert res['heater_temp'] == pytest.approx(heater)
    assert res['wall_temp'] < wall
    assert res['air_temp'] < air
    assert res['beer_temp'] == pytest.approx(beer)

    res = await response(client.post('/ferment/run', json=ferment_args))
    assert res['heater_temp'] == pytest.approx(heater)
    assert res['wall_temp'] < wall
    assert res['air_temp'] < air
    assert res['beer_temp'] < beer
