# obniz_cli
`obniz_cli` is cli tool for obnizOS(for ESP32) install.

## Installation
Using pip,
```
pip install obniz_cli
```

## Usage
### flashos
```
obniz_cli flashos [-b] [-p]
```
You can install obnizOS to your ESP32 device. If you execute without any option, it is displayed as follows:
```
0: /dev/cu.Bluetooth-Incoming-Port
1: /dev/cu.SLAB_USBtoUART

Select NUMBER from above list(or if you want to cancel, input N key):
```
Select the device you want to install. (A device port can be passed to command with `-p` option like `obniz_cli flashos -p /dev/cu.SLAB_USBtoUART`).  

Then, latest obnizOS is downloaded and installed to device. By default, installation is performed at 921600bps but if installation failed, try to decrease it by `obniz_cli flashos -b 115200`.

### eraseos
```
obniz_cli eraseos [-p]
```
You can reset your device by this command.