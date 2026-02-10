from bibclean.models import Reference


def build_block_key(ref: Reference) -> str:
    if ref.doi:
        return f"doi:{ref.doi}"
    if ref.year and ref.first_author:
        return f"ya:{ref.year}:{ref.first_author}"
    prefix = ref.norm[:12] if ref.norm else ""
    return f"pref:{prefix}"
