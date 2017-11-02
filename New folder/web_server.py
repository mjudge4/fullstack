from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

#Define the Web Server class and extend from BaseHTTPRequestHandler
class WebServerHandler(BaseHTTPRequestHandler):
    
    #Handles all the GET requests our server recieves
    def do_GET(self):
        #looks for path ending with hello
        if self.path.endswith("/hello"):
            #sends response code 200 indicating successful GET request
            self.send_response(200)
            #indicates that we are replying in the form of text to our client
            self.send_header('Content-type', 'text/html')
            #sends a blank line, indicating the end of our HTTP headers
            self.end_headers()

            message = ""
            message += "<html><body>Hello!</body></html>"
            self.wfile.write(message)
            print message
            return
        
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)        
        
#Main method
def main():
    #Creates instance of a HTTP Server Class prodided the exeption is not held (User hitting Ctrl + c)
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "The Web server is running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, shutting down the server"
        server.socket.close()

#runs the main method when the python interpreter executes the script
if __name__ == '__main__':
    main()
    
