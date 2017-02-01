#######################################
# Begin Main script
#######################################
import sys
import refAnalyticsAppConfig as config
import refAnalyticsApp
import traceback


print ('environment : '+config.environment)
print ('continueFrom=' + config.continueFrom)
print ('only=' + config.only)
print("****************** Installing Analytics Reference Application ******************")
try:

	config.retryCount=0
	if config.only not in (''):
		if config.only in ('buildPredixSDKs'):
			refAnalyticsApp.buildPredixSDKs(config)
		if config.only in ('buildReferenceApp'):
			refAnalyticsApp.buildReferenceApp(config)
		if config.only in ('deployAnalyticReferenceAppDelete'):
			refAnalyticsApp.deployAnalyticReferenceAppDelete(config)
		if config.only in ('deployAnalyticReferenceAppSetUAA'):
			refAnalyticsApp.deployAnalyticReferenceAppSetUAA(config)
		if config.only in ('deployAnalyticReferenceAppSetACS'):
			refAnalyticsApp.deployAnalyticReferenceAppSetACS(config)
			refAnalyticsApp.deployAnalyticReferenceAppCreateAnalyticsInstance(config)
			refAnalyticsApp.deployAnalyticReferenceAppFinalPrep(config)
		if config.only in ('deployAnalyticReferenceAppCreateAnalyticsInstance'):
			refAnalyticsApp.deployAnalyticReferenceAppCreateAnalyticsInstance(config)
			refAnalyticsApp.deployAnalyticReferenceAppFinalPrep(config)
		if config.only in ('deployAnalyticReferenceAppAddAuthorities'):
			refAnalyticsApp.deployAnalyticReferenceAppAddAuthorities(config)
		#if config.only in ('deployAnalyticReferenceAppCreateFDH'):
		#	refAnalyticsApp.deployAnalyticReferenceAppCreateFDH(config)
		#if config.only in ('deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate'):
		#	refAnalyticsApp.deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate(config)
		if config.only in ('deployAnalyticReferenceAppCreateRMDAnalytics'):
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDAnalytics(config)
		if config.only in ('deployAnalyticReferenceAppCreateRMDOrchestrationClient'):
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDOrchestrationClient(config)
		if config.only in ('deployAnalyticReferenceAppFinalPrep'):
			refAnalyticsApp.deployAnalyticReferenceAppFinalPrep(config)


		refAnalyticsApp.sanityChecks(config)
	else :
		if config.continueFrom in ('all'):
			refAnalyticsApp.buildPredixSDKs(config)
			refAnalyticsApp.buildReferenceApp(config)
			refAnalyticsApp.deployAnalyticReferenceAppDelete(config)
			refAnalyticsApp.deployAnalyticReferenceAppSetUAA(config)
			refAnalyticsApp.deployAnalyticReferenceAppSetACS(config)
			refAnalyticsApp.deployAnalyticReferenceAppCreateAnalyticsInstance(config)
			refAnalyticsApp.deployAnalyticReferenceAppAddAuthorities(config)
			#refAnalyticsApp.deployAnalyticReferenceAppCreateFDH(config)
			#refAnalyticsApp.deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate(config)
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDAnalytics(config)
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDOrchestrationClient(config)
			refAnalyticsApp.sanityChecks(config)

		if config.continueFrom in ('continue','buildPredixSDKs'):
			config.continueFrom = 'continue'
			refAnalyticsApp.buildPredixSdks(config)
		if config.continueFrom in ('continue','buildReferenceApp'):
			config.continueFrom = 'continue'
			refAnalyticsApp.buildReferenceApp(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppDelete'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppDelete(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppSetUAA'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppSetUAA(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppSetACS'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppSetACS(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppCreateAnalyticsInstance'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppCreateAnalyticsInstance(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppAddAuthorities'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppAddAuthorities(config)
		#if config.continueFrom in ('continue','deployAnalyticReferenceAppCreateFDH'):
		#	config.continueFrom = 'continue'
		#	refAnalyticsApp.deployAnalyticReferenceAppCreateFDH(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppCreateRMDAnalytics'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDAnalytics(config)
		#if config.continueFrom in ('continue','deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate'):
		#	config.continueFrom = 'continue'
		#	refAnalyticsApp.deployAnalyticReferenceAppCreateRabbitMQConsumerTemplate(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppCreateRMDOrchestrationClient'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppCreateRMDOrchestrationClient(config)
		if config.continueFrom in ('continue','deployAnalyticReferenceAppFinalPrep'):
			config.continueFrom = 'continue'
			refAnalyticsApp.deployAnalyticReferenceAppFinalPrep(config)

	refAnalyticsApp.sanityChecks(config)

	print("*******************************************")
	print("**************** SUCCESS!! ****************")
	print("*******************************************")
except:
	print()
	print(traceback.print_exc())
	print()
	if config.only in (''):
		print ('Exception when running ' + config.current + '.  After repairing the problem, use "--continueFrom ' + config.current + '" switch to resume the install')
	print
	sys.exit(2)
