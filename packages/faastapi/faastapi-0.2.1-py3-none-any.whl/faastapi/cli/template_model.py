from typing import Optional, List, Dict, Union
from pydantic import BaseModel, constr, Schema, Any


class MetaConfig(BaseModel):
    name: str
    version: str
    image: str
    label: Optional[constr(max_length=50)] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None


class CopyConfig(BaseModel):
    src: str
    dest: Optional[str] = "."


class BuildConfig(BaseModel):
    dependencies: Optional[List[str]] = None
    copy_files: Optional[List[CopyConfig]] = Schema(default=None, alias="copy")
    extras: Optional[List[str]] = None
    plugins: Optional[List[str]] = None


class RunConfig(BaseModel):
    script: str
    function: str
    method: str
    input: Optional[List[Dict[str, Any]]] = None
    output: Optional[Union[Dict[str, str], str]] = None
    environment: Dict[str, str] = {}


class TemplateConfig(BaseModel):
    apiversion: Optional[str] = "v1"
    meta: MetaConfig
    build: BuildConfig
    run: RunConfig
