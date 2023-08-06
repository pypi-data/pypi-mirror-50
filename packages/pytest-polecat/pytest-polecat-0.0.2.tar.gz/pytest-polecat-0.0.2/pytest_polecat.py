# -*- coding: utf-8 -*-

import copy

import pytest
from polecat.core.config import RootConfig, default_config
from polecat.model import Blueprint, default_blueprint
from polecat.test import fixture


@pytest.fixture
def server():
    with fixture.server() as f:
        yield f


@pytest.fixture
def immutabledb():
    with fixture.immutabledb() as f:
        yield f


@pytest.fixture
def testdb():
    with fixture.testdb() as f:
        yield f


@pytest.fixture(scope='session')
def migrateddb():
    with fixture.migrateddb() as f:
        yield f


@pytest.fixture
def db(migrateddb):
    with fixture.db(migrateddb) as f:
        yield f


@pytest.fixture(scope='session')
def factory():
    with fixture.factory() as f:
        yield f


@pytest.fixture
def push_blueprint():
    old_bp = default_blueprint.get_target()
    try:
        bp = copy.deepcopy(old_bp)
        default_blueprint.set_target(bp)
        yield bp
    finally:
        default_blueprint.set_target(old_bp)


@pytest.fixture
def push_config():
    old_cfg = default_config.get_target()
    try:
        cfg = RootConfig(prefix='POLECAT')
        default_config.set_target(cfg)
        yield cfg
    finally:
        default_config.set_target(old_cfg)
