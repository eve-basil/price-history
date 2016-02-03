from setuptools import setup, find_packages

setup(
    name="basilprices",
    version="0.1.0.dev",
    packages=find_packages(),

    description="API managing Eve Online prices.",
    install_requires=["Cython==0.23.4",
                      "falcon==0.3.0",
                      "gevent==1.0.2",
                      "gunicorn==19.4.1",
                      "SQLAlchemy==1.0.10",
                      "mysql-python==1.2.5"],
)
