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
touch ./etc/conda/deactivate.d/env_vars.sh

# launch jupter lab
jupyter lab