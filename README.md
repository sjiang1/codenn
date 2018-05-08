# Forked from [sriniiyer/codenn](https://github.com/sriniiyer/codenn)

Extra notes on installation:
* Torch installation: ```export TORCH_NVCC_FLAGS="-D__CUDA_NO_HALF_OPERATORS__"```
* Cutorch installation: [torch/cutorch](https://github.com/torch/cutorch/)\
  ```luarocks install cutorch```
* antlr4: we need version 4.5 specified in src/csharp/CSharp4Lexer.py\
  ```python2 -m pip install 'antlr4-python2-runtime>=4.5,<4.6'```

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
