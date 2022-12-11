from setuptools import setup

package_name = 'self_drive'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Hojunkim',
    author_email='rlaghwns711@naver.com',
    maintainer='Hojunkim',
    maintainer_email='rlaghwns711@naver.com',
    description='ROS 2 package to self-drive turtlebot',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            f'self_drive = {package_name}.self_drive:main',
        ],
    },
)
