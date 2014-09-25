Coupled Simulation-Analysis Execution
======================================

Provides a command line interface to run multiple Molecular Dynamics (MD) simulations, which can be coupled to an analysis tool. The coupled simulation-analysis execution pattern (aka ExTASY pattern) currently supports two examples: 
(a) Gromacs as the "Simulator" and LSDMap as the "Analyzer"; (b) AMBER as the "Simulator" and COCO as the "Analyzer". Due to the plugin-based architecture, this execution pattern, will be 
expandable as to support more Simulators and Analyzers.


Requirements
============

* python >= 2.7
* virtualenv >= 1.11
* pip >= 1.5
* Password-less ssh login to remote machine

> Some tips to setup a password-less login
> ```
> http://www.linuxproblem.org/art_9.html
> ```


Installation
=============

To install the ExTASY framework, create a virtual environment on localhost and use pip to install the package

```
virtualenv /tmp/test
source /tmp/test/bin/activate
cd /tmp/
pip install --upgrade git+https://github.com/radical-cybertools/radical.pilot.git@master#egg=radical.pilot
pip install --upgrade git+https://github.com/radical-cybertools/radical.ensemblemd.mdkernels.git@master#egg=radical.ensemblemd.mdkernels
git clone --branch extasy-0.1-rc2 https://github.com/radical-cybertools/ExTASY.git
cd ExTASY
python setup.py install
```
> If you have multiple allocations on the same system, set the environment variable PROJECT_ID 
> to your allocation number 
>
> ```
> export PROJECT_ID='ABCXYZ123'
> ```

After installation on localhost, the following sections have to be implemented to run the workload.

1. Installing LSDMap/CoCo on Stampede
2. Setting up the Radical Pilot configuration file
3. Setting up the Kernel configuration file : Gromacs-LSDMap/Amber-CoCo
4. Running the workload : Gromacs-LSDMap/Amber-CoCo


Installing LSDMap on Stampede
---------------------------

Running LSDMap on Stampede requires that you make a local installation of scipy 0.10.0 (or greater) and numpy 1.4.1 
(or greater)using the existing python/2.7.6. To use python/2.7.6, you will have to load intel/14.0.1.106. If you do 
not have scipy 0.10.0 (or greater) and numpy 1.4.1 (or greater) with python/2.7.6, goto [link](https://github.com/radical-cybertools/ExTASY/blob/devel/docs/scipy_installation_stampede_python_2_7_6.md)

To check the version of scipy and numpy,

```
import scipy
scipy.__version__
import numpy
numpy.__version__
```


After installing the dependencies, you will need to make a local installation of lsdmap on Stampede using the existing
python/2.7.6

```
module load -intel intel/14.0.1.106
module load python
cd
git clone git://git.code.sf.net/p/lsdmap/git lsdmap
cd lsdmap
python setup.py install --user
```


Installing CoCo on Stampede
-------------------------

Running CoCo on Stampede requires that you make a local installation of scipy 14 (or greater) using the 
existing python/2.7.3. To use python/2.7.3, you will have to load intel/13.0.2.146. If you do not have scipy 14 
(or greater) with python/2.7.3, goto [link](https://github.com/radical-cybertools/ExTASY/blob/devel/docs/scipy_installation_stampede_python_2_7_3.md)

To check the version of scipy and numpy,

```
import scipy
scipy.__version__
import numpy
numpy.__version__
```


After installing the dependencies, you will need to explicitly log into Stampede and make a local 
installation of CoCo using the existing python/2.7.3.

```
cd $HOME
git clone https://bitbucket.org/extasy-project/coco.git
module load python
cd $HOME/coco
python setup.py install --user
```



USAGE
======

To use the CSA tool, you will first need to setup two files. 

A configuration file for the Radical Pilot related parameters which would allow us to launch pilot(s) and compute units on the targeted remote machine.
You will also use this file to mention the Simulation and Analysis kernels to be used.

The second configuration file should contain all the parameters required to execute the Simulation and Analysis kernels. A detailed description for each of the 
combinations (Gromacs-LSDMap / Amber-CoCo) is given below.


Setting up the Radical Pilot configuration file
------------------------------------------------

The RP config file is used for defining the parameters related to Radical Pilot. It is one of the input files 
to the csa tool.

* Load_Preprocessor : The preprocessor to be used. Can be 'Gromacs' or 'Amber'
* Load_Simulator    : The Simulator to be loaded. Can be 'Gromacs' or 'Amber'
* Load_Analyzer     : The Analyzer to be loaded. Can be 'LSDMap' or 'CoCo'
* UNAME         : Username to access the remote machine
* REMOTE_HOST   : URL of remote machine
* WALLTIME      : Walltime in minutes for the complete job
* PILOTSIZE     : No. of cores to reserved for the entire job
* DBURL         : MongoDB URL


Setting up the Kernel configuration file : Gromacs-LSDMap
----------------------------------------------------------

As described before, the other input file to the tool is the file containing all required parameters for the
Kernel execution. The following are the parameters required for the Gromacs-LSDMap kernel combinations. An 
example/demo can be found in ``` /tmp/ExTASY/config/gromacs_lsdmap_config.py```.

----------------------------------------------------------General-------------------------------------------------------------------------

* num_CUs           : Number of Compute Units to be submitted to the pilot
* num_iterations    : Number of iterations of Simulation-Analysis
* nsave             : Number of iterations after which backup is to be created
* start_iter        : Iteration number with which to start

-----------------------------------------------------Simulation(Gromacs)--------------------------------------------------------------

* input_gro_loc & input_gro : location and name of the input(gro) file
* grompp_loc & grompp_name  : location and name of the grompp(mdp) file
* topol_loc & topol_name    : location and name of the topol(top) file
* tmp_grofile               : name of the intermediate file used as input for LSDMap
* ndxfile_name & ndxfile_loc: name and location of index file
* grompp_options            : grompp options to be added during runtime
* mdrun_options             : mdrun options to be added during runtime
* itpfile_loc               : location of itpfiles to be transfered

-------------------------------------------------------Analysis(LSDMap)---------------------------------------------------------------

* lsdm_config_loc & lsdm_config_name : location and name of the lsdm configuration file
* wfile     : name of the weight file to be used in LSDMap
* max_alive_neighbors : maximum alive neighbors to be considered during reweighting step
* max_dead_neighbors  : maximum dead neighbors to be considered during reweighting step

------------------------------------------------------------Update--------------------------------------------------------------------------

* num_runs : number of replicas

-------------------------------------------------------------Auto---------------------------------------------------------------------------

These parameters are automatically assigned based on the values above. These are mainly for the 
propagation of filenames throughout the tool.

* system_name
* outgrofile_name
* egfile 
* evfile 
* nearest_neighbor_file 
* num_clone_files 


Setting up the Kernel configuration file : Amber-CoCo
------------------------------------------------------

As described before, the other input file to the tool is the file containing all required parameters for the
Kernel execution. The following are the parameters required for the Amber-CoCo kernel combinations. An 
example/demo can be found in ``` /tmp/ExTASY/config/amber_coco_config.py```.


----------------------------------------------------------General-----------------------------------------------------------------------------

* num_iterations  : Number of iterations of Simulation-Analysis chain
* nreps           : Number of replicas


-------------------------------------------------------Simulation(Amber)----------------------------------------------------------------

* mdshort_loc & mdshortfile : Location and name of the mdshort file
* min_loc & minfile         : Location and name of the min file
* crd_loc & crdfile         : Location and name of the crd file
* top_loc & topfile         : Location and name of the topology file


-------------------------------------------------------Analysis(CoCo)--------------------------------------------------------------------

* grid              : the number of grid points per dimension in the CoCo histogram
* dims              : the number of dimensions (PCs) in the CoCo mapping
* frontpoints       : the number of fronteir points to return structures



Running the workload : Gromacs-LSDMap
---------------------------------------
46
The command format to run the workload is as follows,

```
extasy --RPconfig RPCONFIG --Kconfig KCONFIG
```

where RPCONFIG is the path to the Radical Pilot configuration file and KCONFIG is the path to the Kernel 
configuration file. But before running this command, there are some dependencies to address which is particular 
to this combination of kernels.


The update stage following LSDMap in each iteration requires numpy. For this install numpy as follow,

```
pip install numpy
```

Next we need to set the tool to use Gromacs as the Simulation kernel and LSDMap as the Analysis kernel. For this,
we need to set 2 parameters in the Radical Pilot configuration file.

```
Load_Simulator = 'Gromacs'
Load_Analyzer = 'LSDMap'
````

All set ! Run the workload execution command ! If you followed this document completely, the command should look like
```
extasy --RPconfig /tmp/ExTASY/config/RP_config.py --Kconfig /tmp/ExTASY/config/gromacs_lsdmap_config.py
```


**What this does ...**

This command starts the execution. It will first submit a pilot on the REMOTE_HOST and reserve the number of cores as defined by the
PILOTSIZE. Once the pilot goes through the queue, the Preprocessor splits the input gro file as defined by ```input_gro``` into
temporary smaller files based on ```num_CUs```. The Simulator is then loaded which submits Compute Units to the REMOTE_HOST
and takes as input the temporary files, a mdp file and a top file and runs the MD. The output is aggregated into one gro file to be used 
during the Analysis phase. The Analyzer is then loaded which looks for a gro file as defined by ```tmp_grofile```
in KCONFIG in the current directory (from where ```extasy``` is run) and runs LSDMap on it.


Number of CUs in the simulation stage = num_CUs

Number of CUs in the analysis stage = 1

Total number of CUs in N iterations of ASA = N*(num_CUs + 1)


Running the workload : Amber-CoCo
---------------------------------------

The command format to run the workload is as follows,

```
extasy --RPconfig RPCONFIG --Kconfig KCONFIG
```

where RPCONFIG is the path to the Radical Pilot configuration file and KCONFIG is the path to the Kernel 
configuration file. But before running this command, there are some dependencies to address which is particular 
to this combination of kernels.

Before we start with the execution, we need to set the tool to use Amber as the Simulation kernel and CoCo as the Analysis kernel. For this,
we need to set 2 parameters in the Radical Pilot configuration file.

```
Load_Simulator = 'Amber'
Load_Analyzer = 'CoCo'
````

All set ! Run the workload execution command ! If you followed this document completely, the command should look like

```
extasy --RPconfig /tmp/ExTASY/config/RP_config.py --Kconfig /tmp/ExTASY/config/amber_coco_config.py
```


**What this does ...**

This command starts the execution. It will first submit a pilot on the REMOTE_HOST and reserve the number of cores as defined by the
PILOTSIZE. Once the pilot goes through the queue, there is no Preprocessor for these combination of kernels. The 
Simulator is loaded which transfers the required files (.crd,.top,.in) and performs the amber simulation on the
provided input. After all the simulations are done, the Analysis stage kicks in and performs analysis using the CoCo method.
The output of the Analysis stage is fed back as the input of the Simulation in the next iteration. 

 
Number of CUs in the simulation stage = num_CUs

Number of CUs in the analysis stage = 1

Total number of CUs in N iterations of ASA = N*(num_CUs + 1) 

