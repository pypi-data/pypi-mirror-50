from ndx_spectrum import Spectrum
from datetime import datetime
from pynwb import NWBFile, NWBHDF5IO

nwb = NWBFile('session_description', 'identifier', datetime.now().astimezone())

spectrum = Spectrum('test_spectrum', frequencies=[1., 2., 3.],
                    power=[1., 2., 3.],
                    phase=[1., 2., 3.])

with NWBHDF5IO('test_spectrum.nwb', 'w') as io:
    io.write(nwb)

with NWBHDF5IO('test_spectrum.nwb', 'r', load_namespaces=True) as io:
    io.read()
