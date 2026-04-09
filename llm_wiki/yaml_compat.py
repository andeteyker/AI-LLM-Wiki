from __future__ import annotations

from typing import Any


try:
    import yaml as _yaml  # type: ignore

    def safe_dump(data: dict[str, Any], sort_keys: bool = False) -> str:
        return _yaml.safe_dump(data, sort_keys=sort_keys)

    def safe_load(text: str) -> dict[str, Any]:
        return _yaml.safe_load(text)
except Exception:  # pragma: no cover
    def safe_dump(data: dict[str, Any], sort_keys: bool = False) -> str:
        items = data.items()
        if sort_keys:
            items = sorted(items)
        lines = []
        for k, v in items:
            if isinstance(v, dict):
                lines.append(f"{k}:")
                for sk, sv in v.items():
                    lines.append(f"  {sk}: {sv}")
            elif isinstance(v, list):
                lines.append(f"{k}: [{', '.join(map(str, v))}]")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines) + "\n"

    def _parse_value(value: str):
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                return []
            return [i.strip().strip("'\"") for i in inner.split(",")]
        if value.lower() in {"true", "false"}:
            return value.lower() == "true"
        try:
            if "." in value and value.replace(".", "", 1).isdigit():
                return float(value)
            if value.isdigit():
                return int(value)
        except ValueError:
            pass
        return value.strip("'\"")

    def safe_load(text: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        current_parent: str | None = None
        for line in text.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if line.startswith("  ") and current_parent and ":" in line:
                k, v = line.strip().split(":", 1)
                out.setdefault(current_parent, {})
                out[current_parent][k.strip()] = _parse_value(v)
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                key = k.strip()
                if v.strip() == "":
                    out[key] = {}
                    current_parent = key
                else:
                    out[key] = _parse_value(v)
                    current_parent = None
        return out
