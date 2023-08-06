#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# transfert_interfaces.py
#
# This file is part of pymls, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2017
# 	Olivier Dazel <olivier.dazel@univ-lemans.fr>
# 	Mathieu Gaborit <gaborit@kth.se>
# 	Peter Göransson <pege@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import numpy as np


def fluid_pem_interface(O):
    raise NotImplementedError

    a = -np.array([
        [O[0,1],O[0,2]],
        [O[3,1],O[3,2]]
    ])
    Tau = np.dot(np.linalg.inv(a), np.array([[O[0,0]], [O[3,0]]]))
    Tau_tilde = np.concatenate([np.eye(1),Tau])

    Omega_moins = np.array([[O[2,0]], [O[4,0]]]) + np.dot(np.array([[O[2,1], O[2,2]], [O[4,1], O[4,2]]]), Tau)

    return (Omega_moins, Tau_tilde)


def pem_fluid_interface(O):
    raise NotImplementedError

    Omega_moins = np.zeros((6,3), dtype=np.complex)
    Omega_moins[1,1] = 1
    Omega_moins[2,0] = O[0,0]
    Omega_moins[4,0] = O[1,0]
    Omega_moins[5,2] = 1

    Tau_tilde = np.zeros((1,3), dtype=np.complex)
    Tau_tilde[0,0] = 1

    return (Omega_moins, Tau_tilde)


def elastic_fluid_interface(O):

    Omega_moins = np.zeros((2,2), dtype=np.complex)
    Omega_moins[0,0] = O[0,0]
    Omega_moins[1,0] = -O[1,0]

    Tau_tilde = np.zeros((1,1), dtype=np.complex)

    print(Omega_moins.shape)
    return (Omega_moins, Tau_tilde)


def fluid_elastic_interface(O):

    Tau = -O[0,0]/O[0,1]
    Omega_moins = np.array([[O[1,1]], [-O[2,1]]])*Tau + np.array([[O[1,0]], [-O[2,0]]])
    Tau_tilde = np.concatenate([np.eye(1,1), np.array([[Tau]])])

    return (Omega_moins, Tau_tilde)


def pem_elastic_interface(O):
    raise NotImplementedError

    Omega_moins = np.zeros((6,3), dtype=np.complex)
    Omega_moins[0,0:2] = O[0,0:2]
    Omega_moins[1,0:2] = O[1,0:2]
    Omega_moins[2,0:2] = O[1,0:2]
    Omega_moins[3,0:2] = O[2,0:2]
    Omega_moins[3,2] = 1
    Omega_moins[4,2] = 1
    Omega_moins[5,0:2] = O[3,0:2]

    Tau_tilde = np.zeros((2,3), dtype=np.complex)
    Tau_tilde[0,0] = 1
    Tau_tilde[1,1] = 1
    return (Omega_moins, Tau_tilde)


def elastic_pem_interface(O):
    raise NotImplementedError

    Dplus = np.array([0, 1, -1, 0, 0, 0])
    Dmoins = np.zeros((4,6), dtype=np.complex)
    Dmoins[0,0] = 1
    Dmoins[1,1] = 1
    Dmoins[2,3] = 1
    Dmoins[2,4] = -1
    Dmoins[3,5] = 1
    Tau = -Dplus.dot(O[:,2:4])**-1 * np.dot(Dplus, O[:,0:2])

    Omega_moins = Dmoins.dot(O[:,0:2] + O[:,2:4]*Tau)

    Tau_tilde = np.vstack([np.eye(2), Tau])

    return (Omega_moins, Tau_tilde)
