import vakt

from .abac_pip import PIP
from .pdp import PDP


class ABACManager(object):
	"""
		Manager class to interact with ABAC operations
	"""

	@staticmethod
	def check_authorized(file, user, policies, action):
		pip = PIP(policies)

		inquiry = ABACManager.create_inquiry(user, file, action)

		pdp = PDP(pip, inquiry)

		return pdp.is_allowed()

	@staticmethod
	def create_inquiry(user, file, action):
		inq = vakt.Inquiry(action=action,
                   resource=file,
                   subject=user)

	       return inq 
