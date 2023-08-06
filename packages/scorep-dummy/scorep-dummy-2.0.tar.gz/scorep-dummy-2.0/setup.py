from distutils.core import setup

setup(
    name='scorep-dummy',
    version='2.0',
    description='This is a dummy package for the scorep pakcage',
    author='Andreas Gocht',
    author_email='andreas.gocht@tu-dresden.de',
    url='https://github.com/score-p/scorep_binding_python_dummy',
    long_description='''
This package only provides the user interface of the Score-P Python tracing.
The goal is to allow the presence of userinstrumentation in packages even if no Score-P is present.
''',
    packages=['scorep', 'scorep.instrumenters']
)
