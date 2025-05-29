import os
from PyFlow.Core.PackageBase import PackageBase

class ACHHXBase(PackageBase):
	def __init__(self):
		super(ACHHXBase, self).__init__()
		self.analyzePackage( os.path.dirname(__file__))