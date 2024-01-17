
import os
import glob
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension

__version__ = "1.0.0"

module_name = "DifferentiablePointRender"
submodule_names = [
    "GaussianSplatting"
    # more submodules in the future
]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULAR_DIR = os.path.join(ROOT_DIR, module_name)

def search_sources(submodule):
    
    sources = glob.glob(os.path.join(f"{MODULAR_DIR}/{submodule}", "src/*.c"))
    sources += glob.glob(os.path.join(f"{MODULAR_DIR}/{submodule}", "src/*.cu")) 
    sources += glob.glob(os.path.join(f"{MODULAR_DIR}/{submodule}", "src/*.cpp"))

    return sources


def search_includes():
    return glob.glob(os.path.join(f"{MODULAR_DIR}", "*/include"))


def search_third_party():
    third_party_dir = os.path.join(ROOT_DIR, "third_party")
    
    third_parties = []
    if os.path.exists(third_party_dir):
        third_parties = [os.path.join(third_party_dir, d) 
            for d in os.listdir(third_party_dir)]

    return third_parties
    

def make_extensions():
    exts = [CUDAExtension(
            name=f"{module_name}.{submodule}._C",
            sources=search_sources(submodule),
            include_dirs=search_includes()+search_third_party(),
            extra_compile_args={'cxx': ['-g'], 'nvcc': ['-g']},
            #  extra_compile_args={"nvcc": ["-O3", "--use_fast_math"]}
        )
        for submodule in submodule_names
    ]
    
    return exts

setup(
    name="DifferentiablePointRender",
    version=__version__,
    description="Differentiable Point Render CUDA extension for Pointrix",
    url="https://github.com/NJU-3DV/DifferentiablePointRender",
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "jaxtyping"
    ],
    packages=[f"{module_name}"] + [f"{module_name}.{submodule}" for submodule in submodule_names],
    ext_modules=make_extensions(),
    cmdclass={"build_ext": BuildExtension}
)
