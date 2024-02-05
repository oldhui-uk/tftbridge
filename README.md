# tftbridge
This Klipper add-on allows you to use the BigTreeTech TFT35 display with Klipper in touch screen mode.

## Hardware Connection
For the general idea of the connection and hardware connection, please refer to [my post here](https://oldhui.wordpress.com/2024/01/28/using-btt-tft35-with-klipper-in-touch-mode/).


## Software Setup

A standard installation of Klipper puts the system into the `pi` user account.
Host add-ons will be in the  `/home/pi/klipper/klippy/extras` folder.
To install `tftbridge` as a Klipper add-on:

1. Copy `tftbridge.py` into `/home/pi/klipper/klippy/extras`
1. In your standard printer.cfg file, add the following section:

```
[tftbridge]
tft_device: /dev/ttyAMA0
tft_baud: 250000
tft_timeout: 0
klipper_device: /home/pi/printer_data/comms/serial/klipper.serial
klipper_baud: 250000
klipper_timeout: 0
```

If your configuration is different, you may need to customise the above settings.

## Running the Add-on
Restart the Klipper service to run the add-on:
```
sudo service klipper start
```

You should see Klipper starting as usual. A while later, the TFT35 should show "printer connected" in Touch Screen mode.

## Limitations
The add-on does not translate any commands. As the TFT35 is designed for Marlin, there may be Gcode which cannot be understood by Klipper.