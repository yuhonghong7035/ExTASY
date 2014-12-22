__author__ = 'vivek'

import radical.pilot
from radical.ensemblemd.mdkernels import MDTaskDescription
import os
import time
import saga
import sys


def Simulator(umgr,RPconfig,Kconfig,cycle,paths):


    print 'Starting Simulation'

    if (Kconfig.num_cores_per_sim_cu < 2):
        print 'Amber MPI requires num_cores_per_sim_cu to be greater than or equal to 2'
        sys.exit(1)

    dict = {}
    dict['crdfile'] = Kconfig.initial_crd_file
    dict['crdfilename'] = os.path.basename(dict['crdfile'])
    dict['topfile'] = Kconfig.top_file
    dict['topfilename'] = os.path.basename(dict['topfile'])
    dict['mdin']    = Kconfig.md_input_file
    dict['mdinfilename'] = os.path.basename(dict['mdin'])
    dict['minin']   = Kconfig.minimization_input_file
    dict['mininfilename'] = os.path.basename(dict['minin'])
    dict['cycle'] = cycle

    start_times = []
    end_times = []

    cudesc_list_A = []
    for i in range(Kconfig.num_CUs):

        mdtd = MDTaskDescription()
        mdtd.kernel = "AMBER"
        mdtd.arguments = ['-O','-i',dict['mininfilename'],'-o','min%s.out'%cycle,'-inf','min%s.inf'%cycle,'-r',
                          'md%s.crd'%cycle,'-p',dict['topfilename'],'-c','min%s.crd'%cycle,'-ref','min%s.crd'%cycle]
        mdtd_bound = mdtd.bind(resource=RPconfig.REMOTE_HOST)
        cu = radical.pilot.ComputeUnitDescription()
        cu.cores = Kconfig.num_cores_per_sim_cu
        cu.mpi = True
        cu.executable = mdtd_bound.executable
        cu.pre_exec = mdtd_bound.pre_exec
        cu.arguments = mdtd_bound.arguments
        if(cycle==0):
            cu.pre_exec = cu.pre_exec + ['ln %s/%s min%s.crd'%(paths[0],dict['crdfilename'],cycle),'ln %s/%s .'%(paths[0],dict['topfilename']),'ln %s/%s .'%(paths[0],dict['mininfilename'])]
        else:
            cu.pre_exec = cu.pre_exec + ['ln %s/min%s%s.crd min%s.crd'%(paths[cycle],cycle,i,cycle),'ln %s/%s .'%(paths[0],dict['topfilename']),'ln %s/%s .'%(paths[0],dict['mininfilename'])]
        cudesc_list_A.append(cu)

    cu_list_A = umgr.submit_units(cudesc_list_A)

    cu_list_B = []

    cu_list_A_copy = cu_list_A[:]

    i=0
    while cu_list_A:
        for cu_a in cu_list_A:
            cu_a.wait ()
            path=saga.Url(cu_a.working_directory).path

            mdtd = MDTaskDescription()
            mdtd.kernel = "AMBER"
            mdtd.arguments = ['-O','-i',dict['mdinfilename'],'-o','md%s.out'%cycle,'-inf','md%s.inf'%cycle,
                              '-x','md%s.ncdf'%cycle,'-r','md%s.rst'%cycle,'-p',dict['topfilename'],'-c','md%s.crd'%cycle]
            mdtd_bound = mdtd.bind(resource=RPconfig.REMOTE_HOST)
            cudesc = radical.pilot.ComputeUnitDescription()
            cudesc.cores = Kconfig.num_cores_per_sim_cu
            cudesc.mpi = True
            cudesc.executable = mdtd_bound.executable
            cudesc.pre_exec = ['ln %s/* .'%path] + mdtd_bound.pre_exec
            cudesc.arguments = mdtd_bound.arguments
            #cudesc.input_staging = [dict['mdin']]
            cudesc.pre_exec = cudesc.pre_exec + ['ln %s/%s .'%(paths[0],dict['mdinfilename'])]
            if((cycle+1)%Kconfig.nsave==0):
                cudesc.output_staging = ['md%s.ncdf > md_%s_%s.ncdf'%(cycle,cycle,i)]
            cudesc.post_exec = ['ln md%s.ncdf %s/md_%s_%s.ncdf'%(cycle,paths[cycle],cycle,i)]
            cu_b = umgr.submit_units(cudesc)
            i+=1
            cu_list_B.append(cu_b)
            cu_list_A.remove(cu_a)

    for cu_b in cu_list_B:
        cu_b.wait()

    try:
        for unit_a in cu_list_A_copy:
            start_times.append(unit_a.start_time)

        for unit_b in cu_list_B:
            end_times.append(unit_b.stop_time)

        print 'Simulation Execution Time : ', (max(end_times)-min(start_times)).total_seconds()

    except:
        pass

