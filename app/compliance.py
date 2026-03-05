def calculate_compliance(helmet_count: int, head_count: int) -> dict:
    total_workers = helmet_count + head_count
    if total_workers == 0:
        compliance = 100.0
    else:
        compliance = round((helmet_count / total_workers) * 100, 2)

    return {
        "compliance_%": compliance,
        "status": "SAFE" if compliance == 100 else "VIOLATION",
        "helmet_count": helmet_count,
        "violations": head_count,
        "total_workers": total_workers
    }