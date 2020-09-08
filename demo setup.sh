conda create --name demo python=3.7 pip
conda activate demo
pip install pyplatform
conda install ipykernel
ipython kernel install --user --name=demo

# initialization script for dev env
cd $CONDA_PREFIX
mkdir -p ./etc/conda/activate.d
mkdir -p ./etc/conda/deactivate.d
touch ./etc/conda/activate.d/env_vars.sh
# set environment variables in activation script
#!/bin/sh
# export GOOGLE_APPLICATION_CREDENTIALS='path/to/service-account-file.json'

touch ./etc/conda/deactivate.d/env_vars.sh
# unset environment variables in deactivate script
#!/bin/sh
# unset GOOGLE_APPLICATION_CREDENTIALS

# launch jupter lab
jupyter lab
