# Keep an eye on your Donkey's battery - First step for eco-friendly Donkey Cars
Enables you to monitor various key properties of your car's battery which are stored with the images, throttle, steering, ... values in *mycar/data/* to include them into your model training.
This implementation provides voltage, current and power values but can also be extended or reduces just to your needs.

## Setup
This works for Donkeys with with a [Robohat MM1](https://robohatmm1-docs.readthedocs.io/en/latest/) and an INA219 current unit.

Make sure you have the [libraries](https://docs.circuitpython.org/projects/ina219/en/latest/) for communication with the current unit installed (`pip install adafruit-circuitpython-ina219 adafruit-circuitpython-register`).

Complete the [software setup](https://docs.donkeycar.com/guide/create_application/) on your car.
Add the following lines to **myconfig.py**: 
```
HAVE_INA = True
INA_ADDR = 0x41
```

It is said that the default address of the current unit is *0x40* although in practice it should often be *0x41*. You can check which address is used by executing `i2cdetect -r -y 1` in the console of your Donkey Car.
Now you can add the current unit **ina.py** as another *part* to your car and replace your **manage.py** with the one provided here. Alternatively you can just add the following lines to your **manage.py** which create the INA219 object and cause that the battery information is recorded alongside the other tub data.

```
if cfg.HAVE_INA:
        from donkeycar.parts.ina import INA
        ina = INA(addr=INA_ADDR)
        V.add(ina, outputs=['ina/voltage', 'ina/current', 'ina/power'], threaded=False)
        
if cfg.HAVE_INA:
      inputs += ['ina/voltage', 'ina/current', 'ina/power']
      types += ['float', 'float', 'float']
```

## Ideas how to progress

- Make sure your car can drive

	...at some point there has already been an implementation of automated stopping as soon as the battery level falls below a certain threshold. Something similar can be implemented or even use it so that the car only drives when the battery level is in a certain range. This can be essential for realiable driving. For example when recording training data for self-driving Donkey Car you want to deploy the car in a similar environment including same behaviour of the throttle and thus battery level.
- Make sure your car can drive at consistent speed

	...this is a more narrow use-case of the previous one. We saw that some batteries discharge quite fastly when driving for a while. Consequently the same throttle values will be equivalent to different speed depending on the time. With a more dicharged battery it needs more throttle to reach the same speed which makes the car bahave different as we would expect from real cars or at least we would want the speed to be linearly dependent on the throttle. (Without being able to measure the real speed because you might lack the necessary sensors.) Now with knowing the battery voltage you at least have the tools at hand to come up with a function that translates throttle to real speed - but this will most probably be specific to your battery and car used.
- Voltmeter

	...without any proper voltmeter at hand you could use the INA. Using a 8.4 V LiPo battery the measurements were quite accurate for me.
**- Eco-friendly driving

	...actually our first use-case for this implementation. We were thinking about a machine learning model that takes the energy used into account so that it of course drives safely but as well tries to minimize the energy needed and e.g. drives smoother, slower, more careful. The energy spent could be retrieved via the area under the power curve. In particular we were thinking about a RL-model that gets rewarded for low battery usage. If that is feasable and how to use the provided values best in a model has yet to be investigated.**
	
## Different approach
If you are interested in retrieving battery information from/ on the robohat directly you might be interested in this [piece](https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in) (the pin for the MM1 is *board.BATTERY*) and communication of [MM1 to Donkey Car](https://github.com/tillwenke/robohatmm1_to_donkeycar_communication).
	
## Resources
All of this is inspired by how a IMU (another sensor) is treated for the same purpose in the default [donkeycar code](https://github.com/autorope/donkeycar).
There was also a implementation present in the [Donkey App](https://play.google.com/store/apps/details?id=com.robocarLtd.RobocarController&hl=en&gl=US&pli=1) which has been [abandoned](https://github.com/robocarstore/donkeycar_controller/issues/10) as MM1 is discontinued by the manufacturer. Still you can investigate the portion of how much your battery is charged (ranging 7V to 8.4V) via `http://donkey-ip:8000/vehicle/status` and an implementation of the retrieval of those values can be found [here](https://github.com/robocarstore/donkeycar-console/blob/dev/dkconsole/vehicle/vehicle_service.py#L702).
