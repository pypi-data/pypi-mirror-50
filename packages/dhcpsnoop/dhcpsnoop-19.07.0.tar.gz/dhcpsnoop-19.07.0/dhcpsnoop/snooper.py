#!/usr/bin/env python3.7
import glog as log
import sys
import yaml

from pathlib import Path
from scapy.all import sniff
from scapy.layers.l2 import Ether
from time import monotonic
from typing import List

class SnooperConfiguration:
    config_file = ""
    trusted_devices: List[str] = []
    presence_debounce_time = 5.0
    presence_last = 0.0
    presence_times: List[List[str]] = []
    non_file_fields = ["non_file_fields", "config_file", "presence_last"]


class Snooper:
    def __init__(self, callback=None, config_file="/etc/dhcpsnooper.conf", filter="port 68") -> None:
        self.config = SnooperConfiguration()
        self.init_config(config_file)
        self.callback = callback
        self.filter = filter

    def check_trusted_devices(self, src_mac: str) -> bool:
        return src_mac in self.config.trusted_devices

    def check_time_window(self) -> bool:
        # Is this a good time to update presence?
        return True

    def snooper_cb(self, pkt: Ether) -> None:
        # Debounce calls here
        if monotonic() - self.config.presence_last < self.config.presence_debounce_time:
            return

        # Check to see if this is a trusted device request
        if not self.check_trusted_devices(pkt.src):
            return

        # Check if this is a good time to updat presence
        if not self.check_time_window():
            return

        # Update debouncer
        self.config.presence_last = monotonic()

        log.info(f"Seen packet from trusted device \"{pkt.src}\"")
        if self.callback:
            self.callback(pkt.src)

    def init_config(self, config_file: str) -> None:
        # Load configuration file from disk
        config_file_path = Path(config_file)
        log.check(
            Path(config_file).exists(),
            message=f'Config file "{config_file_path}" doesn\'t exits',
        )
        with config_file_path.open() as config_file_fh:
            try:
                config_raw = yaml.safe_load(config_file_fh)
            except yaml.YAMLError as exc:
                log.error(f'Configuration file "{config_file_path}" parse error\n{exc}')

        # Set the config file we loaded
        self.config.config_file = str(config_file_path)
        # Load config from file
        for key, val in config_raw.items():
            # Don't load non_file_fields
            if key in self.config.non_file_fields:
                continue
            try:
                getattr(self.config, key)
            except AttributeError:
                # Warn when rubbish config is loaded
                log.warn(f'Loaded unknown configuration "{key}"')
            setattr(self.config, key, val)
        print("Finished Loading Config")
        return

    def snoop(self) -> None:
        print(f"Starting Snooper")
        sniff(prn=self.snooper_cb, filter=self.filter, store=0)
