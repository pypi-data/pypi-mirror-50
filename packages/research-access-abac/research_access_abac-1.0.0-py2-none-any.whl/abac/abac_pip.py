import vakt


class PIP(object):

	def __init__(self, policies):
		self.policies = policies

	def get_policies_as_storage(self):
		storage = vakt.MemoryStorage()

		for policy in self.policies:
			storage.add(policy)

		return storage

	def __repr__(self):
		return "PIP<policies={}>".format(
			self.policies)
