#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment.
# https://cortix.org

import pickle

import numpy as np
import scipy.constants as const
from scipy.integrate import odeint
from cortix.src.module import Module
from cortix.support.phase import Phase
from cortix.support.quantity import Quantity

class Probation(Module):
    '''
    Probation Cortix module used to model criminal group population in a probation.

    Note
    ----
    `adjudication`: this is a `port` for the rate of population groups to/from the
        Adjudication domain module.

    `arrested`: this is a `port` for the rate of population groups to/from the
        Arrested domain module.

    `jail`: this is a `port` for the rate of population groups to/from the
        Jail domain module.

    `community`: this is a `port` for the rate of population groups to/from the Community
        domain module.

    `visualization`: this is a `port` that sends data to a visualization module.
    '''

    def __init__(self, n_groups=1, pool_size=0.0):

        super().__init__()

        quantities      = list()
        self.ode_params = dict()

        self.initial_time = 0.0 * const.day
        self.end_time     = 100 * const.day
        self.time_step    = 0.5 * const.day

        # Population groups
        self.n_groups = n_groups

        # Probation population groups
        fbg_0 = np.random.random(self.n_groups) * pool_size
        fbg = Quantity(name='fbg', formalName='probation-pop-grps',
                unit='individual', value=fbg_0)
        quantities.append(fbg)

        # Model parameters: commitment coefficients and their modifiers

        # Probation to community
        cb0g_0 = np.random.random(self.n_groups) / const.day
        cb0g = Quantity(name='cb0g', formalName='commit-community-coeff-grps',
               unit='individual', value=cb0g_0)
        self.ode_params['commit-to-community-coeff-grps'] = cb0g_0
        quantities.append(cb0g)

        mb0g_0 = np.random.random(self.n_groups)
        mb0g = Quantity(name='mb0g', formalName='commit-community-coeff-mod-grps',
               unit='individual', value=mb0g_0)
        self.ode_params['commit-to-community-coeff-mod-grps'] = mb0g_0
        quantities.append(mb0g)

        # Probation to jail
        cbjg_0 = np.random.random(self.n_groups) / const.day
        cbjg = Quantity(name='cbjg', formalName='commit-jail-coeff-grps',
               unit='individual', value=cbjg_0)
        self.ode_params['commit-to-jail-coeff-grps'] = cbjg_0
        quantities.append(cbjg)

        mbjg_0 = np.random.random(self.n_groups)
        mbjg = Quantity(name='mbjg', formalName='commit-jail-coeff-mod-grps',
               unit='individual', value=mbjg_0)
        self.ode_params['commit-to-jail-coeff-mod-grps'] = mbjg_0
        quantities.append(mbjg)

        # Death term
        self.ode_params['probation-death-rates'] = np.zeros(self.n_groups)

        # Phase state
        self.population_phase = Phase(self.initial_time, time_unit='s',
                quantities=quantities)

        self.population_phase.SetValue('fbg', fbg_0, self.initial_time)

        # Set the state to the phase state
        self.state = self.population_phase

        return

    def run(self, state_comm=None, idx_comm=None):

        time = self.initial_time

        while time < self.end_time:

            # Interactions in the jail port
            #------------------------------
            # one way "to" jail

            message_time = self.recv('jail')
            outflow_rates = self.compute_outflow_rates( message_time, 'jail' )
            self.send( (message_time, outflow_rates), 'jail' )

            # Interactions in the adjudication port
            #------------------------------------
            # one way "from" adjudication

            self.send( time, 'adjudication' )
            (check_time, adjudication_inflow_rates) = self.recv('adjudication')
            assert abs(check_time-time) <= 1e-6
            self.ode_params['adjudication-inflow-rates'] = adjudication_inflow_rates

            # Interactions in the arrested port
            #----------------------------------
            # one way "from" arrested

            self.send( time, 'arrested' )
            (check_time, arrested_inflow_rates) = self.recv('arrested')
            assert abs(check_time-time) <= 1e-6
            self.ode_params['arrested-inflow-rates'] = arrested_inflow_rates

            # Interactions in the community port
            #------------------------------
            # one way "to" community

            message_time = self.recv('community')
            outflow_rates = self.compute_outflow_rates( message_time, 'community' )
            self.send( (message_time, outflow_rates), 'community' )

            # Interactions in the visualization port
            #---------------------------------------

            fbg = self.population_phase.GetValue('fbg')
            self.send( fbg, 'visualization' )

            # Evolve probation group population to the next time stamp
            #---------------------------------------------------------

            time = self.step( time )

        self.send('DONE', 'visualization') # this should not be needed: TODO

        if state_comm:
            try:
                pickle.dumps(self.state)
            except pickle.PicklingError:
                state_comm.put((idx_comm,None))
            else:
                state_comm.put((idx_comm,self.state))

    def rhs_fn(self, u_vec, t, params):

        fbg = u_vec  # probation population groups

        arrested_inflow_rates     = params['arrested-inflow-rates']
        adjudication_inflow_rates = params['adjudication-inflow-rates']

        inflow_rates  = arrested_inflow_rates + adjudication_inflow_rates

        cb0g = self.ode_params['commit-to-community-coeff-grps']
        mb0g = self.ode_params['commit-to-community-coeff-mod-grps']

        cbjg = self.ode_params['commit-to-jail-coeff-grps']
        mbjg = self.ode_params['commit-to-jail-coeff-mod-grps']

        outflow_rates = ( cb0g * mb0g + cbjg * mbjg ) * fbg

        death_rates = params['probation-death-rates']

        dt_fbg = inflow_rates - outflow_rates - death_rates

        return dt_fbg

    def step(self, time=0.0):
        r'''
        ODE IVP problem:
        Given the initial data at :math:`t=0`,
        :math:`u = (u_1(0),u_2(0),\ldots)`
        solve :math:`\frac{\text{d}u}{\text{d}t} = f(u)` in the interval
        :math:`0\le t \le t_f`.

        Parameters
        ----------
        time: float
            Time in the droplet unit of time (seconds).

        Returns
        -------
        None
        '''

        u_vec_0 = self.population_phase.GetValue('fbg', time)
        t_interval_sec = np.linspace(0.0, self.time_step, num=2)

        (u_vec_hist, info_dict) = odeint(self.rhs_fn,
                                         u_vec_0, t_interval_sec,
                                         args=( self.ode_params, ),
                                         rtol=1e-4, atol=1e-8, mxstep=200,
                                         full_output=True)

        assert info_dict['message'] =='Integration successful.', info_dict['message']

        u_vec = u_vec_hist[1,:]  # solution vector at final time step
        values = self.population_phase.GetRow(time) # values at previous time

        time += self.time_step

        self.population_phase.AddRow(time, values)

        # Update current values
        self.population_phase.SetValue('fbg', u_vec, time)

        return time

    def compute_outflow_rates(self, time, name):

        fbg = self.population_phase.GetValue('fbg',time)

        if name == 'jail':

            cbjg = self.ode_params['commit-to-jail-coeff-grps']
            mbjg = self.ode_params['commit-to-jail-coeff-mod-grps']

            outflow_rates = cbjg * mbjg * fbg

            return outflow_rates

        if name == 'community':

            cb0g = self.ode_params['commit-to-community-coeff-grps']
            mb0g = self.ode_params['commit-to-community-coeff-mod-grps']

            outflow_rates = cb0g * mb0g * fbg

            return outflow_rates
