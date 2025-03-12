from pynvml import (
    nvmlInit,
    nvmlDeviceGetName,
    nvmlDeviceGetHandleByIndex,
    NVMLError,
    nvmlShutdown,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetUtilizationRates,
)


nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)
utilization = nvmlDeviceGetUtilizationRates(handle).gpu
print(utilization)
