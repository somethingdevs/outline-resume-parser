def resolve_job_description(jd_text: str | None) -> dict | None:
    if jd_text and jd_text.strip():
        v = jd_text.strip()
        return {
            "source": "inline",
            "value": v,
            "chars": len(v),
        }
    return None
