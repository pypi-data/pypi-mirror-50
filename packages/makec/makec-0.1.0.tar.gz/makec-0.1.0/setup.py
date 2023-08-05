from setuptools import setup
setup(
    author="Ahmed Garawani",
    author_email="ahgarawani@gmail.com",
    name = 'makec',
    python_requires=">=3.6",
    version = '0.1.0',
    url = 'https://github.com/ahgarawani/makec.git',
    packages = ['makec'],
    entry_points = {
        'console_scripts': [
            'makec = makec.__main__:main'
        ]
    })
