from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.domains.auth.models import (
    User
)

from app.domains.auth.repository import (
    AuthRepository
)

from app.domains.auth.schemas import (
    UserCreate
)

from app.core.security.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    async def register_user(
        db: AsyncSession,
        user_data: UserCreate
    ):

        existing_user = (
            await AuthRepository
            .get_user_by_email(
                db,
                user_data.email
            )
        )

        if existing_user:
            raise Exception(
                "User already exists"
            )

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(
                user_data.password
            )
        )

        return await (
            AuthRepository.create_user(
                db,
                user
            )
        )

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ):

        user = await (
            AuthRepository
            .get_user_by_email_or_username(
                db,
                email
            )
        )

        if not user:
            return None

        valid_password = verify_password(
            password,
            user.hashed_password
        )

        if not valid_password:
            return None

        token = create_access_token({
            "sub": str(user.id)
        })

        return token