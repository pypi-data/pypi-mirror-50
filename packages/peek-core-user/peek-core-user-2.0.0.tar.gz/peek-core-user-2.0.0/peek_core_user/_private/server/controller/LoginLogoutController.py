import logging
from datetime import datetime
from typing import List

import pytz
from peek_core_device.server.DeviceApiABC import DeviceApiABC
from peek_core_user._private.server.api.UserHookApi import UserHookApi
from peek_core_user._private.server.api.UserInfoApi import UserInfoApi
from peek_core_user._private.server.auth_connectors.InternalAuth import InternalAuth
from peek_core_user._private.server.auth_connectors.LdapAuth import LdapAuth
from peek_core_user._private.storage.Setting import \
    globalSetting, ALLOW_MULTI_DEVICE_LOGIN, INTERNAL_AUTH_ENABLED_FOR_FIELD, \
    LDAP_AUTH_ENABLED, INTERNAL_AUTH_ENABLED_FOR_OFFICE
from peek_core_user._private.storage.UserLoggedIn import UserLoggedIn
from peek_core_user._private.tuples.LoggedInUserStatusTuple import \
    LoggedInUserStatusTuple
from peek_core_user._private.tuples.UserLoggedInTuple import UserLoggedInTuple
from peek_core_user.server.UserDbErrors import UserIsNotLoggedInToThisDeviceError
from peek_core_user.tuples.login.UserLoginAction import UserLoginAction
from peek_core_user.tuples.login.UserLoginResponseTuple import UserLoginResponseTuple
from peek_core_user.tuples.login.UserLogoutAction import UserLogoutAction
from peek_core_user.tuples.login.UserLogoutResponseTuple import UserLogoutResponseTuple
from peek_plugin_base.storage.DbConnection import DbSessionCreator
from twisted.cred.error import LoginFailed
from twisted.internet.defer import Deferred, inlineCallbacks
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

logger = logging.getLogger(__name__)

USER_ALREADY_LOGGED_ON_KEY = 'pl-user.USER_ALREADY_LOGGED_ON'
DEVICE_ALREADY_LOGGED_ON_KEY = 'pl-user.DEVICE_ALREADY_LOGGED_ON_KEY'


class LoginLogoutController:

    def __init__(self, deviceApi: DeviceApiABC,
                 dbSessionCreator: DbSessionCreator):
        self._deviceApi: DeviceApiABC = deviceApi
        self._hookApi: UserHookApi = None
        self._infoApi: UserInfoApi = None
        self._dbSessionCreator: DbSessionCreator = dbSessionCreator
        self._clientTupleObservable: TupleDataObservableHandler = None
        self._adminTupleObservable: TupleDataObservableHandler = None

    def setup(self, clientTupleObservable,
              adminTupleObservable,
              hookApi: UserHookApi,
              infoApi: UserInfoApi):
        self._clientTupleObservable = clientTupleObservable
        self._adminTupleObservable = adminTupleObservable
        self._hookApi = hookApi
        self._infoApi = infoApi

    def shutdown(self):
        self._clientTupleObservable = None
        self._hookApi = None
        self._infoApi = None

    def _checkPassBlocking(self, ormSession, userName, password) -> List[str]:
        if not password:
            raise LoginFailed("Password is empty")

        # TODO Make the client tell us if it's for office or field

        lastException = None

        # TRY INTERNAL IF ITS ENABLED
        try:
            if globalSetting(ormSession, INTERNAL_AUTH_ENABLED_FOR_FIELD):
                return InternalAuth().checkPassBlocking(ormSession, userName,
                                                        password, InternalAuth.FOR_FIELD)

        except Exception as e:
            lastException = e

        # TRY INTERNAL IF ITS ENABLED
        try:
            if globalSetting(ormSession, INTERNAL_AUTH_ENABLED_FOR_OFFICE):
                return InternalAuth().checkPassBlocking(ormSession, userName,
                                                        password, InternalAuth.FOR_OFFICE)

        except Exception as e:
            lastException = e

        # TRY LDAP IF ITS ENABLED
        try:
            if globalSetting(ormSession, LDAP_AUTH_ENABLED):
                return LdapAuth().checkPassBlocking(ormSession, userName,
                                                    password, LdapAuth.FOR_OFFICE)

        except Exception as e:
            lastException = e

        if lastException:
            raise lastException

        raise Exception("No authentication handlers are enabled, enable one in settings")

    def _checkGroupBlocking(self, ormSession, groups: List[str]):
        pass

    @deferToThreadWrapWithLogger(logger)
    def _logoutInDb(self, logoutTuple: UserLogoutAction):
        """
        Returns Deferred[UserLogoutResponseTuple]
        """

        session = self._dbSessionCreator()
        try:
            # Check if the user is actually logged into this device.
            qry = (
                session.query(UserLoggedIn)
                    .filter(UserLoggedIn.userName == logoutTuple.userName)
                    .filter(
                    UserLoggedIn.deviceToken == logoutTuple.deviceToken)
            )

            if qry.count() == 0:
                raise UserIsNotLoggedInToThisDeviceError(logoutTuple.userName)

            session.delete(qry.one())
            session.commit()

        finally:
            session.close()

    @inlineCallbacks
    def logout(self, logoutTuple: UserLogoutAction) -> Deferred:
        """ Logout

        :param logoutTuple: The tuple containing the information to process
                                for the logout.

        :return A deferred that fires with List[UserLogoutResponseTuple]
        """

        deviceDescription = yield self._deviceApi.deviceDescription(
            logoutTuple.deviceToken
        )

        response = UserLogoutResponseTuple(
            userName=logoutTuple.userName,
            deviceToken=logoutTuple.deviceToken,
            deviceDescription=deviceDescription,
            acceptedWarningKeys=logoutTuple.acceptedWarningKeys,
            succeeded=True)

        # Give the hooks a chance to fail the logout
        yield self._hookApi.callLogoutHooks(response)

        # If there are no problems, proceed with the logout.
        if response.succeeded:
            yield self._logoutInDb(logoutTuple)

        self._clientTupleObservable.notifyOfTupleUpdate(
            TupleSelector(UserLoggedInTuple.tupleType(),
                          selector=dict(userName=logoutTuple.userName))
        )

        self._adminTupleObservable.notifyOfTupleUpdateForTuple(
            LoggedInUserStatusTuple.tupleType()
        )

        return response

    @deferToThreadWrapWithLogger(logger)
    def _loginInDb(self, loginTuple: UserLoginAction):
        """
        Returns Deferred[UserLoginResponseTuple]

        """

        userName = loginTuple.userName
        password = loginTuple.password
        acceptedWarningKeys = set(loginTuple.acceptedWarningKeys)
        deviceToken = loginTuple.deviceToken
        vehicle = loginTuple.vehicleId

        responseTuple = UserLoginResponseTuple(
            userName=userName,
            userToken="Not implemented",
            succeeded=False,
            acceptedWarningKeys=loginTuple.acceptedWarningKeys,
            vehicleId=loginTuple.vehicleId
        )

        if not deviceToken:
            raise Exception("peekToken must be supplied")

        thisDeviceDescription = self._deviceApi.deviceDescriptionBlocking(deviceToken)

        ormSession = self._dbSessionCreator()
        try:
            singleDevice = not globalSetting(ormSession, ALLOW_MULTI_DEVICE_LOGIN)
            groups = self._checkPassBlocking(ormSession, userName, password)
            self._checkGroupBlocking(ormSession, groups)

            responseTuple.userDetail = self._infoApi.userBlocking(userName, ormSession)

            # Find any current login sessions
            userLoggedIn = (ormSession.query(UserLoggedIn)
                            .filter(UserLoggedIn.userName == userName)
                            .all())
            userLoggedIn = userLoggedIn[0] if userLoggedIn else None

            loggedInElsewhere = (
                ormSession.query(UserLoggedIn)
                    .filter(UserLoggedIn.deviceToken != deviceToken)
                    .filter(UserLoggedIn.userName == userName)
                    .all())

            if singleDevice and len(loggedInElsewhere) not in (0, 1):
                raise Exception("Found more than 1 ClientDevice for"
                                + (" token %s" % deviceToken))

            loggedInElsewhere = loggedInElsewhere[0] if loggedInElsewhere else None

            sameDevice = userLoggedIn and loggedInElsewhere is None

            # If the user is logged in, but not to this client device, raise exception
            if singleDevice and userLoggedIn and not sameDevice:
                if USER_ALREADY_LOGGED_ON_KEY in acceptedWarningKeys:
                    self._forceLogout(ormSession,
                                      userName,
                                      loggedInElsewhere.deviceToken)
                    userLoggedIn = False

                else:
                    otherDeviceDescription = self._deviceApi.deviceDescriptionBlocking(
                        loggedInElsewhere.deviceToken
                    )

                    # This is false if the logged in device has been removed from
                    # enrollment
                    if otherDeviceDescription:
                        responseTuple.setFailed()
                        responseTuple.addWarning(
                            USER_ALREADY_LOGGED_ON_KEY,
                            "User %s is already logged in, on device %s" % (
                                userName, otherDeviceDescription)
                        )

                        return responseTuple

                    # Else, The old device has been deleted,
                    # Just let them login to the same device.
                    self._forceLogout(ormSession,
                                      loggedInElsewhere.userName,
                                      loggedInElsewhere.deviceToken)

            # If we're logging into the same device, but already logged in
            if sameDevice:  # Logging into the same device
                sameDeviceDescription = self._deviceApi.deviceDescriptionBlocking(
                    userLoggedIn.deviceToken
                )

                responseTuple.deviceToken = userLoggedIn.deviceToken
                responseTuple.deviceDescription = sameDeviceDescription
                responseTuple.succeeded = True
                return responseTuple

            anotherUserOnThatDevice = (
                ormSession.query(UserLoggedIn)
                    .filter(UserLoggedIn.deviceToken == deviceToken)
                    .filter(UserLoggedIn.userName != userName)
                    .all()
            )

            if anotherUserOnThatDevice:
                anotherUserOnThatDevice = anotherUserOnThatDevice[0]
                if DEVICE_ALREADY_LOGGED_ON_KEY in acceptedWarningKeys:
                    self._forceLogout(ormSession,
                                      anotherUserOnThatDevice.userName,
                                      anotherUserOnThatDevice.deviceToken)

                else:
                    responseTuple.setFailed()
                    responseTuple.addWarning(
                        DEVICE_ALREADY_LOGGED_ON_KEY,
                        "User %s is currently logged into this device : %s" % (
                            anotherUserOnThatDevice.userName,
                            thisDeviceDescription)
                    )

                    return responseTuple

            # Create the user logged in entry

            newUser = UserLoggedIn(userName=userName,
                                   loggedInDateTime=datetime.now(pytz.utc),
                                   deviceToken=deviceToken,
                                   vehicle=vehicle)
            ormSession.add(newUser)
            ormSession.commit()

            # Respond with a successful login
            responseTuple.deviceToken = deviceToken
            responseTuple.deviceDescription = thisDeviceDescription
            responseTuple.succeeded = True
            return responseTuple

        finally:
            ormSession.close()

    @inlineCallbacks
    def login(self, loginTuple: UserLoginAction):
        """
        Returns Deferred[UserLoginResponseTuple]

        """
        loginResponse = None
        try:
            loginResponse = yield self._loginInDb(loginTuple)
            yield self._hookApi.callLoginHooks(loginResponse)

        # except UserAlreadyLoggedInError as e:
        #     pass
        #
        # except DeviceAlreadyLoggedInError as e:
        #     pass
        #
        # except UserIsNotLoggedInToThisDeviceError as e:
        #     pass

        except Exception as e:

            # Log the user out again if the hooks fail
            logoutTuple = UserLogoutAction(
                userName=loginTuple.userName,
                deviceToken=loginTuple.deviceToken)

            # Force logout, we don't care if it works or not.
            try:
                yield self._logoutInDb(logoutTuple)
            except UserIsNotLoggedInToThisDeviceError:
                pass

            raise e

        self._clientTupleObservable.notifyOfTupleUpdate(
            TupleSelector(UserLoggedInTuple.tupleType(),
                          selector=dict(userName=loginTuple.userName))
        )

        self._adminTupleObservable.notifyOfTupleUpdateForTuple(
            LoggedInUserStatusTuple.tupleType()
        )

        return loginResponse

    def _forceLogout(self, ormSession, userName, deviceToken):
        (
            ormSession.query(UserLoggedIn)
                .filter(UserLoggedIn.userName == userName)
                .filter(UserLoggedIn.deviceToken == deviceToken)
                .delete(synchronize_session=False)
        )
