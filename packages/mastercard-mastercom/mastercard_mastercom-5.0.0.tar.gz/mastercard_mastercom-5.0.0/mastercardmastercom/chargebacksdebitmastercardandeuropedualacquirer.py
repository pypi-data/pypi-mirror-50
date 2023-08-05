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

class ChargebacksDebitMasterCardAndEuropeDualAcquirer(BaseObject):
    """
    
    """

    __config = {
        
        "4a82d1d4-1a9d-406f-9832-09e34d7731e2" : OperationConfig("/mastercom/v5/chargebacks/debitmc/acknowledge", "update", [], []),
        
        "57d0c195-a094-42f0-91eb-6bdd5e2ff172" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/debitmc", "create", [], []),
        
        "fd5c5158-f81a-496d-b11b-eaa1583d70cc" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/debitmc/{chargeback-id}/reversal", "create", [], []),
        
        "d6994c67-e3db-48fb-8476-cff5bd40d72c" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/debitmc/{chargeback-id}/documents", "query", [], ["format"]),
        
        "c95b8fe0-aeee-4e2a-853e-29ace6c984f6" : OperationConfig("/mastercom/v5/chargebacks/debitmc/imagestatus", "update", [], []),
        
        "f037308b-a3a2-423e-80b2-7f9b622f42ab" : OperationConfig("/mastercom/v5/chargebacks/debitmc/status", "update", [], []),
        
        "cde82e09-1511-429b-b1d2-16822ee33a8a" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/debitmc/{chargeback-id}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())



    def acknowledgeReceivedChargebacks(self):
        """
        Updates an object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("4a82d1d4-1a9d-406f-9832-09e34d7731e2", self)





    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @param Dict mapObj, containing the required parameters to create a new object
        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("57d0c195-a094-42f0-91eb-6bdd5e2ff172", ChargebacksDebitMasterCardAndEuropeDualAcquirer(mapObj))






    @classmethod
    def createReversal(cls,mapObj):
        """
        Creates object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @param Dict mapObj, containing the required parameters to create a new object
        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("fd5c5158-f81a-496d-b11b-eaa1583d70cc", ChargebacksDebitMasterCardAndEuropeDualAcquirer(mapObj))











    @classmethod
    def retrieveDocumentation(cls,criteria):
        """
        Query objects of type ChargebacksDebitMasterCardAndEuropeDualAcquirer by id and optional criteria
        @param type criteria
        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("d6994c67-e3db-48fb-8476-cff5bd40d72c", ChargebacksDebitMasterCardAndEuropeDualAcquirer(criteria))


    def chargebacksImageStatus(self):
        """
        Updates an object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("c95b8fe0-aeee-4e2a-853e-29ace6c984f6", self)






    def chargebacksStatus(self):
        """
        Updates an object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("f037308b-a3a2-423e-80b2-7f9b622f42ab", self)






    def update(self):
        """
        Updates an object of type ChargebacksDebitMasterCardAndEuropeDualAcquirer

        @return ChargebacksDebitMasterCardAndEuropeDualAcquirer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("cde82e09-1511-429b-b1d2-16822ee33a8a", self)






