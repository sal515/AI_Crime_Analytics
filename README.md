# Environment Requirements:
* Python 3.7.2 (Tested on)
* Windows 10 Home x64 (Tested on)
* Miniconda3 (Install Instructions provided in **Installations
 Instructions** section)
    * conda 4.8.3

# Required Libraries (Installation Instructions section provide installation steps): 
* Geopandas 
* matplotlib
* numpy

# Installation Instructions
### Install Miniconda3: (to be able to use conda virtual environment)
* Download link and install, (Use: "Just Me" option when asked): 

        https://docs.conda.io/en/latest/miniconda.html

* (Windows 10) For installation with default settings, add the following paths, to the environment variable called "path" :
    * If "Just Me" option was used to install minconda3, then please add the following paths with your computer name. Otherwise, the miniconda3 has to be found before adding the paths:

            C:\Users\<username or path to miniconda dir>\miniconda3
            
            C:\Users\<username or path to miniconda dir>\miniconda3\Scripts
        
* Update conda from the command prompt: (to test if it is working): 

        conda update conda
       
* If HTTP error occurs (I got this issue):
    * Install Win64 OpenSSL v1.1.1g
        * Download link: 
        
                https://slproweb.com/products/Win32OpenSSL.html
                
    * Please run the **"update conda"** command provided in the previous step to test if the issue is resolved. 


# Run Instructions
### Pe-requisite: Create conda virtual environment for the project
* Open a windows command prompt/terminal

* Go to project directory from terminal

        cd <project_root_path>
        
        example: cd C:\Projects\AI_Crime_Analytics

* Add conda forge channel to conda config by executing the following conda command (required to install the packages):
    
        conda config --append channels conda-forge

* Create conda environment (using **package-list.txt** file provided in this project root directory to install all the required packages):
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html
    
                conda create -n <environment_name> --file <project_root_path>\AI_Crime_Analytics\package-list.txt 
                
                example: conda create -n <environment_name> --file C:\Projects\AI_Crime_Analytics\package-list.txt 
 
    * If the environment was successfully created the following messages will be seen:
        
        Preparing transaction: done
        
        Verifying transaction: done
        
        Executing transaction: done
        
        -# To activate this environment, use

        -#     $ conda activate ai_crime_analytics

        -# To deactivate an active environment, use

        -#     $ conda deactivate

 
* Activate conda environment 
    
        activate <environment_name>
        
    * If the virtual environment was successfully activated, the command prompt will show (environment_name) on the left of each new line on the command prompt
       
* Run project files 
           
    * Note: Please ensure that the python terminal is in the root of the project directory containing **main.py** file and the conda environment is activated
    
    * run the following in the terminal to run the project:     
        
            python main.py   
    
    * Note: it takes some time to run the first time
    
* Deactivate current conda environment (if needed)

        deactivate


# Additional Instructions (only needed during the development of project)
* View conda package list:
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html

            conda list -n <environment_name>

* Update conda package list (Project environment should be activated already):
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html

                conda list --export > <...>\AI_Crime_Analytics\package-list.txt
            
        * For my computer only (Tested on)
            
                conda list --export > C:\Projects\AI_Crime_Analytics\package-list.txt
            
            
* Update conda spec-file (Project environment should be activated already):
    * Reference link: https://docs.conda.io/projects/conda/en/4.6.1/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

                conda list --explicit > <...>\AI_Crime_Analytics\spec-file.txt
            
        * For my computer only (Tested on)
            
                conda list --explicit > C:\Projects\AI_Crime_Analytics\spec-file.txt
            
            
            

* To create a new conda environment from spec-file (Environment specific):
    * Reference link: https://docs.conda.io/projects/conda/en/4.6.1/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

                conda create --name <environment_name> --file <...>\AI_Crime_Analytics\spec-file.txt
            
        * For my computer only (Tested on)
            
                conda create --name <environment_name> --file C:\Projects\AI_Crime_Analytics\spec-file.txt           
                
# General References:
* Tasks with conda:
    
        https://docs.conda.io/projects/conda/en/4.6.1/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands
        
* Conda cheat sheet: 
 
        https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf