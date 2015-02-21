.. _grlsd:

********************************
Runing a Gromacs/LSDMap Workload
********************************

This section will discuss details about the execution phase. The input to the tool
is given in terms of a resource configuration file and a workload configuration file.
The execution is started based on the parameters set in these configuration files.

Running on Stampede
===================

Running the Example Workload
----------------------------

This section is to be done entirely on your **laptop**. The ExTASY tool expects two input
files:

    1. The resource configuration file sets the parameters of the HPC resource we want to
       run the workload on, in this case Stampede.

    2. The workload configuration file defines the GROMACS/LSDMap workload itself.

**Step 1** : Create a new directory for the example,

    ::

        mkdir $HOME/grlsd-on-stampede/
        cd $HOME/grlsd-on-stampede/

**Step 2** : Create a new resource configuration file ``stampede.rcfg`` :

    (Download it `stampede.rcfg <https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/config_files/grlsd-on-stampede/stampede.rcfg>`_ directly.)


    .. note::   Change the following values according to your needs :

                * UNAME
                * ALLOCATION

    ::

        REMOTE_HOST = 'stampede.tacc.utexas.edu'  # Label/Name of the Remote Machine
        UNAME       = 'username'                  # Username on the Remote Machine
        ALLOCATION  = 'TG-MCB090174'              # Allocation to be charged
        WALLTIME    = 60                          # Walltime to be requested for the pilot
        PILOTSIZE   = 16                          # Number of cores to be reserved
        WORKDIR     = None                        # Working directory on the remote machine
        QUEUE       = 'normal'                    # Name of the queue in the remote machine

        DBURL       = 'mongodb://extasy:extasyproject@extasy-db.epcc.ed.ac.uk/radicalpilot'

**Step 3** : Download the sample input data:

    ::

        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-stampede/config.ini
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-stampede/grompp.mdp
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-stampede/input.gro
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-stampede/topol.top


**Step 4** : Create a new workload configuration file ``gromacslsdmap.wcfg`` :

    (Download it `gromacslsdmap.wcfg <https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/config_files/grlsd-on-stampede/gromacslsdmap.wcfg>`_ directly.)

    ::

        #-------------------------Applications----------------------
        simulator             = 'Gromacs'           # Simulator to be loaded
        analyzer              = 'LSDMap'            # Analyzer to be loaded

        #--------------------------General--------------------------------
        num_CUs              = 16                   # Number of tasks or Compute Units
        num_iterations       = 3                    # Number of iterations of Simulation-Analysis
        start_iter           = 0                    # Iteration number with which to start
        nsave                = 2                    # # Iterations after which output is transfered to local machine

        #--------------------------Simulation--------------------------------
        num_cores_per_sim_cu = 1                    # Number of cores per Simulation Compute Units
        md_input_file        = './input.gro'        # Entire path to the MD Input file - Do not use $HOME or the likes
        mdp_file             = './grompp.mdp'       # Entire path to the MD Parameters file - Do not use $HOME or the likes
        top_file             = './topol.top'        # Entire path to the Topology file - Do not use $HOME or the likes
        ndx_file             = None                   # Entire path to the Index file - Do not use $HOME or the likes
        grompp_options       = None                   # Command line options for when grompp is used
        mdrun_options        = None                   # Command line options for when mdrun is used
        itp_file_loc         = None                   # Entire path to the location of .itp files - Do not use $HOME or the likes
        md_output_file       = 'tmp.gro'            # Filename to be used for the simulation output

        #--------------------------Analysis----------------------------------
        lsdm_config_file     = './config.ini'       # Entire path to the LSDMap configuration file - Do not use $HOME or the likes
        num_runs             = 1000                # Number of runs to be performed in the Selection step in Analysis
        w_file               = 'weight.w'           # Filename to be used for the weight file
        max_alive_neighbors  = '10'                 # Maximum alive neighbors to be considered while reweighting
        max_dead_neighbors   = '1'                  # Maximum dead neighbors to be considered while reweighting



**Now you are can run the workload using :**

    ::

        EXTASY_DEBUG=True RADICAL_PILOT_VERBOSE='debug' SAGA_VERBOSE='debug' extasy --RPconfig stampede.rcfg --Kconfig gromacslsdmap.wcfg 2> extasy.log

A **sample output** with expected callbacks and simulation/analysis can be found at `here <https://github.com/radical-cybertools/ExTASY/tree/master/sample_output_logs/grlsd-on-stampede>`_.

+------------------------+----------------+--------------+
|     Stage              |   Simulation   |   Analysis   |
+========================+================+==============+
| Expected TTC/iteration |    50-100 s    |     ~30 s    |
+------------------------+----------------+--------------+

Running on Archer
=================

Running the Example Workload
----------------------------

This section is to be done entirely on your **laptop**. The ExTASY tool expects two input
files:

    1. The resource configuration file sets the parameters of the HPC resource we want
       to run the workload on, in this case Archer.

    2. The workload configuration file defines the CoCo/Amber workload itself.

**Step 1** : Create a new directory for the example,

    ::

        mkdir $HOME/grlsd-on-archer/
        cd $HOME/grlsd-on-archer/

**Step 2** : Create a new resource configuration file ``archer.rcfg`` :

    (Download it `archer.rcfg <https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/config_files/grlsd-on-archer/archer.rcfg>`_ directly.)


    .. note::   Change the following values according to your needs :

                * UNAME
                * ALLOCATION

    ::

        REMOTE_HOST = 'archer.ac.uk'              # Label/Name of the Remote Machine
        UNAME       = 'username'                  # Username on the Remote Machine
        ALLOCATION  = 'e290'                      # Allocation to be charged
        WALLTIME    = 60                          # Walltime to be requested for the pilot
        PILOTSIZE   = 24                          # Number of cores to be reserved
        WORKDIR     = None                        # Working directory on the remote machine
        QUEUE       = 'standard'                  # Name of the queue in the remote machine

        DBURL       = 'mongodb://extasy:extasyproject@extasy-db.epcc.ed.ac.uk/radicalpilot'

**Step 3** : Download the sample input data:

    ::

        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-archer/config.ini
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-archer/grompp.mdp
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-archer/input.gro
        curl -k -O https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/input_files/grlsd-on-archer/topol.top



**Step 4** : Create a new workload configuration file ``gromacslsdmap.wcfg`` :

    (Download it `gromacslsdmap.wcfg <https://raw.githubusercontent.com/radical-cybertools/ExTASY/master/config_files/grlsd-on-archer/gromacslsdmap.wcfg>`_ directly.)

    ::

        #-------------------------Applications----------------------
        simulator             = 'Gromacs'           # Simulator to be loaded
        analyzer              = 'LSDMap'            # Analyzer to be loaded

        #--------------------------General--------------------------------
        num_CUs              = 24                   # Number of tasks or Compute Units
        num_iterations       = 2                    # Number of iterations of Simulation-Analysis
        start_iter           = 0                    # Iteration number with which to start
        nsave                = 1                    # # Iterations after which output is transfered to local machine

        #--------------------------Simulation--------------------------------
        num_cores_per_sim_cu = 1                    # Number of cores per Simulation Compute Units
        md_input_file        = './input.gro'        # Entire path to the MD Input file - Do not use $HOME or the likes
        mdp_file             = './grompp.mdp'       # Entire path to the MD Parameters file - Do not use $HOME or the likes
        top_file             = './topol.top'        # Entire path to the Topology file - Do not use $HOME or the likes
        ndx_file             = None                   # Entire path to the Index file - Do not use $HOME or the likes
        grompp_options       = None                   # Command line options for when grompp is used
        mdrun_options        = None                   # Command line options for when mdrun is used
        itp_file_loc         = None                   # Entire path to the location of .itp files - Do not use $HOME or the likes
        md_output_file       = 'tmp.gro'            # Filename to be used for the simulation output

        #--------------------------Analysis----------------------------------
        lsdm_config_file     = './config.ini'       # Entire path to the LSDMap configuration file - Do not use $HOME or the likes
        num_runs             = 100                # Number of runs to be performed in the Selection step in Analysis
        w_file               = 'weight.w'           # Filename to be used for the weight file
        max_alive_neighbors  = '10'                 # Maximum alive neighbors to be considered while reweighting
        max_dead_neighbors   = '1'                  # Maximum dead neighbors to be considered while reweighting



**Now you are can run the workload using :**

    ::

        EXTASY_DEBUG=True RADICAL_PILOT_VERBOSE='debug' SAGA_VERBOSE='debug' extasy --RPconfig archer.rcfg --Kconfig gromacslsdmap.wcfg 2> extasy.log

A **sample output** with expected callbacks and simulation/analysis can be found at `here <https://github.com/radical-cybertools/ExTASY/tree/master/sample_output_logs/grlsd-on-archer>`_.

+------------------------+----------------+--------------+
|     Stage              |   Simulation   |   Analysis   |
+========================+================+==============+
| Expected TTC/iteration |    200-350 s   |     ~30 s    |
+------------------------+----------------+--------------+


There are two stages in the execution phase - Simulation and Analysis. Execution starts
with any Preprocessing that might be required on the input data and then moves to
Simulation stage. In the Simulation stage, a number of tasks (num_CUs) are launched to
execute on the target machine. The number of tasks set to execute depends on the PILOTSIZE,
num_CUs, num_cores_per_sim_cu, the number of tasks in execution state simultaneously would
be PILOTSIZE/num_cores_per_sim_cu. As each task attains 'Done' (completed) state, the
remain tasks are scheduled till all the num_CUs tasks are completed.

This is followed by the Analysis stage, one task is scheduled on the target machine which
takes all the cores as the PILOTSIZE to perform the analysis and returns the data required
for the next iteration of the Simulation stage. As can be seen, per iteration, there are
(num_CUs+1) tasks executed.