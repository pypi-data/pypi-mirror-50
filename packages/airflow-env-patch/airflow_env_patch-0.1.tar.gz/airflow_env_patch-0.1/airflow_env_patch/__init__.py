#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: mithril
# Created Date: 2019-08-14 13:45:51
# Last Modified: 2019-08-14 14:16:04


def patched_build_spark_submit_command(self, application):
    """
    Construct the spark-submit command to execute.
    :param application: command to append to the spark-submit command
    :type application: str
    :return: full command to be executed
    """
    self.log.info('Monkey Patched!')

    connection_cmd = self._get_spark_binary_path()

    # The url ot the spark master
    connection_cmd += ["--master", self._connection['master']]

    if self._conf:
        for key in self._conf:
            connection_cmd += ["--conf", "{}={}".format(key, str(self._conf[key]))]
    if self._env_vars and (self._is_kubernetes or self._is_yarn):
        if self._is_yarn:
            tmpl = "spark.yarn.appMasterEnv.{}={}"
        else:
            tmpl = "spark.kubernetes.driverEnv.{}={}"

        self.log.info('set appMasterEnv and executorEnv')
        for key in self._env_vars:
            connection_cmd += [
                "--conf",
                tmpl.format(key, str(self._env_vars[key]))]
            connection_cmd += [
                "--conf",
                "spark.executorEnv.{}={}".format(key, str(self._env_vars[key]))]

        self.log.info('set Popen env')
        self._env = self._env_vars  # Do it on Popen of the process
    if self._is_kubernetes:
        connection_cmd += ["--conf", "spark.kubernetes.namespace={}".format(
            self._connection['namespace'])]
    if self._files:
        connection_cmd += ["--files", self._files]
    if self._py_files:
        connection_cmd += ["--py-files", self._py_files]
    if self._archives:
        connection_cmd += ["--archives", self._archives]
    if self._driver_class_path:
        connection_cmd += ["--driver-class-path", self._driver_class_path]
    if self._jars:
        connection_cmd += ["--jars", self._jars]
    if self._packages:
        connection_cmd += ["--packages", self._packages]
    if self._exclude_packages:
        connection_cmd += ["--exclude-packages", self._exclude_packages]
    if self._repositories:
        connection_cmd += ["--repositories", self._repositories]
    if self._num_executors:
        connection_cmd += ["--num-executors", str(self._num_executors)]
    if self._total_executor_cores:
        connection_cmd += ["--total-executor-cores", str(self._total_executor_cores)]
    if self._executor_cores:
        connection_cmd += ["--executor-cores", str(self._executor_cores)]
    if self._executor_memory:
        connection_cmd += ["--executor-memory", self._executor_memory]
    if self._driver_memory:
        connection_cmd += ["--driver-memory", self._driver_memory]
    if self._keytab:
        connection_cmd += ["--keytab", self._keytab]
    if self._principal:
        connection_cmd += ["--principal", self._principal]
    if self._name:
        connection_cmd += ["--name", self._name]
    if self._java_class:
        connection_cmd += ["--class", self._java_class]
    if self._verbose:
        connection_cmd += ["--verbose"]
    if self._connection['queue']:
        connection_cmd += ["--queue", self._connection['queue']]
    if self._connection['deploy_mode']:
        connection_cmd += ["--deploy-mode", self._connection['deploy_mode']]

    # The actual script to execute
    connection_cmd += [application]

    # Append any application arguments
    if self._application_args:
        connection_cmd += self._application_args

    self.log.info("Spark-Submit cmd: %s", connection_cmd)

    return connection_cmd


import airflow.contrib.hooks.spark_submit_hook
airflow.contrib.hooks.spark_submit_hook.SparkSubmitHook._build_spark_submit_command = patched_build_spark_submit_command