# EdgeST SDK

EdgeST SDK is an IoT edge computing abstraction library for Linux gateways. It relies on cloud platforms' edge SDKs to enable local execution of functions on a Linux gateway and synchronization to the cloud.

More specifically, it enables the creation of “virtual” devices on the gateway that map to non-IP connected devices (e.g. via Bluetooth Low Energy technology), and the corresponding "shadow" devices on the cloud. Local computation can be performed directly on the gateway with the same logic written for the cloud even when Internet connection is lost, and shadow devices will be synchronized to virtual devices as soon as Internet connection becomes available.

Currently [Amazon AWS Greengrass](https://aws.amazon.com/it/greengrass/) edge computing service is supported, while other cloud engines will be added in the future.


## Documentation
Documentation can be found [here](https://stmicroelectronics.github.io/EdgeSTSDK_Python/index.html).


## Compatibility
This version of the SDK is compatible with [Python](https://www.python.org/) 2.7 and runs on a Linux system.

