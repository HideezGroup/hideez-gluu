# Copyright (c) 2019, Hideez & Gluu
# Author: Jacob Revyakin (yr@hideez.com) & Yuriy Movchan (Gluu)

from org.xdi.service.cdi.util import CdiUtil
from org.xdi.oxauth.security import Identity
from org.xdi.model.custom.script.type.auth import PersonAuthenticationType
from org.xdi.oxauth.service import UserService, AuthenticationService, SessionIdService
from org.xdi.util import StringHelper
from org.xdi.oxauth.util import ServerUtil
from java.util import Arrays
from com.hideez.idphes1 import HESAuthenticator

import java

class PersonAuthentication(PersonAuthenticationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Basic. Initialization"

        self.hideez_count_login_steps = 1

        if not configurationAttributes.containsKey("hideez:url"):
            print "Hideez AuthN. Initialization. Property hideez:url is mandatory"
            return False

        self.hideezUrl = configurationAttributes.get("hideez:url").getValue2()

        print "Basic. Initialized successfully"
        return True

    def destroy(self, configurationAttributes):
        print "Basic. Destroy "
        print "Basic. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def isValidAuthenticationMethod(self, usageType, configurationAttributes):
        return True

    def getAlternativeAuthenticationMethod(self, usageType, configurationAttributes):
        return None

    def authenticate(self, configurationAttributes, requestParameters, step):
        authenticationService = CdiUtil.bean(AuthenticationService)
        identity = CdiUtil.bean(Identity)
        logged_in = False

        if (step == 1):
            print "Basic. Authenticate for step 1"

            credentials = identity.getCredentials()
            user_name = credentials.getUsername()
            user_password = credentials.getPassword()

            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password)):
                try:
                    authNr = HESAuthenticator(self.hideezUrl)
                    hUser = authNr.authN(user_name, user_password)
                    print "Hideez user: Email %s, Name %s, Surname %s" % (hUser.email, hUser.firstName, hUser.lastName)
                    authenticationService.authenticate(user_name)
                    self.hideez_count_login_steps = 1
                    logged_in = True
                except HESAuthenticator.NeedOTPException, ex:
                    identity.setWorkingParameter("hideez_user_name", user_name)
                    identity.setWorkingParameter("hideez_user_password", user_password)
                    self.hideez_count_login_steps = 2
                    logged_in = True
#                except (HESAuthenticator.UserNotFoundException, HESAuthenticator.InvalidCredentialsException, HESAuthenticator.UserIsLockedout), ex:
#                    logged_in = False
#                    print ex.class.name + ex.message
                except Exception, ex:
                    logged_in = False
                    print ex.class.name + ex.message

        else:
            print "OTP. Authenticate for step 2"

            session_id = CdiUtil.bean(SessionIdService).getSessionIdFromCookie()
            if StringHelper.isEmpty(session_id):
                print "OTP. Validate session id. Failed to determine session_id"
                return False

            otpCode = ServerUtil.getFirstValue(requestParameters, "loginForm:otpCode")
            if StringHelper.isEmpty(otpCode):
                print "OTP. Process OTP authentication. otpCode is empty"
                #facesMessages.add(FacesMessage.SEVERITY_ERROR, "Failed to authenticate. OTP code is empty")
		return False

            user_name = identity.getWorkingParameter("hideez_user_name")
            user_password = identity.getWorkingParameter("hideez_user_password")

            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password) and StringHelper.isNotEmptyString(otpCode)):
                try:
                    authNr = HESAuthenticator(self.hideezUrl)
                    hUser = authNr.authN(user_name, user_password, otpCode)
                    print "Hideez user: Email %s, Name %s, Surname %s" % (hUser.email, hUser.firstName, hUser.lastName)
                    authenticationService.authenticate(user_name)
                    logged_in = True
#                except (HESAuthenticator.UserNotFoundException, HESAuthenticator.InvalidCredentialsException, HESAuthenticator.UserIsLockedout, HESAuthenticator.NeedOTPException), ex:
#                    logged_in = False
#                    print ex.class.name + ex.message
                except Exception, ex:
                    logged_in = False
                    print ex.class.name + ex.message

        if (not logged_in):
            return False
        else:
            return True

    def prepareForStep(self, configurationAttributes, requestParameters, step):
        return True

    def getExtraParametersForStep(self, configurationAttributes, step):
        if (step == 2):
            return Arrays.asList("hideez_user_name", "hideez_user_password")
        return None

    def getCountAuthenticationSteps(self, configurationAttributes):
        return self.hideez_count_login_steps

    def getPageForStep(self, configurationAttributes, step):
        if (step == 2):
            return "/auth/hideez/otplogin.xhtml"
        return "/auth/hideez/login.xhtml"

    def logout(self, configurationAttributes, requestParameters):
        return True
