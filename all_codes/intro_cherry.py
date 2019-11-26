import cherrypy

class HelloWorld():
    @cherrypy.expose
    def index(self):
        return "Hello Rasp Pi!"
    
    @cherrypy.expose
    def sayHello(self, myFriend="my friend"):
        return "Hello "+ myFriend

cherrypy.quickstart(HelloWorld())
    