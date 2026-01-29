#!/bin/bash

# Přepni topnou tyč do pairing módu!
echo "!!! PŘEPNI TOPNOU TYČ DO PAIRING MÓDU (5s tlačítko, modrá LED) !!!"
echo "Máš 30 sekund..."
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