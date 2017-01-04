"""Database initialization script."""

import os
import sys
import transaction
import faker

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models import Profile


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    fake = faker.Faker()

    profile = [Profile(
        name=fake.name(),
        favorite_food=fake.food(),
        date=fake.date_object(),
        description=fake.text(100),
    ) for i in range(100)]

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        dbsession.add(profile)
