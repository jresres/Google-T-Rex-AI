#!/bin/sh

case "$1" in 
    open)
        docker run --rm --name trex -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest
        ;;
    build)
        docker build -t app .
        docker run --rm --network host app
        ;;
    run)
        docker run --rm --network host app
        ;;
    kill)
        docker kill trex
        ;;
    *)
    echo "Invalid config argument"
    exit 1
    ;;
esac