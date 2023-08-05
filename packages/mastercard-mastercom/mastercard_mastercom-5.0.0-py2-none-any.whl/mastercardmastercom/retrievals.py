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

class Retrievals(BaseObject):
    """
    
    """

    __config = {
        
        "7fb1a8d7-31b0-4eca-9044-d53bb99f1cb7" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/{request-id}/fulfillments", "create", [], []),
        
        "e863b4fb-965e-472e-92f8-2f80e8e33789" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests", "create", [], []),
        
        "c3943340-1b96-4e71-85bf-9a9a8232c955" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/loaddataforretrievalrequests", "query", [], []),
        
        "4540fba7-0663-4d50-8ad3-c6bd231353da" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/{request-id}/documents", "query", [], ["format"]),
        
        "ffa382f3-2de5-4e31-94c9-2d8bf0f4edcf" : OperationConfig("/mastercom/v5/claims/{claim-id}/retrievalrequests/{request-id}/fulfillments/response", "create", [], []),
        
        "473d43c4-3b90-44d8-a927-123ec04ba542" : OperationConfig("/mastercom/v5/retrievalrequests/imagestatus", "update", [], []),
        
        "5ca1090f-4822-460a-8674-18f5ed92aa2c" : OperationConfig("/mastercom/v5/retrievalrequests/status", "update", [], []),
        
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
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("7fb1a8d7-31b0-4eca-9044-d53bb99f1cb7", Retrievals(mapObj))






    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("e863b4fb-965e-472e-92f8-2f80e8e33789", Retrievals(mapObj))











    @classmethod
    def getPossibleValueListsForCreate(cls,criteria):
        """
        Query objects of type Retrievals by id and optional criteria
        @param type criteria
        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("c3943340-1b96-4e71-85bf-9a9a8232c955", Retrievals(criteria))






    @classmethod
    def getDocumentation(cls,criteria):
        """
        Query objects of type Retrievals by id and optional criteria
        @param type criteria
        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("4540fba7-0663-4d50-8ad3-c6bd231353da", Retrievals(criteria))

    @classmethod
    def issuerRespondToFulfillment(cls,mapObj):
        """
        Creates object of type Retrievals

        @param Dict mapObj, containing the required parameters to create a new object
        @return Retrievals of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("ffa382f3-2de5-4e31-94c9-2d8bf0f4edcf", Retrievals(mapObj))







    def retrievalFullfilmentImageStatus(self):
        """
        Updates an object of type Retrievals

        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("473d43c4-3b90-44d8-a927-123ec04ba542", self)






    def retrievalFullfilmentStatus(self):
        """
        Updates an object of type Retrievals

        @return Retrievals object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("5ca1090f-4822-460a-8674-18f5ed92aa2c", self)






