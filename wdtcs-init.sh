#!/bin/bash

PYTHON_PATH=/usr/bin/python
WDTCS_HOME=`pwd`
API_SETTINGS=$WDTCS_HOME/conf/settings.py
BIN_DIR=$WDTCS_HOME/bin
LOG_DIR=$WDTCS_HOME/logs
WEBSRV_APP=$BIN_DIR/wdtcs_websrv.py
WEBSRV_PID=$BIN_DIR/wdtcs_websrv.pid
WEBSRV_LOG=$LOG_DIR/wdtcs_websrv.log
APISRV_APP=$BIN_DIR/wdtcs_apisrv.py
APISRV_PID=$BIN_DIR/wdtcs_apisrv.pid
APISRV_LOG=$LOG_DIR/wdtcs_apisrv.log

status() {
    # Check web server's status
    if is_websrv_running; then
        echo "The web server is RUNNING"
    else
        echo "The web server is NOT running"
    fi
    # Check api server's status
    if is_apisrv_running; then
        echo "The api server is RUNNING"
    else
        echo "The api is NOT running"
    fi
 }

restart() {
    stop
    start
}

start() {
    # Start the web server
    start_websrv
    # Start the api server
    start_apisrv
}

start_websrv() {
    if is_websrv_running; then
        echo "The web server is already running!"
    else
        echo "Starting the web server..."
        $PYTHON_PATH "${WEBSRV_APP}" $WDTCS_HOME >> $WEBSRV_LOG 2>&1 &
        echo $! > $WEBSRV_PID
    fi
}

start_apisrv() {
    if is_apisrv_running; then
        echo "The api server is already running!"
    else
        echo "Starting the api server..."
        $PYTHON_PATH "${APISRV_APP}" $API_SETTINGS >> $APISRV_LOG 2>&1 &
        echo $! > $APISRV_PID
    fi
}

stop() {
    # Stop the web server
    stop_websrv
    # Stop the api server
    stop_apisrv
}

stop_websrv() {
    if is_websrv_running; then
        echo "The web server is stopping"
        kill `get_websrv_pid`
        wait_while_websrv_running 30
        if is_websrv_running; then
            echo "The web server still not stopped. Trying kill -9"
            kill -9 `get_websrv_pid`
            wait_while_websrv_running 30

            if is_websrv_running; then
                echo "The web server still not stopped. Giving up."
                exit 1
            fi
        fi
    else
        echo "The web server is NOT running"
    fi
}

stop_apisrv() {
    if is_apisrv_running; then
        echo "The api server is stopping"
        kill `get_apisrv_pid`
        wait_while_apisrv_running 30
        if is_apisrv_running; then
            echo "The api server still not stopped. Trying kill -9"
            kill -9 `get_apisrv_pid`
            wait_while_apisrv_running 30

            if is_apisrv_running; then
                echo "The api server still not stopped. Giving up."
                exit 1
            fi
        fi
    else
        echo "The api server is NOT running"
    fi
}

is_websrv_running() {
    ps -e -o pid,command | grep "$WEBSRV_APP" | awk '{print $1}' | grep -q "^`get_websrv_pid`$"
    return $?
}

get_websrv_pid() {
    if [[ ! -f ${WEBSRV_PID} ]]; then
        echo "x"
    else
        cat ${WEBSRV_PID}
    fi
}

wait_while_websrv_running() {
    TIMEOUT=$1
    COUNTER=0
    echo -n "waiting..."
    while is_websrv_running && [ $COUNTER -lt $TIMEOUT ]; do
        sleep 1
        echo -n .
        let COUNTER=COUNTER+1
    done
    if is_websrv_running; then
        echo
    else
        echo " stopped"
    fi
}

is_apisrv_running() {
    ps -e -o pid,command | grep "$APISRV_APP" | awk '{print $1}' | grep -q "^`get_apisrv_pid`$"
    return $?
}

get_apisrv_pid() {
    if [[ ! -f ${APISRV_PID} ]]; then
        echo "x"
    else
        cat ${APISRV_PID}
    fi
}

wait_while_apisrv_running() {
    TIMEOUT=$1
    COUNTER=0
    echo -n "waiting..."
    while is_apisrv_running && [ $COUNTER -lt $TIMEOUT ]; do
        sleep 1
        echo -n .
        let COUNTER=COUNTER+1
    done
    if is_apisrv_running; then
        echo
    else
        echo " stopped"
    fi
}


case "$1" in
    start|stop|restart|status)
        $1
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 2
        ;;
esac
