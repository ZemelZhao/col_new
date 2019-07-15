
def configuration(parent_package='', top_path=None):
    """DocString for configuration"""
    #@todo: to be defined.
    #:parent_package='': @todo.
    #:top_path=None: @todo.
    from numpy.distutils.misc_util import Configuration
    config = Configuration('filter', parent_package, top_path)
    config.add_extension('_filter', sources=['filter.cpp'])

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
