# Keep an eye on your Donkey's battery
Enables you to monitor various key properties of your car's battery which are stored with the images, throttle, steering, ... values in *mycar/data/* to include them into your model training.

## Setup
This works for Donkeys with with a [Robohat MM1](https://robohatmm1-docs.readthedocs.io/en/latest/) and an INA219 current unit.

Make sure you have the [libraries](https://docs.circuitpython.org/projects/ina219/en/latest/) for communication with the current unit installed (`pip install adafruit-circuitpython-ina219 adafruit-circuitpython-register`).

Complete the [software setup](https://docs.donkeycar.com/guide/create_application/) on your car.
Add the following line to **myconfig.py**: `HAVE_INA = True`
Now you can add the current unit **ina.py** as another *part* to your car and replace your **manage.py** with the one provided here. Alternatively you can just add the following lines to your **manage.py** which create the INA219 object and cause that the battery information is recorded alongside the other tub data.

```
if cfg.HAVE_INA:
        from donkeycar.parts.ina import INA
        ina = INA(addr=0x41)
        V.add(ina, outputs=['ina/voltage', 'ina/current', 'ina/power'], threaded=False)
        
if cfg.HAVE_INA:
      inputs += ['ina/voltage', 'ina/current', 'ina/power']
      types += ['float', 'float', 'float']
```
(all of this is inspired by how a IMU (another sensor) is treated for the same purpose in the default [donkeycar code](https://github.com/autorope/donkeycar).)

## Ideas how to progress

- be sure your car can drive
- quite reliable battery checker
- eco friendly driving -> rl
- as model input to keep driving at consistent speed 
- explain the values & give credits to sources
- check registers with "i2cdetect -r -y 1"
