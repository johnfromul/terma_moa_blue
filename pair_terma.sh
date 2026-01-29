#!/bin/bash

# Switch the heating element into pairing mode!
echo "!!! SWITCH THE HEATING ELEMENT INTO PAIRING MODE (5s hold button, blue
LED slow blink) !!!"
echo "You have 30 seconds..."
sleep 10

{
  sleep 2
  echo "agent KeyboardDisplay"
  sleep 1
  echo "default-agent"
  sleep 1
  echo "pair CC:22:37:11:48:0D"
  sleep 3
  echo "123456"
  sleep 5
  echo "trust CC:22:37:11:48:0D"
  sleep 2
  echo "quit"
} | bluetoothctl
EOF
