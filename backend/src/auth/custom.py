from typing import Type

from fastapi import (
    APIRouter, Body, Depends,
    HTTPException, Request, Response, status
    )

# from pydantic import EmailStr

from fastapi_users import FastAPIUsers, exceptions, models, schemas
from fastapi_users.authentication import Authenticator
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.router.common import ErrorCode, ErrorModel


class CustomFastAPIUsers(FastAPIUsers[models.UP, models.ID]):
    """Class for calling the rewritten get_users_router function."""

    def get_users_router(
        self,
        user_schema: Type[schemas.U],
        user_update_schema: Type[schemas.UU],
        requires_verification: bool = False,
    ) -> APIRouter:

        return custom_get_users_router(
            self.get_user_manager,
            user_schema,
            user_update_schema,
            self.authenticator,
            requires_verification,
        )

    def get_verify_router(self, user_schema: Type[schemas.U]) -> APIRouter:
        """
        Return a router with e-mail verification route.

        :param user_schema: Pydantic schema of a public user.
        """
        return custom_get_verify_router(self.get_user_manager, user_schema)


def custom_get_users_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
    user_update_schema: Type[schemas.UU],
    authenticator: Authenticator,
    requires_verification: bool = False,
) -> APIRouter:
    """ Generate a router with the authentication routes.
    CUSTOM: Remove all admin routes.
    """
    router = APIRouter()

    get_current_active_user = authenticator.current_user(
        active=True, verified=requires_verification
    )

    async def get_user_or_404(
        id: str,
        user_manager:
            BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ) -> models.UP:
        try:
            parsed_id = user_manager.parse_id(id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

    @router.get(
        "/me",
        response_model=user_schema,
        name="users:current_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def me(
        user: models.UP = Depends(get_current_active_user),
    ):
        return schemas.model_validate(user_schema, user)

    @router.patch(
        "/me",
        response_model=user_schema,
        dependencies=[Depends(get_current_active_user)],
        name="users:patch_current_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                "summary": "A user with this "
                                           "email already exists.",
                                "value": {
                                    "detail":
                                    ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code":
                                        ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def update_me(
        request: Request,
        user_update: user_update_schema,  # type: ignore
        user: models.UP = Depends(get_current_active_user),
        user_manager:
            BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.update(
                user_update, user, safe=True, request=request
            )
            return schemas.model_validate(user_schema, user)
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
            )

    @router.delete(
        "/me",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        dependencies=[Depends(get_current_active_user)],
        name="users:delete_current_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def delete_user(
        request: Request,
        user: models.UP = Depends(get_current_active_user),
        user_manager:
            BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        await user_manager.delete(user, request=request)
        return None

    return router


def custom_get_verify_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
):
    """ Generate the verification router.
    CUSTOM: Remove /request-verify-token route.
    """
    router = APIRouter()

    @router.post(
        "/verify",
        response_model=user_schema,
        name="verify:verify",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.VERIFY_USER_BAD_TOKEN: {
                                "summary": "Bad token, not existing user or"
                                "not the e-mail currently set for the user.",
                                "value": {
                                    "detail": ErrorCode.VERIFY_USER_BAD_TOKEN
                                    },
                            },
                            ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                                "summary": "The user is already verified.",
                                "value": {
                                    "detail":
                                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                                },
                            },
                        }
                    }
                },
            }
        },
    )
    async def verify(
        request: Request,
        token: str = Body(..., embed=True),
        user_manager:
            BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.verify(token, request)
            return schemas.model_validate(user_schema, user)
        except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )
        except exceptions.UserAlreadyVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )

    return router