#!/usr/bin/env python

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr  = rp.PilotManager(session=session)
        umgr  = rp.UnitManager(session=session)


        pdesc = rp.ComputePilotDescription({'resource'      : 'local.localhost',
                                            'runtime'       : 60,
                                            'exit_on_error' : True,
                                            'cores'         : 2})
        pilot = pmgr.submit_pilots(pdesc)
        umgr.add_pilots(pilot)

        cuds = list()
        for i in range(8):
            cud = rp.ComputeUnitDescription()
            cud.executable       = '/bin/date'
            cud.stdout           = 'date.out'
            cud.output_staging   = [{'source' : 'unit:///date.out',
                                     'target' : 'client:///out/cu.%04d.out' % i,
                                     'action' : rp.TRANSFER}
                                   ]
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

