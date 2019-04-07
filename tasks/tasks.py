from invoke import Collection

from tasks import clean
from tasks import check
from tasks import setup
from tasks import start


namespace = Collection()

namespace.add_collection(setup.setup, 'setup')
namespace.add_task(setup.install_dependencies, 'install')
namespace.add_task(setup.migrate_db, 'migrate')

namespace.add_collection(check.check, 'check')
namespace.add_task(check.lint, 'lint')
namespace.add_task(check.tests, 'test')

namespace.add_collection(start.start, 'start')
namespace.add_task(start.django_shell, 'shell')

namespace.add_collection(clean.clean, 'clean')
