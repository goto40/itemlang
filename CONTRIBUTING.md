# Contributing

## Get Started!

        cd itemlang/
        virtualenv -p $(which python3) venv
        # or: virtualenv venv
        source venv/bin/activate
        pip install -r requirements_dev.txt
        pip install -e .
        
    Previous stuff is needed only the first time. Later you just do:
    
        cd itemlang/
        source venv/bin/activate
        
## Run tests

	py.test tests

## Check code style

	flake8

Note: You can run flake8 from within pycharm using "Settings > External Tools" and add flake8 there (set the working directory to "$Projectpath$"). After this you can run flake8 from the context menu of your project. 
