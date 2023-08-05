#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardmastercom import ResourceConfig

class RetrievalsDebitMasterCardAndEuropeDualAcquirer(BaseObject):
    """
    
    """

    __config = {
        
        "11991c96-2c83-4575-ac51-379590435e70" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/debitmc/{request-id}/fulfillments", "create", [], []),
        
        "014e90ec-3824-4f04-a6c8-0a215b17d6da" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/debitmc", "create", [], []),
        
        "d7b11d89-bbeb-4e6e-9b0f-92c0c3626f1d" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/debitmc/{request-id}/documents", "query", [], ["format"]),
        
        "a0c5284d-47d4-4be3-a356-142f91b5fb46" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/debitmc/{request-id}/fulfillments/response", "create", [], []),
        
        "22c33181-8d6a-4689-933e-a0e98e5d4a76" : OperationConfig("/mastercom/v5/retrievalrequests/debitmc/imagestatus", "update", [], []),
        
        "93572a3f-3530-4821-81ba-94985ac91693" : OperationConfig("/mastercom/v5/retrievalrequests/debitmc/status", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def acquirerFulfillARequest(cls,mapObj):
        """
        Creates object of type RetrievalsDebitMasterCardAndEuropeDualAcquirer

        @param Dict mapObj, containing the required parameters to create a new object
        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("11991c96-2c83-4575-ac51-379590435e70", RetrievalsDebitMasterCardAndEuropeDualAcquirer(mapObj))






    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type RetrievalsDebitMasterCardAndEuropeDualAcquirer

        @param Dict mapObj, containing the required parameters to create a new object
        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("014e90ec-3824-4f04-a6c8-0a215b17d6da", RetrievalsDebitMasterCardAndEuropeDualAcquirer(mapObj))











    @classmethod
    def getDocumentation(cls,criteria):
        """
        Query objects of type RetrievalsDebitMasterCardAndEuropeDualAcquirer by id and optional criteria
        @param type criteria
        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("d7b11d89-bbeb-4e6e-9b0f-92c0c3626f1d", RetrievalsDebitMasterCardAndEuropeDualAcquirer(criteria))

    @classmethod
    def issuerRespondToFulfillment(cls,mapObj):
        """
        Creates object of type RetrievalsDebitMasterCardAndEuropeDualAcquirer

        @param Dict mapObj, containing the required parameters to create a new object
        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("a0c5284d-47d4-4be3-a356-142f91b5fb46", RetrievalsDebitMasterCardAndEuropeDualAcquirer(mapObj))







    def retrievalFullfilmentImageStatus(self):
        """
        Updates an object of type RetrievalsDebitMasterCardAndEuropeDualAcquirer

        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("22c33181-8d6a-4689-933e-a0e98e5d4a76", self)






    def retrievalFullfilmentStatus(self):
        """
        Updates an object of type RetrievalsDebitMasterCardAndEuropeDualAcquirer

        @return RetrievalsDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("93572a3f-3530-4821-81ba-94985ac91693", self)






