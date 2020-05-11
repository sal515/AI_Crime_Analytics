# Environment Requirements:
* Python 3.7.2 (Tested on)
* Windows 10 Home x64 (Tested on)
* Miniconda (Install Instructions provided in **Installations
 Instructions** section)
    * conda 4.8.3

# Required Libraries (Installation Instructions section provide installation steps): 
* Geopandas 

# Installation Instructions
### Install Miniconda: (to be able to use conda virtual environment)
* Download link and install: 

        https://docs.conda.io/en/latest/miniconda.html

* Add following paths, to the environment variable path (windows 10):

        C:\Users\Sal\miniconda3
        
        C:\Users\Sal\miniconda3\Scripts
        
* Update conda from the command prompt: (to test if it is working): 

        conda update conda
       
* If HTTP error occurs (I got this issue):
    * Install openSSL module
        * Download link: 
        
                https://slproweb.com/products/Win32OpenSSL.html
                
    * Please run the **"update conda"** command provided in the previous step to test if the issue is resolved. 

### Install Geopandas: (conda virtual environment needs to be activated before installation)
* Setup command using conda manager: 

        conda install geopandas  
    * Reference link: https://geopandas.org/install.html

# Run Instructions
### Pe-requisite: Create conda virtual environment for the project
* Go to project directory

        cd <project_root_path>
        
    * For my computer only (Tested on)
                
                cd C:\Projects\AI_Crime_Analytics

* Create conda environment (using **package-list.txt** file provided in this project root directory):
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html
    
                conda create -n <environment_name> --file <...>\AI_Crime_Analytics\package-list.txt 
                
        * For my computer only (Tested on)
                
                conda create -n <environment_name> --file C:\Projects\AI_Crime_Analytics\package-list.txt 
            
            

* Activate conda environment 
    
        activate <environment_name>
        
    * If the virtual environment was successfully activated, the command prompt will show (environment_name) on the left of each new line on the command prompt
       
* Run project files 
    
        Project file run instructions
    
* Deactivate current conda environment (if needed)

        deactivate


# Additional Instructions (needed during the development of project)
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