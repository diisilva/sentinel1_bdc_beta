# sentinel1_bdc_beta package 
## About 
Sentinel 1  processing library (beta version).

## 1. Requirements
    - Anaconda 3.x (https://www.anaconda.com/products/distribution)
    
    ps. Need to create an environment in anaconda (conda for installation of the eradicate packaging of the Sentinel Application Platform (SNAP).
    ```E.g. 
        conda create --name my_env python=3```

    - Snap v8.0.0 (https://anaconda.org/Terradue/snap)
    ```E.g. 
        conda install -c terradue snap```

# 2. Instalation sentinel1_bdc_beta package  
## After enabling the conda environment and installing the snap package in the directory where you git cloned the sentinel1_bdc_beta library run 
    ```pip3 install -e . ```

# 3. Usage Examples
    ```$python3
    >>> from sentinel1_bdc_beta import run
    >>> run.start('PATH_ZIP_IMAGE') 
    ```

# 4. Functions documentation
    ``` pending/documenting ```

# 5. Alternative usage
## 5.1 You can use the library in a docker environment. 
 ``` Step 1: 
        > docker pull marujore/sentinel-toolboxes:1.0.0
    
    Step 2:
        > sudo docker run --restart=always -d -it -v [YOUR_PATH]:/work --name test marujore/sentinel-toolboxes:1.0.0

    Step 3: 
        > sudo docker exec -it teste bash
    
    Step 4: Clone the resporitory sentinel1_bdc_beta package in /work and 
        > conda activate geospatial
    
    Step 5: 
        > Repeat items 2 and 3 of this documentation 
    

