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

class Chargebacks(BaseObject):
    """
    
    """

    __config = {
        
        "57b75c2b-eb8e-495c-88b0-8c9d0d33663e" : OperationConfig("/mastercom/v5/chargebacks/acknowledge", "update", [], []),
        
        "633b0ac1-b71c-430d-bc6c-1f33c460c840" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks", "create", [], []),
        
        "426c9ee9-e9a1-4286-9104-d033875eeea5" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/{chargeback-id}/reversal", "create", [], []),
        
        "f816ba10-37eb-4627-90c0-675f628126d3" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/{chargeback-id}/documents", "query", [], ["format"]),
        
        "350319f9-480e-467c-bae8-d7daca9a12fb" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/loaddataforchargebacks", "create", [], []),
        
        "d2f960a8-e382-4b72-ab56-76c6d275bdb5" : OperationConfig("/mastercom/v5/chargebacks/imagestatus", "update", [], []),
        
        "70af773a-fd5a-4173-a848-022ab39f088c" : OperationConfig("/mastercom/v5/chargebacks/status", "update", [], []),
        
        "aa1b6eaa-18d5-44c3-8480-0696e5cd3bc7" : OperationConfig("/mastercom/v5/claims/{claim-id}/chargebacks/{chargeback-id}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())



    def acknowledgeReceivedChargebacks(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("57b75c2b-eb8e-495c-88b0-8c9d0d33663e", self)





    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("633b0ac1-b71c-430d-bc6c-1f33c460c840", Chargebacks(mapObj))






    @classmethod
    def createReversal(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("426c9ee9-e9a1-4286-9104-d033875eeea5", Chargebacks(mapObj))











    @classmethod
    def retrieveDocumentation(cls,criteria):
        """
        Query objects of type Chargebacks by id and optional criteria
        @param type criteria
        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("f816ba10-37eb-4627-90c0-675f628126d3", Chargebacks(criteria))

    @classmethod
    def getPossibleValueListsForCreate(cls,mapObj):
        """
        Creates object of type Chargebacks

        @param Dict mapObj, containing the required parameters to create a new object
        @return Chargebacks of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("350319f9-480e-467c-bae8-d7daca9a12fb", Chargebacks(mapObj))







    def chargebacksImageStatus(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("d2f960a8-e382-4b72-ab56-76c6d275bdb5", self)






    def chargebacksStatus(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("70af773a-fd5a-4173-a848-022ab39f088c", self)






    def update(self):
        """
        Updates an object of type Chargebacks

        @return Chargebacks object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("aa1b6eaa-18d5-44c3-8480-0696e5cd3bc7", self)






