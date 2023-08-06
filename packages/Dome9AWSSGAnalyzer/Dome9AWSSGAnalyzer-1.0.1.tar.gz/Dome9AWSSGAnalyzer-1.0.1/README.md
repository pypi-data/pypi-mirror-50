Dome9-SG-LookUp
---------------

Dome9-SG-LookUp (SGAnalyzerApp) uses Dome9 APIs to get information
about the Security Groups present in the account.

Running the App
---------------

::

	from SGAnalyzerAppDir import app

    app.main()


Features
--------

- Get details of Security Group provided SG-ID.
- Get details of Security Group by SG-Name in JSON.
- Get details of Security Group rules in JSON provided SG-ID.

Usage
-----

- Step 1: Enter the api-details in the api-config file, apiURL will be there
  already, enter the apiSecret and apiKey.
- Step 2: You can add associated Dome9 "cloudAccountId" with your AWS account ID
  as <Dome9clo-udac-coun-tIDE-nterhereonly>=<AWSAcIDhere> as a map under
  [aws-dome9-map] in api-config.ini file.
- Step 3: If you wish to create this as a package, use pyinstaller to package it
  and use shutil to keep api-config.ini file at the bottom of spec file.
- First button - Details by SGID - provides information filled in the boxes
  automatically when user hit the button after providing SGID in the box.
  Feel free to copy or reset by then.
- Second button is to reset the results.
- Third Button - Rules By SGID - provides a JSON format inbound and outbound
  configuration downloaded at the same location.
- Fourth Button - SGs by Name - provides a JSON format file including all the
  Security Group configuration as provided by user in SGName field.
- Will be adding more functionality and a new look to this initiative in near
  future.

HowToRun
--------

- Please find below the console snapshot from PyCharm:

import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\nitin.sharma\\PycharmProjects\\Dome9-SG-LookUp', 'C:/Users/nitin.sharma/PycharmProjects/Dome9-SG-LookUp'])
PyDev console: starting.
Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)] on win32
>> from SGAnalyzerAppDir import app
>> app.main()

