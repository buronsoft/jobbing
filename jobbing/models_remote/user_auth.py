# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from jobbing.models.base_model_ import Model
from jobbing import util


class UserAuth(Model):
	def __init__(self,
			user_auth_id:int = None,
			user_auth_password:str = None,
			user_auth_pass_date:str = None,
			user_model_id:int = None,
			user_auth_updated_date:str = None,
			user_auth_name:str = None,
			user_auth_email:str = None): # noqa: E501

		self.swagger_types = {
			'user_auth_id': int,
			'user_auth_password': str,
			'user_auth_pass_date': str,
			'user_model_id': int,
			'user_auth_updated_date': str,
			'user_auth_name': str,
			'user_auth_email': str
		}

		self.attribute_map = {
			'user_auth_id': 'user_auth_id',
			'user_auth_password': 'user_auth_password',
			'user_auth_pass_date': 'user_auth_pass_date',
			'user_model_id': 'user_model_id',
			'user_auth_updated_date': 'user_auth_updated_date',
			'user_auth_name': 'user_auth_name',
			'user_auth_email': 'user_auth_email'
		}

		self._user_auth_id = user_auth_id
		self._user_auth_password = user_auth_password
		self._user_auth_pass_date = user_auth_pass_date
		self._user_model_id = user_model_id
		self._user_auth_updated_date = user_auth_updated_date
		self._user_auth_name = user_auth_name
		self._user_auth_email = user_auth_email

	@classmethod
	def from_dict(cls, dikt) -> 'UserAuth':
		return util.deserialize_model(dikt, cls)

	@property
	def user_auth_id(self) -> int:
		return self._user_auth_id

	@user_auth_id.setter
	def user_auth_id(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_id`, must not be `None`")  # noqa: E501
		self._user_auth_id = param

	@property
	def user_auth_password(self) -> str:
		return self._user_auth_password

	@user_auth_password.setter
	def user_auth_password(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_password`, must not be `None`")  # noqa: E501
		self._user_auth_password = param

	@property
	def user_auth_pass_date(self) -> str:
		return self._user_auth_pass_date

	@user_auth_pass_date.setter
	def user_auth_pass_date(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_pass_date`, must not be `None`")  # noqa: E501
		self._user_auth_pass_date = param

	@property
	def user_model_id(self) -> int:
		return self._user_model_id

	@user_model_id.setter
	def user_model_id(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_model_id`, must not be `None`")  # noqa: E501
		self._user_model_id = param

	@property
	def user_auth_updated_date(self) -> str:
		return self._user_auth_updated_date

	@user_auth_updated_date.setter
	def user_auth_updated_date(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_updated_date`, must not be `None`")  # noqa: E501
		self._user_auth_updated_date = param

	@property
	def user_auth_name(self) -> str:
		return self._user_auth_name

	@user_auth_name.setter
	def user_auth_name(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_name`, must not be `None`")  # noqa: E501
		self._user_auth_name = param

	@property
	def user_auth_email(self) -> str:
		return self._user_auth_email

	@user_auth_email.setter
	def user_auth_email(self, param):
		if param is None:
			raise ValueError("Invalid value for `user_auth_email`, must not be `None`")  # noqa: E501
		self._user_auth_email = param

