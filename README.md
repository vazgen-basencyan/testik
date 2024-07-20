# Integration suite
The Integration Suite is designed to test the integration of the platform and engine modules of the Aparavi applicatiob. Whether you need to connect and test specific endpoints, automate workflows, or ensure data consistency across your technology stack, our Integration Suite provides the tools and capabilities you need.

## Table of Contents

- [Toolset](#toolset)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [For Windows](#windows)
  - [For Linux](#linux)
- [Python and pip installation](#python-and-pip-installation)
- [Documentation for API Endpoints](#documentation-for-api-endpoints)

### Toolset
The Integration Suite is built using a robust set of tools and technologies to ensure the efficiency, reliability, and extensibility of our integration solution. Our toolset includes:
- API version: 2.7.1-7532
- Package version: 1.0.0
- Swagger Codegen version: 2.4.9

(no need to install them for now)

### Installation

#### Windows
**For Windows Users**: Please execute and check off each step below in the Table of Contents as you complete them to ensure a successful installation.
- [Prerequisites](#prerequisites)
- [Installation steps](#installation-steps-for-windows)
    - Step 1: [WSL installation](#wsl-installation)
    - Step 2: [Venv setup (for pycharm)](#venv-setup-for-pycharm)
    - Step 3: [Commands to run](#necessary-commands)

#### Linux
**For Linux Users**: Please execute and check off each step below in the Table of Contents as you complete them to ensure a successful installation.
- [Prerequisites](#prerequisites)
- [Installation steps](#installation-steps-for-linux)

##### Prerequisites
Before you can use or install this project, ensure that you meet the following system requirements:
Python 2.7 and 3.4+, Java 11+

##### Installation Steps for Windows

###### WSL installation
The current suites requires wsl to be installed in windows.
First, there is a command to check if WSL is installed:
    ```
    wsl -l -v
    ```

If you do not have installed WSL, then follow the next steps:
1. Open Command Prompt as an administrator by pressing `Win + X`, then selecting **Command Prompt (Admin)** or **Windows PowerShell (Admin)**.
2. Install the WSL feature by running the following command:
   ```
   wsl --install
   ```
3. Restart your computer to apply the changes.

###### venv setup for Pycharm
1. Configure a new venv for the project using this link https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements
2. Activate the venv, f.e use this command in Terminal (PyCharm) in Windows:
   ```
   .\venv\Scripts\activate.bat 
   ```

###### Necessary commands
1. Activate WSL in the root of directory:     
````wsl````
2. Run [this](#python-and-pip-installation) script if you don't have installed Python and Pip
3. Update .env file - check [this](#environment-file-content) for reference
4. Run this command: `sed -i 's/\r//' ./scripts/generate-models.sh`
5. Execute pip install:  `pip install .`
6. Check in the root of project if `swagger_client` folder is generated or not
7. If you have any problem debug it by running the following script: `bash ./scripts/generate-models.sh`
8. Finally, run the tests: ```pytest tests```
   
##### Python and Pip installation
If you do not have installed Python (and Pip), then run the **python-and-pip-install.sh** script:
1. Open Terminal
2. Run the command:
   ```
    bash ./scripts/python-and-pip-install.sh
   ```
   
##### Installation Steps for Linux
1. Activate `./venv` environment
2. Run [this](#python-and-pip-installation) script if you don't have installed Python and Pip
3. Execute pip install:  `pip install .`
4. Run this command: `sed -i 's/\r//' ./scripts/generate-models.sh`
5. Check in the root of project if `swagger_client` folder is generated or not
6. If you have any problem debug it by running the following script: `bash ./scripts/generate-models.sh`
7. Finally, run the tests: ```pytest tests```

## Documentation for API Endpoints

------ needs to be updated

All URIs are relative to *https://portal.aparavi.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*PublicApi* | [**server_api_v3_auth_get**](docs/PublicApi.md#server_api_v3_auth_get) | **GET** /server/api/v3/auth | Authentication Services

## Environment file content
Add `.env` file with the following content and update it accordingly.
```
HOST=http://localhost.aparavi.com
BASE_PATH=/server/api/v3
HYBRID_PORT=9752
AUTOTEST_USERNAME=root
AUTOTEST_PASSWORD=root
AUTOTEST_EMAIL=test@aparavi.com
ROOT_USERNAME=root
ROOT_PASSWORD=root
VERSION='2.10.0-8822'
ENVIRONMENT=local
SCAN_FOLDER=C:\Users\<YOUR_USER>\Documents
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
AWS_REGION=<AWS_REGION>
AWS_BUCKET=<AWS_BUCKET>
SMB_USERNAME=<SMB_USERNAME>
SMB_PASSWORD=<SMB_PASSWORD>
SMB_DOMAIN=<SMB_DOMAIN>
SMB_SHARE_NAME=<SMB_SHARE_NAME>
SMB_PATH=<SMB_PATH>
MINIO_ENDPOINT=<MINIO_ENDPOINT>
MINIO_ACCESS_KEY=<MINIO_ACCESS_KEY>
MINIO_SECRET_KEY=<MINIO_SECRET_KEY>
```# testik
# testik
