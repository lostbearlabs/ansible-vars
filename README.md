
# ansible-vars

ansible-vars summarizes variables used in the playbooks and roles of an ansible project.
It reports:
* default values for variables in each role and playbook
* where each variable in a role or playbook is referenced
* variables which are set but never referenced
* variables which are referenced by never set
* variables with the same name but different defaults
* default values specified for the same variable name in multiple places

ansible-vars is inspired by [ansible-lint][https://github.com/willthames/ansible-lint]


## Setup

### From Source

```
git clone https://github.com/lostbearlabs/ansible-vars
export PYTHONPATH=$PYTHONPATH:`pwd`/ansible-vars/lib
export PATH=$PATH:`pwd`/ansible-vars/bin
```

## Usage

```
Usage:
$> ansible-vars -d ../my-ansible-project

Arguments:

  -d    --directory    location of ansible project to analyze
  -v    --verbose      emit extra debugging information during run

```



## Development Notes

### PyCharm Run Target

```
$> dev/ansible/ansible-vars/lib/ansiblevars/main/__init__.py -d  ../my-ansible-project
```

### Running Tests at Terminal

```
$> tox test
# -- OR --
$> python setup.py test
```

### Running Tests in PyCharm

```
target:              path
                     ansible-vars/test
patterh:             *.py

working directory:   ansible-vars
```

