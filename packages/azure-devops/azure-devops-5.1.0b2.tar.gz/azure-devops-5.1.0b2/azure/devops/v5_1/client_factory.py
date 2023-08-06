# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# Generated file, DO NOT EDIT
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------------------------


class ClientFactoryV5_1(object):
    """ClientFactoryV5_1.
    A factory class to get the 5.1 preview clients.
    """

    def __init__(self, connection):
        self._connection = connection

    def get_feature_availability_client(self):
        """get_feature_availability_client.
        Gets the 5.1 version of the FeatureAvailabilityClient
        :rtype: :class:`<FeatureAvailabilityClient> <azure.devops.v5_1.feature_availability.feature_availability_client.FeatureAvailabilityClient>`
        """
        return self._connection.get_client('azure.devops.v5_1.feature_availability.feature_availability_client.FeatureAvailabilityClient')

    def get_location_client(self):
        """get_location_client.
        Gets the 5.1 version of the LocationClient
        :rtype: :class:`<LocationClient> <azure.devops.v5_1.location.location_client.LocationClient>`
        """
        return self._connection.get_client('azure.devops.v5_1.location.location_client.LocationClient')

    def get_operations_client(self):
        """get_operations_client.
        Gets the 5.1 version of the OperationsClient
        :rtype: :class:`<OperationsClient> <azure.devops.v5_1.operations.operations_client.OperationsClient>`
        """
        return self._connection.get_client('azure.devops.v5_1.operations.operations_client.OperationsClient')

    def get_security_client(self):
        """get_security_client.
        Gets the 5.1 version of the SecurityClient
        :rtype: :class:`<SecurityClient> <azure.devops.v5_1.security.security_client.SecurityClient>`
        """
        return self._connection.get_client('azure.devops.v5_1.security.security_client.SecurityClient')

