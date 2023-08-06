# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Definition for the generic Estimator classes.

Estimators are the building block for training.  An estimator encapsulates the training code and parameters,
the compute resources and runtime environment for a particular training scenario.

With Azure Machine Learning, you can easily submit your training script to various compute targets, using
:class:`azureml.core.runconfig.RunConfiguration` object and :class:`azureml.core.script_run_config.ScriptRunConfig`
object. That pattern gives you a lot of flexibility and maximum control.

To facilitate deep learning model training, the Azure Machine Learning Python SDK provides an alternative
higher-level abstraction, the estimator, which allows users to easily construct run configurations. You can create
and use a generic :class:`azureml.train.estimator.Estimator` to submit a training script using any learning framework
you choose. You can submit your run on any compute target, whether it's your local machine,
a single VM in Azure, or a GPU cluster in Azure. For PyTorch, TensorFlow, Chainer, and Scikit-learn tasks,
Azure Machine Learning also provides :class:`azureml.train.dnn.PyTorch`, :class:`azureml.train.dnn.TensorFlow`,
:class:`azureml.train.dnn.Chainer`, and :class:`azureml.train.sklearn.SKLearn` estimators respectively to simplify
using these frameworks.

For introduction to model training, please see
https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-train-ml-models

For information about docker containers used in Azure ML training, please see
https://github.com/Azure/AzureML-Containers

"""

import logging

from azureml.core._experiment_method import experiment_method
from azureml.train._estimator_helper import _estimator_submit_method, _init_run_config, \
    _is_notebook_run, _update_config_for_notebook_run
from ._mml_base_estimator import MMLBaseEstimator

module_logger = logging.getLogger(__name__)


class Estimator(MMLBaseEstimator):
    """A generic Estimator to train the data using any supplied framework.

    This class is designed for use with frameworks that do not have a framework specific estimator class.

    .. remarks::
            This simple estimator wraps run configuration information to help simplify the tasks of specifying
            how a script is executed. It supports single-node as well as multi-node execution. Execution of the
            estimator will result in a model being produced which should be placed in the
            ScriptParams.OUTPUT_PATH folder.

            An example of how to submit an experiment through Estimator:

            .. code-block:: python

                from azureml.train.estimator import Estimator

                # run an experiment from the train.py code in your current directory
                estimator = Estimator(source_directory='.',
                                      compute_target='local',
                                      entry_script='train.py',
                                      conda_packages=['scikit-learn'])

                # submit the experiment and then wait until complete
                run = experiment.submit(estimator)
                run.wait_for_completion()

            See https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-train-models-with-aml
            for an example of training a model using remote cluster through Estimator.

            For information about docker containers used in Azure ML training, please see
            https://github.com/Azure/AzureML-Containers

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target:  The ComputeTarget where training will happen. This can either be an object or the
        string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.

        Supported values: Any Azure VM size.

        The list of available VM sizes are listed here:
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.

        Supported values: 'dedicated' and 'lowpriority'.

        This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dictionary containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
         distributed job will be run. Only AmlCompute target is supported for distributed jobs.
    :type node_count: int
    :param process_count_per_node: Number of processes per node. If greater than 1, mpi
         distributed job will be run. Only AmlCompute target is supported for distributed jobs.
    :type process_count_per_node: int
    :param distributed_backend: Communication backend for distributed training.

        Supported values: 'mpi'.

            'mpi': MPI/Horovod

        This parameter is required when node_count, process_count_per_node and/or worker_count > 1.

        When node_count == 1 and process_count_per_node == 1, no backend will be used
        unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param distributed_training: Parameters for running a distributed training job. Please use this option
        instead of deprecated distributed_backend.

        For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
        object to specify process_count_per_node.
    :type distributed_training: azureml.core.runconfig.MpiConfiguration
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
    :param source_directory_data_store: The backing data store for the project share.
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
    """

    _SUPPORTED_BACKENDS = ["mpi"]

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
                 max_run_duration_seconds=None):
        """Initialize the estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target:  The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.

            Supported values: Any Azure VM size.

            The list of available VM sizes are listed here:
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.

            Supported values: 'dedicated' and 'lowpriority'.

            This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dictionary containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param distributed_backend: Communication backend for distributed training.

            Supported values: 'mpi'.

                'mpi': MPI/Horovod

            This parameter is required when node_count, process_count_per_node and/or worker_count > 1.

            When node_count == 1 and process_count_per_node == 1, no backend will be used
            unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param distributed_training: Parameters for running a distributed training job. Please use this option
            instead of deprecated distributed_backend.

            For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
            object to specify process_count_per_node.
        :type distributed_training: azureml.core.runconfig.MpiConfiguration
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
        :param source_directory_data_store: The backing data store for the project share.
        :type source_directory_data_store: Datastore
        :param shm_size: The size of the Docker container's shared memory block. Please refer to
            https://docs.docker.com/engine/reference/run/ for more information. If not set, default is
            azureml.core.environment._DEFAULT_SHM_SIZE.
        :type shm_size: str
        :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
            cancel the run, if it took longer than this value.
        :type max_run_duration_seconds: int
        """
        estimator_config = _init_run_config(
            estimator=self,
            source_directory=source_directory,
            compute_target=compute_target,
            vm_size=vm_size,
            vm_priority=vm_priority,
            entry_script=entry_script,
            script_params=script_params,
            node_count=node_count,
            process_count_per_node=process_count_per_node,
            distributed_backend=distributed_backend,
            distributed_training=distributed_training,
            use_gpu=use_gpu,
            use_docker=use_docker,
            custom_docker_image=custom_docker_image,
            image_registry_details=image_registry_details,
            user_managed=user_managed,
            conda_packages=conda_packages,
            pip_packages=pip_packages,
            conda_dependencies_file_path=conda_dependencies_file_path,
            pip_requirements_file_path=pip_requirements_file_path,
            conda_dependencies_file=conda_dependencies_file,
            pip_requirements_file=pip_requirements_file,
            environment_variables=environment_variables,
            environment_definition=environment_definition,
            inputs=inputs,
            source_directory_data_store=source_directory_data_store,
            shm_size=shm_size,
            resume_from=resume_from,
            max_run_duration_seconds=max_run_duration_seconds)

        self._manual_restart_used = (resume_from is not None)
        self._distributed_backend = distributed_backend
        if distributed_training:
            self._distributed_backend = distributed_training

        if _is_notebook_run(estimator_config.script):
            _update_config_for_notebook_run(estimator_config,
                                            use_gpu,
                                            custom_docker_image)

        super(self.__class__, self).__init__(source_directory, compute_target=compute_target,
                                             estimator_config=estimator_config)
