from ipykernel.kernelapp import IPKernelApp
from . import ScriptaxKernel

IPKernelApp.launch_instance(kernel_class=ScriptaxKernel)
