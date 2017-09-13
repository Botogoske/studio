import importlib
import shutil
import pickle
import os
import logging
import sys

from studio import fs_tracker

logging.basicConfig()
logger = logging.getLogger('completion_service_client')
try:
    logger.setLevel(int(sys.argv[1]))
except BaseException:
    logger.setLevel(10)


def main():
    logger.debug('copying and importing client module')

    script_path = fs_tracker.get_artifact('clientscript')
    logger.debug("Script path: " + script_path)

    mypath = os.path.dirname(script_path)
    module_name = os.path.splitext(os.path.basename(script_path))[0]

    client_module = importlib.import_module(module_name)
    logger.debug('loading args')
    with open(fs_tracker.get_artifact('args')) as f:
        args = pickle.loads(f.read())

    logger.debug('getting file mappings')
    artifacts = fs_tracker.get_artifacts()

    logger.debug('calling client funciton')
    retval = client_module.clientFunction(args, artifacts)

    logger.debug('saving the return value')
    with open(fs_tracker.get_artifact('retval'), 'w') as f:
        f.write(pickle.dumps(retval))


if __name__ == "__main__":
    main()
