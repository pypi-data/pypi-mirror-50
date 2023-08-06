#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org

from cortix.src.module import Module
from cortix.src.cortix_main import Cortix

from cortix.examples.dataplot import DataPlot
from cortix.examples.droplet import Droplet
from cortix.examples.vortex import Vortex

'''
This example uses three modules instantiated many times in two different networks.
Each network configuration uses a different amount of module instances and a different
network topology. This example can be executed with MPI (if mpi4py is available) or
with the Python multiprocessing library. These choices are made by variables listed
below in the executable portion of this run file.

Single Plot
-----------

The first network case is named "single plot". Here one DataPlot module is connected
to all Droplet modules. To run this case using MPI you should compute the number of
processes as follows:

    `nprocs = n_droplets + 1 vortex + 1 data_plot + 1 cortix`

then issue the MPI run command as follows (replace `nprocs` with a number):

     `mpiexec -n nprocs run_droplet.py`

To run this case with the Python multiprocessing library, just run this file at the
command line as

     `run_droplet.py`

Multiple Plot
-------------

The second network case is named "multiple plot". Here each Droplet is connected to an
instance of the DataPlot module, therefore many more nodes are added to the network
when compared to the first network case. To run this case using MPI compute

    `nprocs = 2*n_droplets + 1 vortex + 1 cortix`

then issue the MPI run command as follows (replace `nprocs`:

    `mpiexec -n nprocs run_droplet.py`

To run this case with the Python multiprocessing library, just run this file at the
command line as

    `run_droplet.py`
'''

if __name__ == '__main__':

    # Configuration Parameters
    use_single_plot = True  # True for a single plot output
                            # False for multiple plot files and network
    use_mpi         = False # True for MPI; False for Python multiprocessing

    plot_vortex_profile = False # True may crash the X server.

    n_droplets = 5
    end_time   = 300
    time_step  = 0.1

    cortix = Cortix(use_mpi=use_mpi)

    # Network for a single plot case
    if use_single_plot:

        # Vortex module (single).
        vortex = Vortex()
        cortix.add_module(vortex)
        vortex.show_time = (True,100)
        vortex.end_time = end_time
        vortex.time_step = time_step
        if plot_vortex_profile:
            vortex.plot_velocity()

        # DataPlot module (single).
        data_plot = DataPlot()
        cortix.add_module(data_plot)
        data_plot.title = 'Droplet Trajectories'
        data_plot.same_axes = True
        data_plot.dpi = 300

        for i in range(n_droplets):

            # Droplet modules (multiple).
            droplet = Droplet()
            cortix.add_module(droplet)
            droplet.end_time = end_time
            droplet.time_step = time_step
            droplet.bounce = False
            droplet.slip = False

            # Network port connectivity (connect modules through their ports)
            droplet.connect('external-flow', vortex.get_port('fluid-flow:{}'.format(i)))
            droplet.connect('visualization', data_plot.get_port('viz-data:{:05}'.format(i)))

    # Network for a multiple plot case
    if not use_single_plot:

        # Vortex module (single).
        vortex = Vortex()
        cortix.add_module(vortex)
        vortex.show_time = (True,100)
        vortex.end_time = end_time
        vortex.time_step = time_step
        if plot_vortex_profile:
            vortex.plot_velocity()

        for i in range(n_droplets):

            # Droplet modules (multiple).
            droplet = Droplet()
            cortix.add_module(droplet)
            droplet.end_time = end_time
            droplet.time_step = time_step
            droplet.bounce = False
            droplet.slip = False

            # DataPlot modules (multiple).
            data_plot = DataPlot()
            cortix.add_module(data_plot)
            data_plot.title = 'Droplet Trajectory '+str(i)
            data_plot.dpi = 300

            # Network port connectivity (connect modules through their ports)
            droplet.connect('external-flow', vortex.get_port('fluid-flow:{}'.format(i)))
            droplet.connect('visualization', data_plot.get_port('viz-data:{:05}'.format(i)))

    cortix.draw_network('network.png')

    cortix.run()
