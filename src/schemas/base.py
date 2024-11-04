from pydantic import BaseModel


class BaseCreateScheme(BaseModel):
    pass


class BaseUpdateScheme(BaseModel):
    pass


class BaseGetScheme(BaseModel):
    pass


class BaseSChemas:
    def __init__(
        self,
        create_scheme: BaseCreateScheme = None,
        update_scheme: BaseUpdateScheme = None,
        get_scheme: BaseGetScheme = None,
    ):
        self.create_scheme: BaseCreateScheme = create_scheme
        self.update_scheme: BaseUpdateScheme = update_scheme
        self.get_scheme: BaseGetScheme = get_scheme


def get_base_schemas() -> BaseSChemas:
    return BaseSChemas()
