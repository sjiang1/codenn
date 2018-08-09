# Forked from [sriniiyer/codenn](https://github.com/sriniiyer/codenn)

Extra notes on installation:
* Torch installation:
  * to overcome the LuaJIT low memory limit when using torch.save, **install torch with Lua 5.2 instead of LuaJIT**\
    use ```./clean.sh; TORCH_NVCC_FLAGS="-D__CUDA_NO_HALF_OPERATORS__" CC=/usr/bin/gcc-6 CXX=/usr/bin/g++-6 TORCH_LUA_VERSION=LUA52 ./install.sh``` to install Torch.
  * (build-essential, gcc, g++, libreadline-dev, cmake)
* install [cuda](https://developer.nvidia.com/cuda-downloads)
* Cutorch installation: [torch/cutorch](https://github.com/torch/cutorch/)\
  ```luarocks install cutorch```, ```luarocks install cunn```
* (for data preprocessing) antlr4: we need version 4.5 specified in src/csharp/CSharp4Lexer.py\
  ```python2 -m pip install 'antlr4-python2-runtime>=4.5,<4.6'```
* (for data preprocessing) antlr4-complete: to create a parser for Java, we need to download:\
  ```curl -O http://www.antlr.org/download/antlr-4.5.3-complete.jar```\
    ```export CLASSPATH=".:[path: antlr-4.5.3-complete.jar]:$CLASSPATH"```

---
---

# Original README

**Run CODENN**

See details of CODENN in our paper

Summarizing Source Code using a Neural Attention Model (https://github.com/sriniiyer/codenn/blob/master/summarizing_source_code.pdf)

Requirements

* Torch (http://torch.ch/docs/getting-started.html)
* Cutorch
* antlr4 for parsing C# (pip install antlr4-python2-runtime)

Setup environment

`export PYTHONPATH=~/codenn/src/:~/codenn/src/sqlparse`
`export CODENN_DIR=~/codenn/`
`export CODENN_WORK=./workdir`

Build both csharp and sql datasets

Install modified sqlparse

`cd src/sqlparse/`
`sudo python setup.py install`

Build datasets

`cd src/model`
`./buildData.sh`

Train codenn models and predict on test set

`./run.sh {sql|csharp}`
