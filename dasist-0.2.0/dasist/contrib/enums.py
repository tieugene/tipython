"""Misc common enumerates"""

from enum import IntEnum

class ERole(IntEnum):
    """ROLE_OMTSCHIEF, ROLE_SDOCHIEF"""
    Mgr = 1     # ROLE_ASSIGNEE
    Chief = 2
    Boss = 3
    Lawyer = 4
    Accounter = 5

class EState(IntEnum):
    Draft = 1       # Черновик
    OnWay = 2       # В пути (на подписи)
    Rejected = 3    # Завернут
    OnPay = 4       # В оплате (согласовано со всеми) (???)
    Done = 5        # Исполнен (Одобрено юристом > готово в архив)
