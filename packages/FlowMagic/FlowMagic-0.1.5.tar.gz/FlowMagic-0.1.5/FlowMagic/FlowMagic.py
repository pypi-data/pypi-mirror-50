import json,traceback,os,logging



logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
#env = os.environ
#logging.info("All Environment Variables")
#logging.info(os.environ)
#try:
#	logging.info('Input Paths %s', json.loads(env['input_path']))
#except Exception as e:
#	logging.error("Input path not found")


def info_log( *args ):
#	for info in args:
		logging.info( args  )

def err_log( *args ):
#	for err in args:
		logging.error( args )

def debug( *args ):
#	for data in args:
		logging.debug( args  )




def base_input_path( path=None ):
	try:
		return json.loads(os.environ.get('input_path'))

	except (Exception, IndexError) as e:
		if path!=None:	return path
		return traceback.format_exc()
		
def base_output_path( path=None ):

	try:
		out_path = json.loads(os.environ.get('output_path')  ) 
		for output_folder in out_path:
			os.makedirs( output_folder )
		return out_path
	except (Exception, IndexError) as e:
		if path!=None:	return path
		return traceback.format_exc()


def getSystemValue( key=None ):
	if key==None: return os.environ
	return os.environ.get( key )


def input_tree_path( obj , prevPath ,k ):

	if obj['type'] == 'dir':
		for x in obj['children']:
			#print(  os.path.join(prevPath,x['name']) )
			input_tree_path( x, os.path.join(prevPath,x['name']),k )  	
	elif obj['type'] == 'file':
		#print(  prevPath+ "."+obj['endsWith'] ) 
		k.append( prevPath+ "."+obj['endsWith']  )

def configJsonFile():
	configFileData={}
	with open( 'config.json' ) as json_file:
		configFileData = json.load(json_file)
	return configFileData

