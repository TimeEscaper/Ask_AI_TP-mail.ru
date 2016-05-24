def application(env, start_response):
	status = '200 OK'
	headers = [
		('Content-type', 'text/plain')
	]

	post_query = env['wsgi.input'].read()
	get_query = env['QUERY_STRING']
	
	post_string = '\n'.join(['%s' % param for param in post_query.split('&')])
	get_string = '\n'.join(['%s' % param for param in get_query.split('&')])
	
	body = 'Hello, World!\n\nPOST data:\n%s\n\nGET data:\n%s\n' % (post_string,get_string)
	
	return [body]
 	 
