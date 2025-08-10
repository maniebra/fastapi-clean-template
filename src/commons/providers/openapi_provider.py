from typing import cast, TypeGuard
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi as fa_get_openapi


def _is_str_obj_dict(x: object) -> TypeGuard[dict[str, object]]:
    if not isinstance(x, dict):
        return False
    xd = cast(dict[object, object], x)
    for key in xd.keys():
        if not isinstance(key, str):
            return False
    return True


def _ensure_dict(root: dict[str, object], key: str) -> dict[str, object]:
    v = root.get(key)
    if not _is_str_obj_dict(v):
        v = {}
        root[key] = v
    return v


def build_openapi(app: FastAPI) -> dict[str, object]:
    schema: dict[str, object] = fa_get_openapi(
        title="FastAPI Clean Architecture Template",
        version="1.0.0",
        summary="This is the OpenAPI schema from FastAPI Clean Architecture Template",
        description="Here's a description of the custom **OpenAPI** schema",
        routes=app.routes,
    )

    components = _ensure_dict(schema, "components")
    security_schemes = _ensure_dict(components, "securitySchemes")
    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    security_req: list[dict[str, list[object]]] = [{"bearerAuth": []}]
    schema["security"] = security_req
    return schema
