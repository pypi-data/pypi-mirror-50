========================
Transient Simulation
========================

After the steady state calculation is completed, TSNet adopts
the Method of Characteristics (MOC)
for solving governing transient flow equations.
A transient simulation can be run using the following code:

.. literalinclude:: ../examples/Tnet1_valve_closure.py
    :lines: 27-28

The results will be returned to the transient model (tm) object,
and then stored in the 'Tnet1.obj' file for the easiness of retrieval.


Mass and Momentum Conservation
-------------------------------
The transient flow is govenred by the mass and monmentum conservation
equation [WYSS93]_:

.. math::
    \frac{\partial H}{\partial t} + \frac{a^2}{g} \frac{\partial V}{\partial t} - gV\sin \alpha = 0

    \frac{\partial V}{\partial t} + g\frac{\partial H}{\partial t} + h_f = 0

where
:math:`H` is the piezometric head,
:math:`V` is the flow velocity in the pipe,
:math:`t` is time,
:math:`a` is the wave speed,
:math:`g` is the gravity acceleration,
:math:`\alpha` is the angle from horizontal,
and :math:`h_f` represents the head loss.

Method of Characteristics (MOC)
-------------------------------
The Method of Characteristics (MOC) method is used to solve the system of
governing equations above. The essence of MOC is to transform the set of
partial differential equations to an equivalent set of ordinary differential
equations that apply along specific lines, i.e., characteristics lines,
as shown below [LAJW99]_:

.. math::
    \frac{dV}{dt} + \frac{g}{a} \frac{dH}{dt} + h_f - gV\sin(\alpha) = 0
    \text{  only when  } \frac{dx}{dt} = a

    \frac{dV}{dt} - \frac{g}{a} \frac{dH}{dt} + h_f - gV\sin(\alpha) = 0
    \text{  only when  } \frac{dx}{dt} = -a

The explicit MOC technique is then adopted to solve the above systems of
equations along the characteristics lines [LAJW99]_.

Headloss in Pipes
---------------------

TSNet adopts Darcy-Weisbach equation to compute head loss, regardless of the
friction method defined in the EPANet .inp file. This package computes
Darcy-Weisbach coefficients (:math:`f`) based on the head loss
(:math:`{h_f}_0`) and flow velocity (:math:`V_0`) in initial condition,
using the following equation:

.. math::
    f = \frac{{h_f}_0}{(L/D)(V_0^2/2g)}

where
:math:`L` is the pipe length,
:math:`D` is the pipe diameter,
and :math:`g` is gravity acceleration.

Subsequently, in transient simulation the headloss (:math:`h_f`) is calculated
based on the following equation:

.. math::
    h_f = f\frac{L}{D}\frac{V^2}{2g}

Pressure-driven Demand
----------------------

During the transient simulation in TSNet, the demands are treated as pressure-
dependent discharge, thus indicating that the actual demands are not
equivalent to the demands defined in the INP file.

The actual demands (:math:`D_{actual}`) are modeled based on the
instantaneous pressure head, and the demand discharge coefficients,
using the following equation:

.. math::
    D_{actual} = k \sqrt{H_p}

where :math:`H_p` is the pressure head
(not the piezometric head (:math:`H`, :math:`H=H_p+elevation`)
and :math:`k` is the demand discharge coefficient,
which is calculated from the initial demand (:math:`D_0`) and head (:math:`H_0`):

.. math::
    k = \frac{D_0}{\sqrt{{H_p}_0}}

It should be noted that if the pressure head is negative, the demand flow will be
treated zero, assuming that a backflow preventer exists on each node.


Choice of Time Step
-----------------------

The determination of time step in MOC is not a trivial task. There are two
constraints that have to be satisfied simultaneously:

1.  The Courant's criterion has to be satisfied for each pipe,
    indicating the maximum time step allowed in the network transient analysis
    will be:

.. math::
    \Delta t \leqslant \min{(\frac{L_i}{N_i a_i})} \text{,       }
    i = 1 \text{, } 2 \text{, ..., } n_p

2.  The time step has to be the same for any pipe in the network, therefore
    restricting the wave travel time :math:`\frac{L_i}{N_ia_i}` to be the same
    for any computational unit in the network. However, this is not the
    realistic situation in a real network, because different pipe lengths
    and wave speeds usually cause different wave travel times. Moreover,
    the number of sections in the :math:`i^{th}` pipe (:math:`N_i`) has to
    be an even integer due to the grid configuration in MOC; however, the
    combination of time step and pipe length is likely to produce
    non-integer value of :math:`N_i`, which then requires further adjustment.

This package adopted the wave speed adjustment scheme  [WYSS93]_ to make
sure the two criterion stated above are satisfied.

To begin with, the maximum allowed time step (:math:`{\Delta t}_{max}`) is
calculated, assuming there are two computation segments on the shortest pipe:

.. math::
    \Delta t_{max} = \min{\frac{L_i}{2a_i}} \text{,       }
    i = 1 \text{, } 2 \text{, ..., } n_p

If the user defined time step is greater than :math:`{\Delta t}_{max}`, a
fatal error will be raised and the program will be killed; if not, the
user defined value will be used as the initial guess for the upcoming
adjustment.

.. literalinclude:: ../examples/Tnet1_valve_closure.py
    :lines: 9-11

It is acknowledged that the determination of time step might not be
straightforward, especially in large networks. Thus, we allow the user
to ignore the time step setting, and if that is the case,
:math:`{\Delta t}_{max}` will be used as the initial guess for the upcoming adjustment.

All the steps after this will then happen behind the scene. Firstly,
the :math:`i^{th}` pipes (:math:`p_i`) with length (:math:`L_i`) and wave
speed (:math:`a_i`) will be discretized into (:math:`N_i`) segments:

.. math::
    N_i = 2\text{int}\frac{L_i}{a_i \Delta t} \text{,       }
    i = 1 \text{, } 2 \text{, ..., } n_p

Furthermore, the discrepancies introduced by the rounding of :math:`N_i`
can be compensated by correcting the wave speed (:math:`a_i`).

.. math::
    \Delta t = \min{\frac{L_i}{a_i(1 \pm \phi_i)N_i}} \text{,       }
    i = 1 \text{, } 2 \text{, ..., } n_p

Least squares approximation is then used to determine :math:`\Delta t`
such that the sum of squares of the wave speed adjustments
(:math:`\sum{{\phi_i}^2}`) is minimized. Ultimately, an adjusted
:math:`\Delta t` can be determined and then used in the transient simulation.

It should be noted that even if the user defined time step satisfied the
Courant's criterion, it will still be adjusted.


Valve Operation (Closure and Opening)
-------------------------------------

.. Two types of valve are included in TSNet: end valve, located on the boundary
    of a network, and inline valve, located in the middle of the network and
    connected by one pipe on each end.

Valve operations, including closure and opening, are supported in TSNet.
The default valve shape is gate valve, the valve characteristics curve
of which is defined according to [STWV96]_.
The following examples illustrate how to operate valve.

Valve closure can be simulated by defining
the valve closure start time (:math:`ts`),
the closure duration (:math:`t_c`),
the valve open percentage when the closure is completed b (:math:`se`),
and the closure constant (:math:`m`), which characterize
the shape of the closure curve.
These parameters essentially defines the valve closure cure.
For example, using the code below will yield the blue curve
shown in :numref:`valve_closure`.
If the closure constant (:math:`m`) is
instead set to be :math:`2`, the valve curve will then correspond to the
orange curve in :numref:`valve_closure`.


.. code:: python

  tc = 1 # valve closure period [s]
  ts = 0 # valve closure start time [s]
  se = 0 # end open percentage [s]
  m = 1 # closure constant [dimensionless]
  valve_op = [tc,ts,se,m]
  tm.valve_closure('VALVE',valve_op)

.. _valve_closure:
.. figure:: figures/valve_closure.png
   :width: 600
   :alt: valve_closure

Furthermore, valve opening can be simulated by defining a similar set of
parameters related to the valve opening curve. The valve opening curves
with :math:`m=1` and :math:`m=2` are illustrated in :numref:`valve_opening`.

.. code:: python

  tc = 1 # valve opening period [s]
  ts = 0 # valve opening start time [s]
  se = 1 # end open percentage [s]
  m = 1 # opening constant [dimensionless]
  valve_op = [tc,ts,se,m]
  tm.valve_opening('VALVE',valve_op)


.. _valve_opening:
.. figure:: figures/valve_opening.png
   :width: 600
   :alt: valve_opening


Pump Operation (Shut-off and Start-up)
--------------------------------------
The TSNet also includes the capacity to perform controlled pump operations
by specifying the relation between pump rotation speed and time.
However, pump shut-off due to power failure has not been included yet.

The following example shows how to add pump shut-off event to the network:

.. literalinclude:: ../examples/Tnet2_pump_shutdown.py
    :lines: 13-18

where the parameters are defined in the same manner as in valve closure.
Correspondingly, the controlled pump opening can be simulated using:

.. code:: python

  tc = 1 # pump opening period [s]
  ts = 0 # pump opening start time [s]
  se = 1 # end open percentage [s]
  m = 1 # opening constant [dimensionless]
  pump_op = [tc,ts,se,m]
  tm.pump_start_up('PUMP2',pump_op)

It should be noted that a check valve is assumed in each pump, indicating
that the reverse flow will be stopped by the check valve immediately.


Leakage
--------

In TSNet, leaks and burst are assigned to the junctions. The leak is
defined by specifying the leaking node name and the emitter coefficient
(:math:`k`):

.. literalinclude:: ../examples/Tnet3_burst_leak.py
    :lines: 15-16

The leakage needs to be included in the initial condition solver; thus, it is
necessary to define the leakage before performing the initial condition
calculation. During the transient simulation, the leaking node is modeled
using the two compatibility equations, a continuity equation, and an orifice
equation which quantifies the leakage discharge (:math:`Q_l`):

.. math::
    Q_l = k \sqrt{{H_p}_l}

where :math:`{H_p}_l` is the pressure head at the leakage node.
It should be noted that :math:`{H_p}_l` is the pressure head
not the piezometric head (:math:`H = H_p +elevation`).
Moreover, if the pressure head is negative, the leakage discharge
will be set to zero, assuming a backflow preventer is installed
on the leakage node.


Burst
-----
The simulation of burst and leakage is very similar. They shared the
same set of governing equations. The only difference is that the burst opening
is simulated only during the transient calculation and not included in the
initial condition calculation. In TSNet, the burst is assumed to be developed
linearly, indicating that the burst area increases linearly from zero to the
a specific size during a certain time period.
Thus, a burst event can be added by defined the start and end time of the
burst development process and the final emitter coefficient when the burst
is fully developed:

.. literalinclude:: ../examples/Tnet3_burst_leak.py
    :lines: 19-22



