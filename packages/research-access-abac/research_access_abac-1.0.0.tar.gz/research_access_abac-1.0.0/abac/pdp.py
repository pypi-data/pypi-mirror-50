import vakt


class PDP(object):
	"""docstring for PDP"""
	def __init__(self, pip, inquiry):
		self.pip = pip
		self.inquiry = inquiry

		self.create_guard()

	def create_guard(self):
		self.guard = vakt.Guard(self.pip.get_policies_as_storage(), vakt.RulesChecker())

	def is_allowed(self):
		return self.guard.is_allowed(self.inquiry)

	def __repr__(self):
		return "PDP<pip={}, inquiry={}>".format(self.pip, self.inquiry)
		