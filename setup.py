import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ayg_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Davide De Benedittis, Daniel Kurghinyan, Suren Atoyan',
    maintainer_email='davide.debenedittis@gmail.com, daniel.kurghinyan@gmail.com, contact@surenatoyan.com',
    description='Ayg description package',
    license='BSD-3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mesh_server = ayg_description.mesh_server:main',
        ],
    },
)
