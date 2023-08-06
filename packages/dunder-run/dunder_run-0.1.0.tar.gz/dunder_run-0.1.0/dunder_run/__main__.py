import argparse
import inspect
from importlib import util
from pathlib import Path
import sys


def main():
    path_to_file = Path('.') / sys.argv[1]
    spec = util.spec_from_file_location('__run__', path_to_file)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entrypoint_function = module.__run__


    signature = inspect.signature(entrypoint_function)
    parameters = signature.parameters.values()

    sys.argv.pop(0)

    parser = argparse.ArgumentParser(description=entrypoint_function.__doc__)
    for parameter in parameters:
        annotation = getattr(parameter, 'annotation', str)

        if annotation is bool:
            parameter_name = f'--{parameter.name}'
            kw_options = {
                'action': 'store_const',
                'const': True,
            }
        else:
            parameter_name = parameter.name
            kw_options = {'type': annotation}

        parser.add_argument(parameter_name, **kw_options)

    args = vars(parser.parse_args())

    entrypoint_function(**args)


if __name__ == '__main__':
    main()
