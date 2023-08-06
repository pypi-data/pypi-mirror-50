import os
import setuptools


class CleanCommand(setuptools.Command):
    # Custom clean command to tidy up the project root

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setuptools.setup(
    name='buzzadn',
    version='0.0.7',
    author='Buzzvil',
    author_email='ernie.kusdavletov@buzzvil.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'clean': CleanCommand,
    }
)
