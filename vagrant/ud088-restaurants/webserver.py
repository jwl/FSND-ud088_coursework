from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"

                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<h2>Enter the new restaurant's name below:</h2>"
                output += "<input name='new_restaurant' type='text' placeholder='New Restaurant Name'><input type='submit' value='Create'> </form>"

                output += "</br><a href='/restaurants'>Back to list</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                # Page for editing a restaurant's name

                # extract restaurant ID and lookup restaurant in DB
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                        id=restaurantID).one()

                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantID
                    output += "<h2>Enter the new name for %s</h2>" % \
                            restaurant.name
                    output += "<input name='new_name' type='text' placeholder='%s'><input type='submit' value='Change'> </form>" % restaurant.name
                    output += "</br><a href='/restaurants'>Back to list</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                return

            if self.path.endswith("/delete"):
                # Page for deleting a restaurant from DB

                # extract restaurant Id and lookup restaurant in DB
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                        id = restaurantID).one()

                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Are you sure you want to delete %s?</h2>" % \
                            restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantID
                    output += "<input type='submit' value='Delete'> </form>"
                    output += "<a href='/restaurants'>Back to list</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output


            if self.path.endswith("/restaurants"):
                # List all restaurants in database
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<p>"
                    output += "%s</br>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % \
                            restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % \
                            restaurant.id
                    output += "</p>"
                output += "Add a <a href='/restaurants/new'>" \
                        "new restaurant</a>!"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#161Hola! <a href='/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            # Execute restaurant deletion
            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                        id = restaurantID).one()
                if restaurant != []:
                    print("Deleting restaurant %s", restaurant.name)
                    session.delete(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            # Execute name change for a given restaurant
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_name')
                    restaurantID = self.path.split("/")[2]
                    print "restaurant ID is: ", restaurantID

                # lookup existing restaurant, edit, and commit change
                restaurant = session.query(Restaurant).filter_by(
                        id=restaurantID).one()
                if restaurant != []:
                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')
                    print "restaurant name is: ", messagecontent[0]

                # Create new Restaurant and add to DB
                new_restaurant = Restaurant(name = messagecontent[0])
                session.add(new_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                # output = ""
                # output += "<html><body>"
                # output += "<h2> New restaurant added! </h2>"
                # output += "<h1> %s </h1>" % messagecontent[0]
                # output += "</br><a href='/restaurants'>Back to list</a>"
                # output += "</body></html>"



            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'> </form>"
                output += "</body></html>"


            self.wfile.write(output)
            print output

        except:
            pass

def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()


