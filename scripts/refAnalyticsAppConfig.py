import os
import subprocess
import sys, getopt
import re

def checkRequirements():
    try:
        cfTarget = subprocess.check_output(["cf", "target"])
        print (cfTarget)
        user = cfTarget.decode('utf8').split('User:')[1].split('Org:')[0]
        org = cfTarget.decode('utf8').split('Org:')[1].split('Space:')[0]
        space = cfTarget.decode('utf8').split('Space')[1]
        print("cf login detected")
        return (user.strip(), org, space)
    except subprocess.CalledProcessError as e:
        sys.exit("Please login to CF.")

#global org
#global space
#global user
global instanceName
global BASE_DIR
global BASE_PREDIX_DIR
global rmdUaaName
global rmdAcsName
global rmdPredixAssetName
global rmdPredixTimeseriesName
global rmdRabbitMQ
global rmdRedis
global predixbootAppName
global dataSeedAppName
global dataSourceAppName
global fdhAppName
#global httpDataRiverAppName
global dataIngestionAppName
global machineSimulatorAppName
global uiAppName
global rmdAnalyticsAppName
global rmdOrchestrationClientAppName
global predixUaaService
global predixAcsService
global predixAssetService
global predixTimeSeriesService
global predixRedis
global predixUaaServicePlan
global predixAcsServicePlan
global predixAssetServicePlan
global predixTimeSeriesServicePlan
global predixRedisPlan
global rmdAppClientId
global rmdAppSecret
global uaaAdminSecret
global clientAuthorities
global clientScope
global projectDir
global predixProject
global rmdUser1
global rmdUser1Pass
global deleteAppsAndServices
global environment
global mvnsettings
global pullsubmodules
global mavenRepo
global continueFrom
global artifactoryrepo
global artifactoryuser
global artifactorypass

try:
    #set defaults
    instanceName = ""
    #mvnsettings = "~/.m2/settings.xml"
    from os.path import expanduser
    homeDir = expanduser("~")

    mvnsettings=os.path.join(homeDir, ".m2", "settings.xml")

    #mvnsettings = ""
    pullsubmodules = 'y'
    mavenRepo = ""
    deleteAppsAndServices = "n"
    environment = "PROD"
    continueFrom = "all"
    only = ""
    fastinstall = 'y'
    artifactoryrepo = ""
    artifactoryuser = ""
    artifactorypass = ""
    #override with arguments
    opts, args = getopt.getopt(sys.argv[1:],"d:e:i:s:p:r:a:v:c:o:f:x:y:z:",["delete=","environment=","instanceName=","mvnsettings=","pullsubmodules=","mavenrepo=","continueFrom=","only=", "fastinstall=", "artifactoryrepo=", "artifactoryuser=", "artifactorypass="])
except getopt.GetoptError:
    print('Exception when parsing : '+sys.argv[0]+' -e (R2/PROD) -i <Instance appender> -s <mvnsettings>')
    sys.exit(2)
for opt, arg in opts:
    print ('opt=' + opt + ' arg=' + arg)
    if opt == '-h':
        print(sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>')
        sys.exit()
    elif opt in ("-i", "--instanceappender"):
        instanceName = arg
    elif opt in ("-d", "--delete"):
        deleteAppsAndServices = arg
    elif opt in ("-e", "--environment"):
        environment = arg
    elif opt in ("-s", "--mvnsettings"):
        mvnsettings = arg
    elif opt in ("-p","--pullsubmodules"):
        pullsubmodules = arg
    elif opt in ("-r","--mavenrepo"):
        mavenRepo = arg
    elif opt in ("-v","--verbose"):
        verbose = true;
    elif opt in ("-c","--continueFrom"):
        continueFrom = arg;
    elif opt in ("-o","--only"):
        only = arg;
    elif opt in ("-f","--fastinstall"):
        fastinstall = arg;
    elif opt in ("-x","--artifactoryrepo"):
        artifactoryrepo = arg;
    elif opt in ("-y","--artifactoryuser"):
        artifactoryuser = arg;
    elif opt in ("-z","--artifactorypass"):
        artifactorypass = arg;

#if mvnsettings == "":
#        print sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>'
#        print 'Maven settings file is a mandatory argument.'
#        sys.exit()

# check check login
user, org, space = checkRequirements()
if len(instanceName) == 0:
    instanceName = user.strip().split("@")[0].replace('.', '_')
print ('Creating instance with your instance name ===', instanceName)

# check or create a directory for Reference application
BASE_DIR = os.getcwd()
BASE_PREDIX_DIR = "PredixApps"

# Reference App Service Instance Names
rmdUaaName = instanceName+"-uaa"
rmdAcsName = instanceName+"-acs"
rmdPredixAssetName = instanceName+"-asset"
rmdPredixTimeseriesName = instanceName+"-time-series"
rmdRabbitMQ= instanceName+"-rabbitmq"


predixbootRepoName="Predix-HelloWorld-WebApp"
predixSDKs="predix-sdks"

# Predix Application Names
print ('instanceName=' + instanceName)
predixbootAppName = instanceName+"-hello-world"
websocketAppName = instanceName+"-websocket-server"
fdhAppName = instanceName+"-data-exchange"
rabbitMQConsumerAppName = instanceName+"-rabbitmq-consumer-template"
rmdAnalyticsAppName = instanceName+"-rmd-analytics"
rmdOrchestrationClientAppName = instanceName+"-fce-consumer"

if environment == 'PROD':
    # Predix Service Instance Name for VPC
    predixUaaService = "predix-uaa"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset"
    predixTimeSeriesService = "predix-timeseries"
    predixRedis = "redis"
    predixRabbitMQ = "p-rabbitmq-35"
    predixAnalyticsCatalog = "predix-analytics-catalog"
    predixAnalyticsRuntime = "predix-analytics-runtime"

    predixUaaServicePlan = "Tiered"
    predixAcsServicePlan = "Tiered"
    predixAssetServicePlan = "Tiered"
    predixTimeSeriesServicePlan = "Bronze"
    predixRedisPlan = "shared-vm"
    predixRabbitMQPlan = "standard"
    predixAnalyticsCatalogPlan = "Free"
    predixAnalyticsRuntimePlan = "Free"

    artifactoryrepo = "https://artifactory.predix.io/artifactory/PREDIX-EXT"
elif environment == 'FREE':
    predixUaaService = "predix-uaa"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset-sysint"
    predixTimeSeriesService = "predix-timeseries-sysint"
    predixRedis = "p-redis"
    predixRabbitMQ = "p-rabbitmq-35"
    predixAnalyticsCatalog = "predix-analytics-catalog-sysint"
    predixAnalyticsRuntime = "predix-analytics-runtime-sysint"

    predixUaaServicePlan = "free"
    predixAcsServicePlan = "free"
    predixAssetServicePlan = "Beta"
    predixTimeSeriesServicePlan = "Beta"
    predixRedisPlan = "shared-vm"
    predixRabbitMQPlan = "standard"
    predixAnalyticsCatalogPlan = "Beta"
    predixAnalyticsRuntimePlan = "Beta"
elif environment == 'HACK' :
    # Predix Service Instance Name for sysint
    predixUaaService = "predix-uaa-training"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset"
    predixTimeSeriesService = "predix-timeseries"
    predixPostgres = "rdpg"
    predixRedis = "redis"
    predixRabbitMQ = "rabbitmq-36"
    predixAnalyticsCatalog = "predix-analytics-catalog"
    predixAnalyticsRuntime = "predix-analytics-runtime"

    predixUaaServicePlan = "Free"
    predixAcsServicePlan = "Free"
    predixAssetServicePlan = "Free"
    predixTimeSeriesServicePlan = "Free"
    predixPostgresPlan = "Free"
    predixRabbitMQPlan = "standard"
    predixRedisPlan = "shared-vm"
    predixBlobstorePlan = "Tiered"
    predixAnalyticsCatalogPlan = "Free"
    predixAnalyticsRuntimePlan = "Free"
else :
    # Predix Service Instance Name for sysint
    predixUaaService = "predix-uaa-sysint"
    predixAcsService = "predix-acs-sysint"
    predixAssetService = "predix-asset-sysint"
    predixTimeSeriesService = "predix-timeseries-sysint"
    predixRedis = "p-redis"
    predixRabbitMQ = "p-rabbitmq-35"
    predixAnalyticsCatalog = "predix-analytics-catalog-sysint"
    predixAnalyticsRuntime = "predix-analytics-runtime-sysint"

    predixUaaServicePlan = "free"
    predixAcsServicePlan = "free"
    predixAssetServicePlan = "Beta"
    predixTimeSeriesServicePlan = "Beta"
    predixRedisPlan = "shared-vm"
    predixRabbitMQPlan = "standard"
    predixAnalyticsCatalogPlan = "Beta"
    predixAnalyticsRuntimePlan = "Beta"

#Reference application client id
rmdAppClientId = "app_client_id"
rmdAppSecret = "secret"
#UAA Admin Account
uaaAdminSecret = "secret"
clientGrantType = ["authorization_code","client_credentials","refresh_token","password"]
clientAuthorities = ["openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write","uaa.resource","uaa.none"]
clientScope = ["uaa.none","openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write"]

projectDir = "predix-microservice-templates"
predixProject = projectDir+".git"
#UAA User account for logging in to RMD Ref App
rmdUser1 = "app_user_1"
rmdUser1Pass = "app_user_1"
#Admin User that is allowed to add asset data
rmdAdmin1 = "app_admin_1"
rmdAdmin1Pass = "app_admin_1"
acsPolicyName= "refapp-acs-policy"
