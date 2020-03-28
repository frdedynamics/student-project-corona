#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ] || [ $TRAVIS_OS_NAME = 'windows' ]; then

    # Install some custom requirements on macOS
    # e.g. brew install pyenv-virtualenv
    python3 -V
    pip3 -V
    pip3 install -r ./requirements.txt

else
    # Install some custom requirements on Linux
    pip install -r ./requirements.txt
fi
