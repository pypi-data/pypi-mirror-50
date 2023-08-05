# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['unrolr',
 'unrolr.core',
 'unrolr.feature_extraction',
 'unrolr.plotting',
 'unrolr.sampling',
 'unrolr.utils']

package_data = \
{'': ['*']}

install_requires = \
['MDAnalysis>=0.17.0',
 'h5py>=2.5.0',
 'matplotlib>=1.4.3',
 'numpy>=1.11.3',
 'pandas>=0.17.1',
 'pyopencl>=2015.1']

setup_kwargs = {
    'name': 'unrolr',
    'version': '0.4.0.6',
    'description': 'Dimensionality reduction method for MD trajectories',
    'long_description': '# Unrolr\nConformational analysis of MD trajectories based on (pivot-based) Stochastic Proximity Embedding using dihedral distance as a metric (https://github.com/jeeberhardt/unrolr).\n\n## Prerequisites\n\nYou need, at a minimum (requirements.txt):\n\n* Python 2.7 or python 3\n* NumPy\n* H5py\n* Pandas\n* Matplotlib\n* PyOpenCL\n* MDAnalysis (>=0.17)\n\n## Installation on UNIX (Debian/Ubuntu)\n\nI highly recommand you to install the Anaconda distribution (https://www.continuum.io/downloads) if you want a clean python environnment with nearly all the prerequisites already installed (NumPy, H5py, Pandas, Matplotlib).\n\n1 . First, you have to install OpenCL:\n* MacOS: Good news, you don\'t have to install OpenCL, it works out-of-the-box. (Update: bad news, OpenCL is now depreciated in macOS 10.14. Thanks Apple.)\n* AMD:  You have to install the [AMDGPU graphics stack](https://amdgpu-install.readthedocs.io/en/amd-18.30/index.html).\n* Nvidia: You have to install the [CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\n* Intel: And of course it\'s working also on CPU just by installing this [runtime software package](https://software.intel.com/en-us/articles/opencl-drivers). Alternatively, the CPU-based OpenCL driver can be also installed through the package ```pocl``` (http://portablecl.org/) with the conda package manager.\n\nFor any other informations, the official installation guide of PyOpenCL is available [here](https://documen.tician.de/pyopencl/misc.html).\n\n2 . As a final step, installation from PyPi server\n```bash\npip install unrolr\n```\n\nOr from the source\n\n```bash\n# Get the package\nwget https://github.com/jeeberhardt/unrolr/archive/master.zip\nunzip unrolr-master.zip\nrm unrolr-master.zip\ncd unrolr-master\n\n# Install the package\npython setup.py install\n```\n\nAnd if somehow pip is having problem to install all the dependencies,\n```bash\nconda config --append channels conda-forge\nconda install pyopencl mdanalysis\n\n# Try again\npython setup.py install\n```\n\n## OpenCL context\n\nBefore running Unrolr, you need to define the OpenCL context. And it is a good way to see if everything is working correctly.\n\n```bash\npython -c \'import pyopencl as cl; cl.create_some_context()\'\n```\n\nHere in my example, I have the choice between 3 differents computing device (2 graphic cards and one CPU). \n\n```bash\nChoose platform:\n[0] <pyopencl.Platform \'AMD Accelerated Parallel Processing\' at 0x7f97e96a8430>\nChoice [0]:0\nChoose device(s):\n[0] <pyopencl.Device \'Tahiti\' on \'AMD Accelerated Parallel Processing\' at 0x1e18a30>\n[1] <pyopencl.Device \'Tahiti\' on \'AMD Accelerated Parallel Processing\' at 0x254a110>\n[2] <pyopencl.Device \'Intel(R) Core(TM) i7-3820 CPU @ 3.60GHz\' on \'AMD Accelerated Parallel Processing\' at 0x21d0300>\nChoice, comma-separated [0]:1\nSet the environment variable PYOPENCL_CTX=\'0:1\' to avoid being asked again.\n```\n\nNow you can set the environment variable.\n\n```bash\nexport PYOPENCL_CTX=\'0:1\'\n```\n\n## Example\n\n```python\nfrom __future__ import print_function\n\nfrom unrolr import Unrolr\nfrom unrolr.feature_extraction import Dihedral\nfrom unrolr.utils import save_dataset\n\n\ntop_file = \'examples/inputs/villin.psf\'\ntrj_file = \'examples/inputs/villin.dcd\'\n\n# Extract all calpha dihedral angles from trajectory and store them into a HDF5 file (start/stop/step are optionals)\nd = Dihedral(top_file, trj_file, selection=\'all\', dihedral_type=\'calpha\', start=0, stop=None, step=1).run()\nX = d.result\nsave_dataset(\'dihedral_angles.h5\', "dihedral_angles", X)\n\n# Fit X using Unrolr (pSPE + dihedral distance) and save the embedding into a csv file\nU = Unrolr(r_neighbor=0.27, n_iter=50000, verbose=1)\nU.fit(X)\nU.save(fname=\'embedding.csv\')\n\nprint(\'%4.2f %4.2f\' % (U.stress, U.correlation))\n```\n\n## Todo list\n- [ ] Compare SPE performance with UMAP\n- [x] Compatibility with python 3\n- [x] Compatibility with the latest version of MDAnalysis (==0.17)\n- [ ] Unit tests\n- [x] Accessible directly from pip\n- [ ] Improve OpenCL performance (global/local memory)\n\n## Citation\nEberhardt, J., Stote, R. H., & Dejaegere, A. (2018). Unrolr: Structural analysis of protein conformations using stochastic proximity embedding. Journal of Computational Chemistry, 39(30), 2551-2557. https://doi.org/10.1002/jcc.25599\n\n## License\nMIT\n',
    'author': 'jeeberhardt',
    'author_email': 'qksoneo@gmail.com',
    'url': 'https://github.com/jeeberhardt/unrolr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
