conda deactivate

git clone https://github.com/djpasseyjr/graphinference.git
cd graphinference

# Set up virtual env
python -m venv graphinference_venv
source graphinference_venv/bin/activate

pip install -r requirements.txt
pip install .

python experiments/noise_experiments_test.py $1
