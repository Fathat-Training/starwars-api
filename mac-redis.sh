#!/bin/bash

# Update Homebrew
brew update

# Install Redis using Homebrew
brew install redis

# Enable Redis autostart
ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents

# Start Redis server via launchctl
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist

# homebrew.mxcl.redis.plist contains reference to redis.conf file location: /usr/local/etc/redis.conf

# Start Redis server using configuration file, Ctrl+C to stop
redis-server /usr/local/etc/redis.conf

redis-cli ping # Check if the Redis server is running

# Disable Redis autostart
# launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
