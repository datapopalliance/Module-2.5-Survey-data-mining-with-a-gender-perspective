# Facebook MOOC


This repository contains all the analysis, databases and cleaning functions used for f020 Facebook MOOC 2021.


## Version and Requirements

This project uses *Python version 3.8.8*

All the libraries and versions that were used for this project are shown in the *requirements.txt* file. To install all the packages you can run the following command in terminal :



~~~bash
pip install -r requirements.txt
~~~



As we are using **Google Cloud Storage** to save our files, don't forget to authenticate and install all the GCP's library dependencies needed for DVC. You need to run the following commands before pushing data through a `dvc push` 



```bash
pip install 'dvc[gs]' 
gcloud auth login
gcloud auth application-default login
```



Also, you need to create a credentials.json file to use the API to download the Google cloud spreadsheet needed to store the metadata in our parquet tables. You can follow the instructions [here](https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c) and [here](https://developers.google.com/workspace/guides/create-credentials) to create such credentials. **IMPORTANT!!!!!!**: do not push your credentials to Github! this is a mayor security  breach.


Furthermore, we recommend you to work with a [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) environment as some of the libraries  may result in conflicts if they are used without an environment. 



## DVC

DVC (Database Version Control) is a library used by python to keep track of all the modifications that were made to our tables. As Git is for Code, [DVC](https://realpython.com/python-data-version-control/) is for databases and tables.

"DVC is meant to be run alongside Git. In fact, the `git` and `dvc` commands will often be used in tandem, one after the other. While Git  is used to store and version code, DVC does the same for data and model  files ... Large data and model files go in your DVC remote storage, and small `.dvc` files that point to your data go in GitHub"

To init dvc in you code computer you should us this command:



```bash
dvc init
```



This command has already been executed, so you don't need to run it.

To create an storage folder (location) for your files with dvc, you can use the following command: 



```bash
dvc remote add -d remote_storage path/to/your/dvc_remote
```



We will work with a **GCloud** bucket to store all the data. This branch has been already created for you to use.



To add a file to dvc you can run the next linechanges 



```bash
dvc add data/path/to/your/files
```



The previous command will create a .dvc file and will put your the file you submmited in the *.gitignore* file. This will avoid for you to push the original large file to github.

After that, you will need to push the dvc files to the remote respository. You need to run the following line



```bash
dvc push
```



A significant difference with Github is that commits are only used when you make a modification to a file you already submitted. To make a commit, you need to run the following line:



```bash
dvc commit
```



Finally, if some one of your team pushes another file to dvc, you can download these files to your local computer by using the following line:

  

```bash
dvc pull
```


## Available Functions

All the cleaning and analytic functions that are used can be found in the *src* folder. If you want to add a functionality to this folder, it is recommended to download [Pycharm](https://www.jetbrains.com/es-es/pycharm/download/#section=linux) and follow its indentation and comments protocols. Also, we recommend that all the functions are comment and follow the [pep8](https://www.python.org/dev/peps/pep-0008/) cleaning standards



## PDFs and other files

All the files that were not available in a tabular format, can be found in the following Google Drive folder 
### Poner Link de drive

The description and variable meaning of some tables were saved as PDFs, so if a table does not has this information, look for it in this folder.



## More Recommendations

Every member of the team must work with a git branch to avoid conflict. As internal protocol each branch must have the following name structure "**TeamMemberName-Task"**. For example, if *Gandalf* is going to add raw tables to dvc the branch name would be "Gandalf-RawTables". You can create a branch with the following git command:



```bash
git checkout -b Gandalf-RawTables
```



Make sure to pull all previous changes before creating a new branch. After all the tasks are finished, the branch would be merge to the main branch, prior a Team revision. 

 
