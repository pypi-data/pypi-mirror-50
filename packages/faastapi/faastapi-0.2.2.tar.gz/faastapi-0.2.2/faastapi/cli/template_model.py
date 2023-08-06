from typing import List, Dict, Union, Any, Optional
from pydantic import BaseModel, constr, Schema


class MetaConfig(BaseModel):
    name: str
    version: str
    image: str
    label: Optional[constr(max_length=50)] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None


class CopyConfig(BaseModel):
    src: str
    dest: str = "."


class BuildConfig(BaseModel):
    dependencies: List[str] = []
    copy_files: List[CopyConfig] = Schema(default=[], alias="copy")
    extras: List[str] = []
    plugins: Dict[str, Union[dict, None]] = {}


class RunConfig(BaseModel):
    script: str
    function: str
    method: str = "post"
    input: List[Dict[str, Any]] = {}
    output: Union[Dict[str, Any], str] = {}
    environment: Dict[str, Any] = {}


class TemplateConfig(BaseModel):
    apiversion: str = "v1"
    meta: MetaConfig
    run: RunConfig
    build: BuildConfig = BuildConfig()
