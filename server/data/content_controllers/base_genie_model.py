from humps import camelize
from pydantic import BaseModel, ConfigDict


class BaseGenieModel(BaseModel):
    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)
