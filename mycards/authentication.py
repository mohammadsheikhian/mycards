from itsdangerous import JSONWebSignatureSerializer
from nanohttp import context, HTTPStatus, HTTPUnauthorized
from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession

from .models import Member


class Authenticator(StatefulAuthenticator):

    @staticmethod
    def safe_member_lookup(condition):
        member = DBSession.query(Member).filter(condition).one_or_none()
        if member is None:
            raise HTTPStatus('400 Incorrect Email Or Password')

        return member

    def create_principal(self, member_id=None, session_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        principal = member.create_jwt_principal()

        return principal

    def create_refresh_principal(self, member_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        return member.create_refresh_principal()

    def validate_credentials(self, email):
        member = self.safe_member_lookup(Member.email == email)
        return member

