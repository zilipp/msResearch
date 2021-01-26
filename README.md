# An automatic tool for bone measurement

The structure of the project is as following:

```
+-- data
|   +-- iphone_ten
|   +-- markII
|   +-- structure_sensor
+-- ios
|   +-- native_app
|   +-- structure_sensor_sdk
+-- web
|   +-- analysis
|   +-- core_alg
|   +-- measurebone
+-- README.md
+-- .gitignore
```

The structure of `/data` is as following:

```
+-- data
|   +-- iphone_ten
|   +-- markII
    |   +-- scan
        |   +-- femur
            |   +-- Model.mtl
            |   +-- femur_0.obj
            |   +-- femur_1.obj
            |   +-- femur_2.obj
            |   +-- femur_3.obj
        |   +-- radius
        |   +-- humerus
        |   +-- tibia
|   +-- structure_sensor
|   +-- CR-1-l-fem
|   +-- CR-2-2-tib

```


In `/ios` 

`/native_app`: contains an application works in iOS mobile device 

`/structure_sensor_sdk`: the SDK of structure sensor Scanner 

In `/web` 

`/analysis`: web service in Django 

`/core_alg`: core algorithms for bone measurements 

Data can be downloaded from: 

https://drive.google.com/drive/folders/1UpFqdTYEeKpiWvTvGRh0lItcKqYEDipQ?usp=sharing

Report can be downloaded from: 

https://drive.google.com/drive/folders/12TX--8sONiThB2JGfjid0tvrq0stinot?usp=sharing
