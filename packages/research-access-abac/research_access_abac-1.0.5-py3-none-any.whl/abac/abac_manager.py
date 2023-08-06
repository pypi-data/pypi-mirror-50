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
			subjects=[ABACManager.subject_to_abac_dict(subjects)],
			effect=vakt.ALLOW_ACCESS if verdict else vakt.DENY_ACCESS,
		)

		return policy.to_json()

	@staticmethod
	def subject_to_abac_dict(subject):
		subject_dict = {}
		for k, v in subject.items():
			if v == 'any':
				subject_dict[k] = Any()
			else:
				subject_dict[k]  = Eq(v)

		print("subject_dict: {}".format(subject_dict))

		return subject_dict



	@staticmethod
	def create_policy_from_json(jsonified_policy):
		return vakt.Policy.from_json(jsonified_policy)
