#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS
    # e.g. brew install pyenv-virtualenv
    brew install python

    case "${TOXENV}" in
        py37)
            # Install some custom Python 3.7 requirements on macOS
            ;;
        py38)
            # Install some custom Python 3.8 requirements on macOS
            ;;
    esac
else
    # Install some custom requirements on Linux
    :
fi
