from setuptools import find_packages, setup

package_name = "inspection_station"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/inspection_station.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="pro-ish",
    maintainer_email="ishani13715@gmail.com",
    description="ROS 2 inspection station learning project.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "camera_node = inspection_station.camera_node:main",
            "plc_node = inspection_station.plc_node:main",
            "conveyor_node = inspection_station.conveyor_node:main",
            "logger_node = inspection_station.logger_node:main",
        ],
    },
)
