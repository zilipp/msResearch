# An automatic tool for bone measurement

# Table of contents
1. [Structure of the project](#project structure)
2. [Core algorithms](#algorithms)
3. [Instructions on web application](#web app)
    1. [Structure of the Django project](#django project)
    1. [Running locally](#local run)
4. [Instructions on Heroku deployment](#heroku)
5. [Other resources](#resources)


## 1. The structure of the project <a name="project structure"></a>

### The structure of the project is as following
```
+-- data
|   +-- iphone_ten
|   +-- structure_sensor
|   +-- UIC7-l
+-- ios
|   +-- native_app
|   +-- structure_sensor_sdk
+-- web
|   +-- analysis
|   +-- core_alg
|   +-- measurebone
|   +-- out
+-- README.md
+-- .gitignore
```

### The structure of `/data` is as following:

```
+-- data
|   +-- iphone_ten
|   +-- UIC7-l
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
|   +-- UIC7-r
|   +-- UIC8-l

```

### In `/ios` 

`/native_app`: contains an application works in iOS mobile device 

`/structure_sensor_sdk`: the SDK of structure sensor Scanner 

### In `/web` 

`/analysis`: web service in Django 

`/core_alg`: core algorithms for bone measurements 

`/out`: output files when taking measurements (ignored in git)

### Data can be downloaded from: 

https://drive.google.com/drive/folders/1UpFqdTYEeKpiWvTvGRh0lItcKqYEDipQ?usp=sharing

### Report can be downloaded from: 

https://drive.google.com/drive/folders/12TX--8sONiThB2JGfjid0tvrq0stinot?usp=sharing


## 2. Core algorithms <a name="algorithms"></a>
The core algorithms are in folder `/web/core_alg`.
 
In `/base`, the ```Bone``` class is the base class for all type of bones.

In `/scan`, we have five files, in `/image_process.py`, 
we pre-precess the 3D model, such as removing background of the model, align the bone in particular layout.
The other four file are algorithms for four type of bones. Please see details in report.

In `/utilies`, we defined some helper functions such us calculating distance from a point to a line.


## 3. Instructions on web application  <a name="django project"></a>
### 3.1 Structure of the Django project<a name="web app"></a>
The folder `/web` is the root directory of the Django project.

The folder `/measurebone` contains settings (urlpatterns, view, etc.) and 
static resources (html file, scripts etc.) of the project.

The folder `/analysis` is the root directory of the measurements app. 

For more details of Django Framework, please refer:  https://docs.djangoproject.com/en/3.1/

### 3.2 Running locally <a name="local run"></a>
Change current directory to `/web`, and run 
```bash
python manage.py runserver
```
The web application will run locally: http://127.0.0.1:8000/


## 4 Instructions on Heroku deployment <a name="heroku"></a>
1. creat an account on Heroku and install Heroku CLI on the machine: 
https://www.heroku.com/

1. init the git repository 

1. create an Heroku app and remote the repo to Heroku repo
    ```bash
    heroku create
    heroku git:remote -a name-of-app
    ```
1. install gunicorn and setting gunicorn
    ```bash
    pip install gunicorn 
    ```
     
    ```bash
    gunicorn measurebone.wsgi.py
    ```
1. creat Procfile and add 'web: gunicorn measurebone.wsgi'

1. push repo to heroku repo, then we have an link to the web app
    ```bash
    git subtree push --prefix web heroku master
    ```
   
1. check logs on Heroku:
```bash
heroku logs --tail
```

There is an detail video instruction on Youtube:
https://www.youtube.com/watch?v=GMbVzl_aLxM&ab_channel=PrettyPrinted


## 5 Other resources <a name="resources"></a>

Subtree: \
https://medium.com/@shalandy/deploy-git-subdirectory-to-heroku-ea05e95fce1f

Buildpack: \
https://github.com/heroku/heroku-buildpack-apt
```bash
heroku buildpacks:add --index 1 heroku-community/apt
```






