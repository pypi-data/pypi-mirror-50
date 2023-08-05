import setuptools

version = '0.0.2'

setuptools.setup(
        name='ctec_consumer2',
        version=version,
        packages=['ctec_consumer', 'ctec_consumer.models', 'ctec_consumer.dummy', 'ctec_consumer.dummy.models',
                  'ctec_consumer.gevent', 'ctec_consumer.gevent.models'],
        author='Zhouziqiang',
        author_email='zhouzq0823@163.com',
        url='http://www.189.cn',
        description='189 rabbitMQ consumer',
        install_requires=['kombu>=3.0.33', 'gevent>=1.0.1']
)
