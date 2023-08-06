import uuid

import vakt
from vakt.rules import Eq, Any, StartsWith, And, Greater, Less

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

	@staticmethod
	def create_jsonified_policy(actions, resources, subjects, verdict):
		print("actions: {}, project_attr: {}, researcher_attr: {}, verdict: {}".format(actions, resources, subjects, verdict))

		policy = vakt.Policy(
			str(uuid.uuid4()),
			actions=[Eq(action) for action in actions],
			resources=[{k: Eq(v)} for k, v in resources.items()],
			subjects=[{k: Eq(v)} for k, v in subjects.items()], 
			effect=vakt.ALLOW_ACCESS if verdict else vakt.DENY_ACCESS,
		)

		return policy.to_json()
