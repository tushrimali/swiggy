from endpoints import Controller
from AssignmentServer import AssignmentServer

class Default(Controller):
  def GET(self):
    return "Hi, I'm the Swiggy Delivery Assignment Server"

  def POST(self, **kwargs):
	a_s = AssignmentServer()
	return a_s.start(kwargs['orders'])