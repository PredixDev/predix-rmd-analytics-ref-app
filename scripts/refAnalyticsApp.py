import sys, shutil
import traceback
import time
import subprocess
import os

statementStatus  = subprocess.call('git submodule update --init --remote predix-scripts ', shell=True)
pwd=os.getcwd()
sys.path.insert(0, pwd)
print(sys.path)
sys.path.insert(0, pwd+'/predix-scripts/python')
print(sys.path)
from predix import *

#####################################################################################################
############################### main methods ###############################
#####################################################################################################

def deployAnalyticReferenceAppDelete(config):
	try:
		if ( config.deleteAppsAndServices == "y" ):
			print("****************** Installing deployAnalyticReferenceAppDelete ******************")
			config.current='deployAnalyticReferenceAppDelete'
			# Deleting existing Applications and Services
			deleteExistingApplication(config.fdhAppName)
			#deleteExistingApplication(config.rabbitMQConsumerAppName)
			deleteExistingApplication(config.rmdAnalyticsAppName)
			deleteExistingApplication(config.rmdOrchestrationClientAppName)

			deleteExistingService(config.rmdRabbitMQ)
			deleteExistingService(config.predixAnalyticsCatalog)
			deleteExistingService(config.predixAnalyticsRuntime)

			config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			time.sleep(10)  # Delay
			deployAnalyticReferenceAppDelete(config)
		else :
			raise

def buildPredixSDKs(config):
	try:
		print("****************** Running buildPredixSDKs ******************")
		config.current='buildPredixSDKs'
		print("Fast install = " + config.fastinstall)

		if config.pullsubmodules == 'y':
			print("CurrentDir " + os.getcwd())
			statementStatus  = subprocess.call('git submodule update --init --remote predix-sdks', shell=True)
			print("CurrentDir " + os.getcwd())
			print("ChangeDir = " + config.predixSDKs)
			os.chdir(config.predixSDKs)
			try :
				updateGitModules(config)
				checkoutSubmodules()
			finally:
				restoreGitModules(config)
			print("ChangeDir = ..")
			os.chdir("..")
			print("Build using maven setting : "+config.mvnsettings +" Maven Repo : "+config.mavenRepo)
		if config.fastinstall != 'y' :
			print("Compiling code...")
			if config.mavenRepo != "":
				os.removedirs(config.mavenRepo)
				#statementStatus  = subprocess.call("rm -rf "+config.mavenRepo, shell=True)
				if config.mvnsettings == "":
					os.chdir(config.predixSDKs)
					statementStatus  = subprocess.call("mvn clean package -Dmaven.repo.local="+config.mavenRepo, shell=True)
					os.chdir("..")
				else:
					os.chdir(config.predixSDKs)
					statementStatus  = subprocess.call("mvn clean package -s "+config.mvnsettings+" -Dmaven.repo.local="+config.mavenRepo, shell=True)
					os.chdir("..")
			else:
				print("mvnSettings=" + config.mvnsettings)
				if config.mvnsettings == "":
					os.chdir(config.predixSDKs)
					statementStatus  = subprocess.call("mvn clean package", shell=True)
					os.chdir("..")
				else:
					os.chdir(config.predixSDKs)
					statementStatus  = subprocess.call("mvn clean package -s "+ config.mvnsettings, shell=True)
					os.chdir("..")
			if statementStatus != 0:
				print("Maven build failed.")
				sys.exit(1);
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			buildPredixSDKs(config)
		else :
			raise

def buildReferenceApp(config):
	try:
		print("****************** Running buildAnalyticReferenceApp ******************")
		config.current='buildReferenceApp'
		print("Fast install = " + config.fastinstall)
		if config.pullsubmodules == 'y':
			checkoutSubmodules()
			print("Build using maven setting : "+config.mvnsettings +" Maven Repo : "+config.mavenRepo)
		if config.fastinstall != 'y' :
			print("Compiling code...")
			if config.mavenRepo != "":
				os.removedirs(config.mavenRepo)
				#statementStatus  = subprocess.call("rm -rf "+config.mavenRepo, shell=True)
				if config.mvnsettings == "":
					statementStatus  = subprocess.call("mvn clean package -Dmaven.repo.local="+config.mavenRepo, shell=True)
				else:
					statementStatus  = subprocess.call("mvn clean package -s "+config.mvnsettings+" -Dmaven.repo.local="+config.mavenRepo, shell=True)
			else:
				 #statementStatus  = subprocess.call("rm -rf ~/.m2/repository/com/ge/predix/", shell=True)
				if config.mvnsettings == "":
					statementStatus  = subprocess.call("mvn clean package", shell=True)
				else:
					statementStatus  = subprocess.call("mvn clean package -s "+config.mvnsettings, shell=True)
			if statementStatus != 0:
				print("Maven build failed.")
				sys.exit(1);
		config.retryCount=0
	except:
		print(traceback.print_exc())

		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			buildReferenceApp(config)
		else :
			raise

def deployAndBindUAAToPredixBoot(config):
	try:
		os.chdir(config.predixbootRepoName)
		cfPush(config.predixbootAppName, 'cf push '+config.predixbootAppName+' -f ' + 'manifest.yml')
		statementStatus  = subprocess.call("cf bs "+config.predixbootAppName +" " + config.rmdUaaName , shell=True)
		if statementStatus == 1 :
				sys.exit("Error binding a uaa service instance to boot ")
	finally:
		os.chdir("..")

def deployAnalyticReferenceAppSetUAA(config):
	try :
		print("****************** Running deployAnalyticReferenceAppSetUAA ******************")
		config.current='deployAnalyticReferenceAppSetUAA'
		# these two are modified by some other functions.
		getAuthorities(config)
		#createPredixUAASecurityService(config)

		#Bind to Predix Boot
		#deployAndBindUAAToPredixBoot(config)
		getPredixUAAConfigfromVcaps(config)

		#Create Client Id and Users
		#createClientIdAndAddUser(config)
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppSetUAA(config)
		else :
			raise

def deployAnalyticReferenceAppSetACS(config):
	try :
		print("****************** Running deployAnalyticReferenceAppSetACS ******************")
		config.current='deployAnalyticReferenceAppSetACS'
		# acs integration
		getPredixUAAConfigfromVcaps(config)
		#createBindPredixACSService(config,config.rmdAcsName)
		getPredixACSConfigfromVcaps(config)

		print("****************** ACS configured As ******************")
		print ("\n ACS_URI = " + config.ACS_URI + "\n "+config.acsPredixZoneHeaderName+"= " +config.acsPredixZoneHeaderValue)
		print (" ACS zone "+config.acsOauthScope)
		print("****************** ***************** ******************")

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppSetACS(config)
		else :
			raise

def updateClientAuthoritiesAssetAndTimeseries(config):
	getClientAuthoritiesforAssetAndTimeSeriesService(config)

def deployAnalyticReferenceAppCreateAnalyticsInstance(config):
	try:
		print("****************** Running deployAnalyticReferenceAppCreateAnalyticsInstance ******************")
		config.current='deployAnalyticReferenceAppCreateAnalyticsInstance'

		# create a Asset Service
		print("****************** Predix Asset Timeseries are already created as part of REF APP INSTALLATION ******************")
		#createAsssetInstance(config,config.rmdPredixAssetName,config.predixAssetService)

		# create a Timeseries
		#createTimeSeriesInstance(config,config.rmdPredixTimeseriesName,config.predixTimeSeriesService)

		createAnalyticsCatalogInstance(config,config.rmdAnalyticsAppName,config.predixAnalyticsCatalog)

		createAnalyticsRuntimeInstance(config,config.rmdOrchestrationClientAppName,config.predixAnalyticsRuntime)

		#bindService(config.predixbootAppName,config.rmdPredixAssetName)
		#bindService(config.predixbootAppName,config.rmdPredixTimeseriesName)
		bindService(config.predixbootAppName,config.rmdAnalyticsAppName)
		bindService(config.predixbootAppName,config.rmdOrchestrationClientAppName)

		getVcapJsonForPredixBoot(config)
		getAssetURLandZone(config)
		getTimeseriesURLandZone(config)
		#getAnalyticsCatalogURLandZone(config)
		getAnalyticsRuntimeURLandZone(config)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppCreateAnalyticsInstance(config)
		else :
			raise

def deployAnalyticReferenceAppAddAuthorities(config):
	try:
		print("****************** Running deployAnalyticReferenceAppAddAuthorities ******************")
		config.current='deployAnalyticReferenceAppAddAuthorities'
		getPredixUAAConfigfromVcaps(config)
		getAuthorities(config)
		updateClientAuthoritiesACS(config)
		updateClientAuthoritiesAssetAndTimeseries(config)
		updateClientIdAuthorities(config)

		updateUserACS(config)
		updateUAAUserGroups(config, config.timeSeriesQueryScopes+","+config.timeSeriesInjestScopes+","+config.assetScopes+","+config.acsOauthScope)

		# setting up ACS policy and Subject
		createRefAppACSPolicyAndSubject(config, config.acsPredixZoneHeaderValue)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppAddAuthorities(config)
		else :
			raise

def getDataseedUrl(config):
	if not hasattr(config,'DATA_SEED_URL') :
		cfTarget= subprocess.check_output(["cf", "app",config.dataSeedAppName])
		print (cfTarget)
		config.DATA_SEED_URL="https://"+cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('dataSeedAppName URL '+config.DATA_SEED_URL)

def getFDHUrl(config):
	if not hasattr(config,'FDH_URL') :
		cfTarget= subprocess.check_output(["cf", "app",config.fdhAppName])
		print ("FDH app details")
		print (cfTarget)
		config.FDH_URL=cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('fdhAppName URL '+config.FDH_URL)

def getAnalyticsUrl(config):
		cfTarget= subprocess.check_output(["cf", "app",config.rmdAnalyticsAppName])
		print (cfTarget)
		config.RMD_ANALYTICS_URL="https://"+cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('RMD Analytics URL '+config.RMD_ANALYTICS_URL)


def getRabbitMQConsumerUrl(config):
	if not hasattr(config,'RABBITMQ_CONSUMER_URL') :
		cfTarget= subprocess.check_output(["cf", "app",config.rabbitMQConsumerAppName])
		print (cfTarget)
		config.RABBITMQ_CONSUMER_URL="https://"+cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('RabbitMQ URL= '+config.RABBITMQ_CONSUMER_URL)

def getWebsocketAppInfo(config):
	if not hasattr(config,'WEB_SOCKET_SERVER_HOST') :
		print("****************** Running getWebsocketAppInfo ******************")
		cfTarget= subprocess.check_output(["cf", "app",config.websocketAppName])
		print (cfTarget)
		config.WEB_SOCKET_SERVER_HOST=cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('WS ingestion URL '+config.WEB_SOCKET_SERVER_HOST)
		config.LIVE_DATA_WS_URL="wss://"+config.WEB_SOCKET_SERVER_HOST
		print ('LIVE_DATA_WS_URL '+config.LIVE_DATA_WS_URL)

def deployAnalyticReferenceAppCreateFDH(config):
	try:
		print("****************** Running deployAnalyticReferenceAppCreateFDH******************")
		config.current='deployAnalyticReferenceAppCreateFDH'
		getPredixUAAConfigfromVcaps(config)
		print("Current Directory ="+os.getcwd())
		getWebsocketAppInfo(config)
		fdhRepoName = "fdh-router-service/data-exchange"
		configureManifest(config, fdhRepoName)
		pushProject(config, config.fdhAppName, 'cf push '+config.fdhAppName+' -f '+fdhRepoName+'/manifest.yml',fdhRepoName, checkIfExists="false")
		print("Current Directory ="+os.getcwd())

		getFDHUrl(config)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			time.sleep(10)  # Delay
			deployAnalyticReferenceAppCreateFDH(config)
		else :
			raise


def deployAnalyticReferenceAppCreateRMDAnalytics(config):
	try:
		print("****************** Running deployAnalyticReferenceAppCreateRMDAnalytics******************")
		print("Current Directory ="+os.getcwd())
		config.current='deployAnalyticReferenceAppCreateRMDAnalytics'
		getPredixUAAConfigfromVcaps(config)
		print("Current Directory ="+os.getcwd())
		rmdAnalyticsRepoName = "rmd-analytics/ref-app-analytic-cf"
		getFDHUrl(config)
		getAnalyticsRuntimeURLandZone(config)
		configureManifest(config, rmdAnalyticsRepoName)
		pushProject(config, config.rmdAnalyticsAppName, 'cf push '+config.rmdAnalyticsAppName+' -f '+rmdAnalyticsRepoName+'/manifest.yml',rmdAnalyticsRepoName, checkIfExists="false")

		getAnalyticsUrl(config)

		print("Current Directory ="+os.getcwd())
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppCreateRMDAnalytics(config)
		else :
			raise

def deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate(config):
	try:
		config.current='deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate'

		getPredixUAAConfigfromVcaps(config)
		rabbitMQConsumerRepoName = "rabbitmq-consumer-template"
		configureManifest(config, rabbitMQConsumerRepoName)
		pushProject(config, config.rabbitMQConsumerAppName, 'cf push '+config.rabbitMQConsumerAppName+' -f '+rabbitMQConsumerRepoName+'/manifest.yml',rabbitMQConsumerRepoName, checkIfExists="false")

		getRabbitMQConsumerUrl(config)
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate(config)
		else :
			raise


def deployAnalyticReferenceAppCreateRMDOrchestrationClient(config):
	try:
		print("****************** Running deployAnalyticReferenceAppCreateRMDOrchestrationClient******************")
		print("*********Create RabbitMQ service********************")
		createRabbitMQInstance(config)

		print("Current Directory ="+os.getcwd())
		config.current='deployAnalyticReferenceAppCreateRMDOrchestrationClient'
		getPredixUAAConfigfromVcaps(config)
		print("Current Directory ="+os.getcwd())
		rmdOrchClientRepoName = "rmd-orchestration/fieldchangedevent-consumer"

		getAnalyticsRuntimeURLandZone(config)
		getAnalyticsUrl(config)
		configureManifest(config, rmdOrchClientRepoName)

		pushProject(config, config.rmdOrchestrationClientAppName, 'cf push '+config.rmdOrchestrationClientAppName+' -f '+rmdOrchClientRepoName+'/manifest.yml',rmdOrchClientRepoName, checkIfExists="false")

		print("Current Directory ="+os.getcwd())
		getOrchClientUrl(config)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppCreateRMDOrchestrationClient(config)
		else :
			raise

def getOrchClientUrl(config):
	cfTarget= subprocess.check_output(["cf", "app",config.rmdOrchestrationClientAppName])
	print (cfTarget)
	config.RMD_ORCH_URL="https://"+cfTarget.decode('utf8').split('urls:')[1].strip().split('last uploaded:')[0].strip()
	#print ('RMD Orch  URL '+config.RMD_ORCH_URL)
	config.fieldChangedEvent_MainQueue = getValueFromManifest("rmd-orchestration/fieldchangedevent-consumer", "fieldChangedEvent_MainQueue")

def configureManifest(config, manifestLocation):
	print("Current dir="+os.getcwd())
	# create a backup
	if os.path.isfile(manifestLocation + "/manifest.yml"):
		shutil.copy(manifestLocation+"/manifest.yml", manifestLocation+"/manifest.yml.bak")
	# copy template as manifest
	shutil.copy(manifestLocation+"/manifest.yml.template", manifestLocation+"/manifest.yml")
	s = open(manifestLocation+"/manifest.yml").read()
	s = s.replace('name: {your-name}', 'name: ' + config.instanceName)
	s = s.replace('{assetService}', config.rmdPredixAssetName)
	s = s.replace('{uaaService}', config.rmdUaaName)
	s = s.replace('{acsService}', config.rmdAcsName)
	s = s.replace('{oauthRestHost}', config.UAA_URI.replace('https://',''))
	s = s.replace('{clientId}', config.rmdAppClientId)
	s = s.replace('{username}', config.rmdUser1)
	s = s.replace('{password}', config.rmdUser1Pass)
	s = s.replace('{secret}', config.rmdAppSecret)
	s = s.replace('{rabbitMQService}', config.rmdRabbitMQ)
	if config.environment == 'FREE' :
		s = s.replace('1GB', '384MB')
	if hasattr(config,'RMD_ANALYTICS_URL') :
		s = s.replace('{rmdAnalyticsURI}', config.RMD_ANALYTICS_URL)
	if hasattr(config,'ACS_URI') :
		s = s.replace('{acsURI}', config.ACS_URI)
	s = s.replace('{timeSeriesService}', config.rmdPredixTimeseriesName)
	if hasattr(config,'ANALYTICRUNTIME_URI') :
		s = s.replace('{analyticsRuntimeService}', config.ANALYTICRUNTIME_URI)
	if hasattr(config,'ANALYTICRUNTIME_ZONE') :
		s = s.replace('{analyticsRuntimeZone}', config.ANALYTICRUNTIME_ZONE)
	if hasattr(config,'CATALOG_URI') :
		s = s.replace('{analyticsCatalogService}', config.CATALOG_URI)
	s = s.replace('{acssubdomain}', 'rmdsubdomain')
	if hasattr(config,'DATA_INGESTION_URL') :
		s = s.replace('{dataIngestionUrl}', config.DATA_INGESTION_URL)
	s = s.replace('{UAA_SERVER_URL}', config.UAA_URI)
	if hasattr(config,'ASSET_URI') :
		s = s.replace('{ASSET_URL}', config.ASSET_URI)
		s = s.replace('{ASSET_ZONE}', config.ASSET_ZONE)
	if hasattr(config,'TS_URI') :
		s = s.replace('{TS_URL}', config.TS_URI.split('/api/')[0])
		s = s.replace('{TS_ZONE}', config.TS_ZONE)
	authString = config.rmdAppClientId+":"+config.rmdAppSecret
	s = s.replace('{ENCODED_CLIENTID}', base64.b64encode(bytearray(authString, 'UTF-8')).decode("ascii"))
	if hasattr(config,'FDH_URL') :
		print("Replacing FDH_URL..."+config.FDH_URL)
		s = s.replace('{FDH_URL}', config.FDH_URL)
	if hasattr(config,'WEB_SOCKET_SERVER_HOST') :
		s = s.replace('{WEB_SOCKET_SERVER_HOST}', config.WEB_SOCKET_SERVER_HOST)
		s = s.replace('{LIVE_DATA_WS_URL}', config.LIVE_DATA_WS_URL)
	f = open(manifestLocation+"/manifest.yml", 'w')
	f.write(s)
	f.close()
	with open(manifestLocation+'/manifest.yml', 'r') as fin:
		print (fin.read())

def getValueFromManifest(manifestLocation, valueToGet):
	print("Current dir="+os.getcwd())
	value=''
	if os.path.isfile(manifestLocation + "/manifest.yml"):
		f = open(manifestLocation+"/manifest.yml")
		for line in f:
			print(line)
			if valueToGet in line:
				value = line.split(":")[1].strip()
		f.close()
	return value

def configureConnectServer(config, fileLocation):
	# create a backup
	if os.path.isfile(fileLocation + "/connect.js"):
		shutil.copy(fileLocation+"/connect.js", fileLocation+"/connect.js.bak")
	# copy template as manifest
	shutil.copy(fileLocation+"/connect.js.template", fileLocation+"/connect.js")
	s = open(fileLocation+"/connect.js").read()
	s = s.replace('{clientId}', config.rmdAppClientId)
	s = s.replace('{secret}', config.rmdAppSecret)
	s = s.replace('{UAA_SERVER_URL}', config.UAA_URI)
	s = s.replace('{ASSET_URL}', config.ASSET_URI)
	s = s.replace('{ASSET_ZONE}', config.ASSET_ZONE)
	s = s.replace('{TS_URL}', config.TS_URI.split('/api/')[0])
	s = s.replace('{TS_ZONE}', config.TS_ZONE)
	authString = config.rmdAppClientId+":"+config.rmdAppSecret
	s = s.replace('{ENCODED_CLIENTID}', base64.b64encode(bytearray(authString, 'UTF-8')).decode("ascii"))
	s = s.replace('{RMD_DATASOURCE_URL}', config.RMD_DATASOURCE_URL)
	s = s.replace('{LIVE_DATA_WS_URL}', config.LIVE_DATA_WS_URL)
	f = open(fileLocation+"/connect.js", 'w')
	f.write(s)
	f.close()
	# with open(fileLocation+'/connect.js', 'r') as fin:
	# 	print (fin.read())

def deployAnalyticReferenceAppFinalPrep(config):
	try:
		print("****************** Running deployAnalyticReferenceAppFinalPrep ******************")
		config.current='deployAnalyticReferenceAppFinalPrep'

		getPredixUAAConfigfromVcaps(config)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployAnalyticReferenceAppFinalPrep(config)
		else :
			raise

def sanityChecks(config):
	config.current='sanityChecks'
	# Sanity checks:
	jsonrequest = "cf apps | grep "+config.instanceName
	statementStatus  = subprocess.call(jsonrequest, shell=True)

	jsonrequest = "cf s | grep "+ config.instanceName
	statementStatus  = subprocess.call(jsonrequest, shell=True)

	getPredixUAAConfigfromVcaps(config)
	getVcapJsonForPredixBoot(config)
	getAssetURLandZone(config)
	getTimeseriesURLandZone(config)
	getPredixACSConfigfromVcaps(config)
	getFDHUrl(config)
	getAnalyticsUrl(config)
	getOrchClientUrl(config)

	#getRabbitMQConsumerUrl(config)

	print ('uaaAdmin= ' + config.uaaAdminSecret)
	print ('clientId= ' + config.rmdAppClientId)
	print ('clientSecret= ' + config.rmdAppSecret)
	print ('rmdUser= ' + config.rmdUser1)
	print ('rmdUserPass= ' + config.rmdUser1Pass)
	print ('rmdAdmin= ' + config.rmdAdmin1)
	print ('rmdAdminPass= ' + config.rmdAdmin1Pass)
	authString = config.rmdAppClientId+":"+config.rmdAppSecret
	print ('client basic auth= ' + base64.b64encode(bytearray(authString, 'UTF-8')).decode("ascii"))
	print ('UAA_SERVER_URL= ' + config.UAA_URI)
	print ('ASSET_URL= ' + config.ASSET_URI)
	print ('ASSET_ZONE= ' + config.ASSET_ZONE)
	print ('TS_URI= ' + config.TS_URI)
	print ('TS_ZONE= ' + config.TS_ZONE)
	print ('ACS_URI= ' + config.ACS_URI)
	print ('ACS_Zone_Id= ' + config.acsPredixZoneHeaderValue)
	#print ('RABBIT MQ CONSUMER TEMPLATE = ' + config.RABBITMQ_CONSUMER_URL)
	print ('RMD ANALYTICS URL = ' + config.RMD_ANALYTICS_URL)
	print ('FDH_URL= ' + config.FDH_URL)
	print ('RMD ORCHESTRATION CLIENT URL = ' + config.RMD_ORCH_URL)
	print ('RMD RABBITMQ SERVICE NAME=' + config.rmdRabbitMQ)
	print ('FieldChangedEvent-RabbitMQ Queue=' + config.fieldChangedEvent_MainQueue)
	print ('FieldChangedEvent-SampleFieldChangedEventFile=' + "rmd-orchestration/fieldchangedevent-consumer/src/test/resources/FieldChangedEvent.xml")
	print ('')
	print ('1. In a command window enter: cf curl /v2/service_instances?q=name:' + config.rmdRabbitMQ)
	print ('2. Using a browser, paste the dashboard_url and click enter')
	print ('3. Using a tool like Postman, query for the Asset at url '+ config.ASSET_URI + '/asset/compressor-2015.tag-extensions.crank-frame-discharge-pressure')
	print ( 'Ensure you have 3 headers: Authorization="Bearer <a bearer token from UAA>", Predix-Zone-Id=' + config.ASSET_ZONE + ', Content-Type=application/json')
	print ('4. Look for the Alert Status, which is one of the values the Analytic computes:')
	print ('assetId": "/asset/compressor-2015.tag-extensions.crank-frame-discharge-pressure",')
	print ('"attributes": {')
	print ('  "alertStatus": {')
	print ('    "complexType": "Attribute",')
	print ('    "enumeration": [],')
	print ('    "value": [')
	print ('      false')
	print ('    ]')
	print ('  },')
	print ('5. Try tailing the logs of the Analytic, cf logs ' + config.rmdAnalyticsAppName)
	print ('6. Using POSTMAN, If you change the false to true.')
	print ('7. Then using the RabbitMQ UI in the browser, put the FieldChangedEvent.xml contents in a message in the Queue')
	print ('8. You will see the logs move and when you GET the asset in Predix Asset, you will see the value has changed back to false')
