#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

""" Aplicación que crea distintas apps en función del recurso que le pida el usuario"""

import socket


class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        return request.split()[1][1:]

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>Hi!</h1></body></html>\r\n\r\n"+
                parsedRequest)

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        try:
            while True:
                print ('Waiting for connections')
                (recvSocket, address) = mySocket.accept()
                print ('HTTP request received (going to parse and process):')
                request = recvSocket.recv(2048).decode('utf-8')
                parsedRequest = self.parse(request)
                recurso = parsedRequest
                print ('Recurso pedido: ' + recurso)
                if recurso == 'hola':
                    hiApp = HolaApp()
                    (returnCode, htmlAnswer) = hiApp.process(parsedRequest)
                elif recurso == 'adios':
                    byeApp = AdiosApp()
                    (returnCode, htmlAnswer) = byeApp.process(parsedRequest)
                else:
                    badApp= RequestFail()
                    (returnCode, htmlAnswer) = badApp.process(parsedRequest)
                #(returnCode, htmlAnswer) = self.process(parsedRequest)
                print ('Answering back...')
                recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n", 'utf-8'))
                recvSocket.close()
        except KeyboardInterrupt:
            mySocket.close()
            print('\r\nClosing program')

class HolaApp():
    def process(self, parsedRequest):
            print('Me han llamado')
            return '200 OK', 'hola bro'

class AdiosApp():
    def process(self, parsedRequest):
            return '200 OK', '<html><body>adios bro</html></body>'

class RequestFail():
    def process(self, request):
            print("El recurso no es válido")
            return '404 Not Found', "<!doctype html> <h1> 404 Not Found</h1><p>El recurso no es valido</p>"
            
if __name__ == "__main__":
    test1 = webApp("localhost", 1234)
    #lo que haya por debajo de test1 se ejecuta cuando se acabe el servidor
