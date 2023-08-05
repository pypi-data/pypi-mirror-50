from setuptools import setup, find_packages


requires = [
            "flask>=1.0.0",
            "flask_cors",
            "apscheduler>=3.0.0",
            "pendulum",
            "pymysql>0.9.0"]

setup(
    name="data-service",
    version="0.0.35",
    description="support data-service api by flask",
    url="https://github.com/xiaodongxiexie/DataService",
    author="xiaodong",
    author_email="xiaodongliang@outlook.com",
    license="MIT",
    classifiers=[
    ],
    keywords="flask data api adscheduler pymysql",
    packages=find_packages("DataService"),
    package_dir={"": "DataService"},
    data_files=[("DataService/config", ["DataService/config/config.cfg"]),
                ("DataService/docs", ["DataService/docs/readme.png"]),
                ("DataService", ["DataService/README.md"])],
    include_package_data=True,
    package_data={"": ["requirements.txt", "*.png", "README.md"],
                  "config": ["*.cfg"]},
    install_requires=requires
    )
