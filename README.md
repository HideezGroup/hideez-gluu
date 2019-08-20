# hideez-gluu
Hideez custom interception authentication script for Gluu Server

### Prerequisites ###

* Gluu Server must be set up and available
* Hideez Server must be set up and available
* Hideez Key and Hideez Client for Windows must be set up on the user's workstation
* An account of the Hideez user must be in place (see Hideez documentation)
* Hideez interception script - hideez.py
* Hideez UI components - login.xhtml, otplogin.xhtml
* Hideez Java SDK - hideez.jar
* Hideez messages - oxauth.properties
* Unirest Java library (http://kong.github.io/unirest-java/) and appropriate runtime libraries. This integration was tested with unirest-java-1.4.9.jar and dependencies:
	* commons-logging-1.2.jar
	* httpasyncclient-4.0.2.jar
	* httpclient-4.3.6.jar
	* httpcore-4.4.4.jar
	* httpcore-nio-4.3.2.jar
	* httpmime-4.3.6.jar
	* json-20140107.jar
	* jstl-1.2.jar

### Integration ###

Actual procedure on how to integrate Hideez AuthN solution and Gluu Server is based on custom authentication interception scripts. The appropriate tutorial is available here - https://gluu.org/docs/ce/authn-guide/customauthn/. During integration Hideez script will be enabled. The script uses Hideez SDK (hideez.jar) to call Hideez authentication.

### Download and copy Hideez components and dependencies ###

Go to the Hideez account on github.com to the hideez-gluu project (https://github.com/HideezGroup/hideez-gluu). Download Hideez components and copy them to the appropriate places on Gluu server

* login.xhtml, otplogin.xhtml copy to ${gluu_chroot}/opt/gluu/jetty/oxauth/custom/pages/auth/hideez/
* hideez.jar copy to ${gluu_chroot}/opt/gluu/jetty/oxauth/custom/libs/
* oxauth.properties copy to ${gluu_chroot}/opt/gluu/jetty/oxauth/custom/i18n/
* hideez.py copy to ${gluu_chroot}/

Download unirest.jar and deps, copy them to ${gluu_chroot}/opt/gluu/jetty/oxauth/custom/libs/

Restart oxauth service under chroot by running "service oxauth restart"

### Enable custom script ###

* Log into the Gluu admin dashboard -> Manage Custom Scripts -> Click "Add Custom Script Configuration" button;
* Add the custom Hideez interception script and select the "Enabled" option;
* Add the hideez:url custom parameter with actual URL to Hideez Server Authentication endpoint (e.g. https://hideez.server.com/authn/) and save the custom script configuration;
* Navigate in the Gluu Server UI to Manage Authentication -> Default Authentication Method and select hideez as the Default acr, then click update
