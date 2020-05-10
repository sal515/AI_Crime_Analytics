# Environment Requirements:
* Python 3.7.2 (Tested on)
* Windows 10 Home x64 (Tested on)
* Miniconda (Install Instructions provided in **Installations Instructions** section)

#Installation Instructions
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
          

# Run Instructions
###Pe-requisite: Create conda virtual environment for the project
* Go to project directory

        cd <project_root_path>

* Create conda environment (using **package-list.txt** file provided in this project root directory):
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html
    
                conda create -n <environment_Name> --file <...>\AI_Crime_Analytics\package-list.txt 
                
        * For my computer only (Tested on)
                
                conda create -n <environment_Name> --file C:\Projects\AI_Crime_Analytics\package-list.txt 
            
            

* Activate conda environment 
    
        activate <environment_Name>
       
* Run project files 
    
        Project file run instructions
    
* Deactivate current conda environment (if needed)

        deactivate


# Additional Instructions (needed during the development of project)
* View conda package list:
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html

            conda list -n <environment_Name>

* Update conda package list (Project environment should be activated already):
    * Reference link: https://docs.conda.io/projects/conda/en/latest/commands/list.html

                conda list --export > <...>\AI_Crime_Analytics\package-list.txt
            
        * For my computer only (Tested on)
            
                conda list --export > C:\Projects\AI_Crime_Analytics\package-list.txt
            

            