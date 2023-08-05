from setuptools import setup

setup(
        name='flask-xd',
        author='Xzavier Dunn',
        description='Setup a flask template with or without auth/user services',
        packages=['app'],
        license='MIT',
        download_url='https://github.com/XzavierDunn/flask-templates/archive/v1.0.tar.gz',
        install_requires=[
            'Click'
        ],
        version='v1.0',
        entry_points={
            'console_scripts': [
                'flasksetup=app.main:install',
            ]
        }
    )
