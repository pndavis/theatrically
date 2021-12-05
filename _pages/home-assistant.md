---
layout: page
title: Home Assistant
permalink: /home-assistant/
---

This is my [home assistant](https://www.home-assistant.io) config. I've been using home assistant since 2018, and have found it to be by far the most powerful echosystem to manage a smart home. 

Hardware:
* In terms of wireless smarthome devices, most are either zigbee, z-wave, or wifi. I would advise anyone who is wanting to build out a larger network to avoid wifi as it is terrible for battery life, and is unable to mesh with other devices, and it's able to send you information back to the manufacturer. 
* **Hub:** For a hub, I use the [Nortek HUSBZB-1](https://www.nortekcontrol.com/products/2gig/husbzb-1-gocontrol-quickstick-combo/). I've had no issues with it, though I haven't tried connecting any z-wave devices to it. Once you have a hub like this connected to home assistant, you don't need to worry about other hubs (though in some cases there are certain devices that need their hub to access a certain feature). For example, I use a lot of Ikea TRÅDFRI devices, but I don't need their gateway hub to connect. 
* **Lights:** For bulbs, most of mine are Ikea bulbs. They run quite a bit cheaper than hue and fairly comparable. For switches, I like the [Aqara Smart Wall Switch](https://www.aqara.com/us/smart_switch_no_neutral.html).
* **Sensors:** All of my sensors are from Aqara, and I have no complaints. I've got a couple of door sensors, a temperature sensor, and a motion sensor. For aqara's motion sensor, it has a two minute cooldown, but that can be easily fixed with [just a little soldering](https://community.smartthings.com/t/making-xiaomi-motion-sensor-a-super-motion-sensor/139806).
* **Remotes:** 
* **NFC Tag Reader:**

Software:
* **Zigbee Home Automation**
* **ControllerX**
* **Roku and Card**
* **HomeKit**
* **spotcast**
* **Node-Red**

Automations: