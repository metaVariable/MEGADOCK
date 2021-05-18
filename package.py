# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Megadock(MakefilePackage):

    # Package Description
    """An ultra-high-performance protein-protein docking for heterogeneous supercomputers"""

    # Source information
    homepage = "https://github.com/akiyamalab/MEGADOCK"
    url      = "https://github.com/akiyamalab/MEGADOCK/archive/refs/tags/4.1.3.tar.gz"

    # Maintainers information (GitHub account)
    maintainers = ['akiyamalab']

    # Older versions
    version('4.1.3', sha256='9eaa31e22bff471cd158c4ce40ab89209108361a9fce970d681d99b40ddffe5f')
    version('4.1.2', sha256='b4f05a3da15d15f9392b03e0fefee74ff34cf39428c0188db9a46086d35773d7')
    version('4.1.1', sha256='1aa9bdbdb7ec80b86bd111c2b9d94aea47ad8eec8d964b51c3fe1f42e52b2e77')
    version('4.1.0', sha256='6cf5e6fdf4ebdf75e7407937c659ea5c65b72ed42cd3a8ca3fb521d65511e964')
    version('4.0.2', sha256='b2e1a888d6763f2e5377490a9a585122ebfe164375848bbe96c73ab7e182b827')

    # Variants
    variant('openmp', default=True, description='Build with OpenMP support (required)')
    variant('gpu', default=False, description='Build with NVIDIA GPU support')
    variant('mpi', default=False, description='Build with MPI support')

    # Dependent packages
    depends_on('fftw@3.3.8~mpi~openmp precision=float')

    # Makefile modifications
    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

        # switch GPU flag
        if '+gpu' in self.spec:
            makefile.filter('USE_GPU    := .*', 'USE_GPU := 1')
        else:
            makefile.filter('USE_GPU    := .*', 'USE_GPU := 0')

        # switch MPI flag
        if '+mpi' in self.spec:
            makefile.filter('USE_MPI    := .*', 'USE_MPI := 1')
        else:
            makefile.filter('USE_MPI    := .*', 'USE_MPI := 0')

        # switch OpenMP flag
        if '~openmp' in self.spec:
            makefile.filter('OMPFLAG  .* ?= .*', 'OMPFLAG := ')
        else:
            makefile.filter('OMPFLAG  .* ?= .*', 'OMPFLAG := ' + self.compiler.openmp_flag)


    # Install
    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        
        bin_name='megadock'

        if '+gpu' in self.spec:
            bin_name += "-gpu"
        if '+mpi' in self.spec:
            bin_name += "-dp"
        
        install(bin_name, prefix.bin)
        install('decoygen', prefix.bin)
        install('calcrg', prefix.bin)
