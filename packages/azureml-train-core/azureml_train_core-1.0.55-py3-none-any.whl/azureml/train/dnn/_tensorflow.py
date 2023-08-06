# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""The TensorFlow estimator class."""

import logging

from azureml.core._experiment_method import experiment_method
from azureml.core.runconfig import TensorflowConfiguration

from ..estimator._framework_base_estimator import _FrameworkBaseEstimator
from .._estimator_helper import _estimator_submit_method


class TensorFlow(_FrameworkBaseEstimator):
    """A TensorFlow Estimator is used to train a TensorFlow-based model.

    Supported versions: 1.10, 1.12, 1.13

    .. remarks::

            While submitting a training job, Azure ML runs your script in a conda environment within
            a Docker container. The TensorFlow containers have the following dependencies installed.

            | Dependencies | TensorFlow 1.10/1.12 | TensorFlow 1.13 |
            | ---------------------- | -------------------- | -------------------- |
            | Python                 | 3.6.2                | 3.6.2                |
            | CUDA  (GPU image only) | 9.0                  | 10.0                 |
            | cuDNN (GPU image only) | 7.4.2                | 7.5.0                |
            | NCCL  (GPU image only) | 2.4.2                | 2.4.2                |
            | azureml-defaults       | Latest               | Latest               |
            | IntelMpi               | 2018.3.222           | 2018.3.222           |
            | horovod                | 0.15.2               | 0.16.1               |
            | miniconda              | 4.5.11               | 4.5.11               |
            | tensorflow             | 1.10.0/1.12.0        | 1.13.1               |
            | git                    | 2.7.4                | 2.7.4                |

            The Docker images extend Ubuntu 16.04.

            If you need to install additional dependencies, you can either use pip_packages/conda_packages
            parameters or provide your pip requirements.txt/conda environment.yml file. Alternatively,
            you can build your own image, and pass the custom_docker_image parameter to the estimator
            constructor.

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
        string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.

        Supported values: Any Azure VM size.

        The list of available VM sizes are listed here:
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.

        Supported values:'dedicated' and 'lowpriority'.

        This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dict containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. Only AmlCompute compute target
        is supported for distributed training (node_count > 1).
    :type node_count: int
    :param process_count_per_node: When using MPI, number of processes per node.
    :type process_count_per_node: int
    :param worker_count: When using Parameter Server, the number of worker nodes.
    :type worker_count: int
    :param parameter_server_count: When using Parameter Server, the number of parameter server nodes.
    :type parameter_server_count: int
    :param distributed_backend: Communication backend for distributed training.

        Supported values: 'mpi' and 'ps'.

            'mpi': MPI/Horovod
            'ps': parameter server

        This parameter is required when any of node_count, process_count_per_node, worker_count, or
        parameter_server_count > 1.
        In case of 'ps', worker_count + parameter_server_count should be less than or equal to
        node_count * (number of CPUs or GPUs per node)

        When node_count == 1 and process_count_per_node == 1, no backend will be used
        unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param distributed_training: Parameters for running a distributed training job. Please use this option
        instead of deprecated distributed_backend.

        For running a distributed job with Parameter Server backend, use
        :class:`azureml.core.runconfig.TensorflowConfiguration` object to specify worker_count and
        parameter_server_count.
        worker_count + parameter_server_count should be less than or equal to
        node_count * (number of CPUs or GPUs per node)

        For running a distributed job with MPI backend, use
        :class:`azureml.core.runconfig.MpiConfiguration` object to specify process_count_per_node.
    :type distributed_training: azureml.core.runconfig.TensorflowConfiguration or
        azureml.core.runconfig.MpiConfiguration
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.container_registry.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param conda_dependencies_file_path: A string representing the relative path to the conda dependencies yaml file.
    :type conda_dependencies_file_path: str
    :param pip_requirements_file_path: A string representing the relative path to the pip requirements text file.
        This can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file_path: str
    :param conda_dependencies_file: A string representing the relative path to the conda dependencies yaml file.
    :type conda_dependencies_file: str
    :param pip_requirements_file: A string representing the relative path to the pip requirements text file.
        This can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file: str
    :param environment_variables: A dictionary of environment variables names and values.
        These environment variables are set on the process where user script is being executed.
    :type environment_variables: dict
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonSection and DockerSection and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: Backing datastore for project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the Docker container's shared memory block. Please refer to
        https://docs.docker.com/engine/reference/run/ for more information. If not set, default is
        azureml.core.environment._DEFAULT_SHM_SIZE.
    :type shm_size: str
    :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
    :type resume_from: azureml.data.datapath.DataPath
    :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
        cancel the run, if it took longer than this value.
    :type max_run_duration_seconds: int
    :param framework_version: Tensorflow version to be used for executing training code.
        TensorFlow.get_supported_versions() returns a list of the versions supported by the current SDK.
    :type framework_version: str
    """

    FRAMEWORK_NAME = "TensorFlow"
    DEFAULT_VERSION = '1.13'
    _SUPPORTED_BACKENDS = ["mpi", "ps"]

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 worker_count=1,
                 parameter_server_count=1,
                 distributed_backend=None,
                 distributed_training=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 conda_dependencies_file_path=None,
                 pip_requirements_file_path=None,
                 conda_dependencies_file=None,
                 pip_requirements_file=None,
                 environment_variables=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None,
                 resume_from=None,
                 max_run_duration_seconds=None,
                 framework_version=None,
                 _enable_optimized_mode=False):
        """Initialize a TensorFlow estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.

            Supported values: Any Azure VM size.

            The list of available VM sizes are listed here:
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.

            Supported values:'dedicated' and 'lowpriority'.

            This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dict containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. Only AmlCompute compute target
            is supported for distributed training (node_count > 1).
        :type node_count: int
        :param process_count_per_node: When using MPI, number of processes per node.
        :type process_count_per_node: int
        :param worker_count: When using Parameter Server, the number of worker nodes.
        :type worker_count: int
        :param parameter_server_count: When using Parameter Server, the number of parameter server nodes.
        :type parameter_server_count: int
        :param distributed_backend: Communication backend for distributed training.

            Supported values: 'mpi' and 'ps'.

                'mpi': MPI/Horovod
                'ps': parameter server

            This parameter is required when any of node_count, process_count_per_node, worker_count, or
            parameter_server_count > 1.
            In case of 'ps', worker_count + parameter_server_count should be less than or equal to
            node_count * (number of CPUs or GPUs per node)

            When node_count == 1 and process_count_per_node == 1, no backend will be used
            unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param distributed_training: Parameters for running a distributed training job. Please use this option
            instead of deprecated distributed_backend.

            For running a distributed job with Parameter Server backend, use
            :class:`azureml.core.runconfig.TensorflowConfiguration` object to
            specify worker_count and parameter_server_count.
            worker_count + parameter_server_count should be less than or equal to
            node_count * (number of CPUs or GPUs per node)

            For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
            object to specify process_count_per_node.
        :type distributed_training: azureml.core.runconfig.TensorflowConfiguration or
            azureml.core.runconfig.MpiConfiguration
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.container_registry.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param conda_dependencies_file_path: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file_path: str
        :param pip_requirements_file_path: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
        :param environment_variables: A dictionary of environment variables names and values.
            These environment variables are set on the process where user script is being executed.
        :param conda_dependencies_file: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file: str
        :param pip_requirements_file: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file: str
        :param environment_variables: A dictionary of environment variables names and values.
            These environment variables are set on the process where user script is being executed.
        :type environment_variables: dict
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonSection and DockerSection and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: Backing datastore for project share.
        :type source_directory_data_store: str
        :param shm_size: The size of the Docker container's shared memory block. Please refer to
            https://docs.docker.com/engine/reference/run/ for more information. If not set, default is
            azureml.core.environment._DEFAULT_SHM_SIZE.
        :type shm_size: str
        :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
            cancel the run, if it took longer than this value.
        :type max_run_duration_seconds: int
        :param framework_version: Tensorflow version to be used for executing training code.
            TensorFlow.get_supported_versions() returns a list of the versions supported by the current SDK.
        :type framework_version: str
        :param _enable_optimized_mode: Enable incremental environment build with pre-built framework images for faster
            environment preparation. A pre-built framework image is built on top of Azure ML default CPU/GPU base
            images with framework dependencies pre-installed.
        :type _enable_optimized_mode: bool
        """
        if worker_count != 1:
            logging.warning("'worker_count' parameter will be deprecated. Please use it as part of "
                            "'distributed_training' parameter.")

        if parameter_server_count != 1:
            logging.warning("'parameter_server_count' parameter will be deprecated. Please use it as part of "
                            "'distributed_training' parameter.")

        super().__init__(source_directory, compute_target=compute_target, vm_size=vm_size,
                         vm_priority=vm_priority, entry_script=entry_script,
                         script_params=script_params, node_count=node_count,
                         process_count_per_node=process_count_per_node,
                         distributed_backend=distributed_backend, distributed_training=distributed_training,
                         use_gpu=use_gpu, use_docker=use_docker, custom_docker_image=custom_docker_image,
                         image_registry_details=image_registry_details,
                         user_managed=user_managed, conda_packages=conda_packages,
                         pip_packages=pip_packages,
                         conda_dependencies_file_path=conda_dependencies_file_path,
                         pip_requirements_file_path=pip_requirements_file_path,
                         conda_dependencies_file=conda_dependencies_file,
                         pip_requirements_file=pip_requirements_file,
                         environment_variables=environment_variables,
                         environment_definition=environment_definition, inputs=inputs,
                         source_directory_data_store=source_directory_data_store,
                         shm_size=shm_size, resume_from=resume_from,
                         max_run_duration_seconds=max_run_duration_seconds,
                         framework_name=self.FRAMEWORK_NAME,
                         framework_version=framework_version,
                         _enable_optimized_mode=_enable_optimized_mode)

        if distributed_backend and distributed_backend.lower() == "ps":
            self._estimator_config.framework = "TensorFlow"
            self._estimator_config.communicator = "ParameterServer"
            self._estimator_config.tensorflow.worker_count = worker_count
            self._estimator_config.tensorflow.parameter_server_count = parameter_server_count

        if distributed_training and isinstance(distributed_training, TensorflowConfiguration):
            self._estimator_config.framework = "TensorFlow"
            self._estimator_config.communicator = "ParameterServer"
            self._estimator_config.tensorflow = distributed_training

    def _get_telemetry_values(self, func):
        telemetry_values = super()._get_telemetry_values(func)
        telemetry_values['numOfWorkers'] = self._estimator_config.tensorflow.worker_count
        telemetry_values['numOfPSNodes'] = self._estimator_config.tensorflow.parameter_server_count
        return telemetry_values
