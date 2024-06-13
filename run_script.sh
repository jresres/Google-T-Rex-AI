#!/bin/sh

case "$1" in 
    open)
        docker run --rm --name trex -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest
        ;;
    build)
        docker build -t app .
        docker run -it --rm -v $(pwd):/app --network host app
        ;;
    run)
        docker run -it --rm -v $(pwd):/app --network host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix app
        ;;
    kill)
        docker kill trex
        ;;
    *)
    echo "Invalid config argument"
    exit 1
    ;;
esac