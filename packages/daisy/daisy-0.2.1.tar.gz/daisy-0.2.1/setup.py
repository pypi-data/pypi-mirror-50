from setuptools import setup

setup(
        name='daisy',
        version='0.2.1',
        description='Block-wise task scheduler for large nD volumes.',
        url='https://daisy-docs.readthedocs.io',
        author='Jan Funke',
        author_email='funkej@janelia.hhmi.org',
        license='MIT',
        packages=[
            'daisy',
            'daisy.ext',
            'daisy.persistence'
        ],
        install_requires=[
            "numpy",
            "tornado>=5,<6",
            "networkx",
            "pymongo"
        ]
)
