# Keep an eye on your Donkey's battery

## Setup
This works for Donkeys with with a [Robohat MM1](https://robohatmm1-docs.readthedocs.io/en/latest/) and an INA219 current unit.

Make sure you have the library for communication with the current unit installes (*pip install adafruit-circuitpython-ina219*).

Complete the [software setup] (https://docs.donkeycar.com/guide/create_application/) on your car.
Add the following line to _myconfig.py_: ’HAVE_INA = True’
Now you can add the current unit _ina.py_ as another *part* to your car and replace your _manage.py_ with the one provided here. Alternatively you can just add the following lines to your _manage.py_ which create the INA219 object and cause that the battery information is recorded alongside the other tub data.

```
if cfg.HAVE_INA:
        from donkeycar.parts.ina import INA
        ina = INA(addr=0x41)
        V.add(ina, outputs=['ina/voltage', 'ina/current', 'ina/power'], threaded=False)
        
if cfg.HAVE_INA:
      inputs += ['ina/voltage', 'ina/current', 'ina/power']
      types += ['float', 'float', 'float']
```

## Ideas how to progress



