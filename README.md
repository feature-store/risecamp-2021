# risecamp-2021
To get started, clone the respository: 
```
git clone https://github.com/feature-store/risecamp-2021.git
cd risecamp-2021

# Setup env
python -m venv env
source env/bin/activate
```
Setup notebook: 
```
pip install ipykernel
python -m ipykernel install --user --name=risecamp-2021
```
Next, install ralf: 
```
git clone https://github.com/feature-store/ralf.git -b api-for-tutorial --single-branch
cd ralf
pip install -e .
```
Now you can follow the tutorial notebook! 
