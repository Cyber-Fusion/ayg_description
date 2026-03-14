from setuptools import find_packages, setup

package_name = 'ayg_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Davide De Benedittis, Daniel Kurghinyan, Suren Atoyan',
    maintainer_email='davide.debenedittis@gmail.com, daniel.kurghinyan@gmail.com, contact@surenatoyan.com',
    description='Ayg description package',
    license='BSD-3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
