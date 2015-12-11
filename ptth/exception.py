# -*- coding: utf-8 -*-


class PtthError(Exception):
    pass


class PtthUrlError(PtthError):
    def __str__(self):
        return 'Invalid PTTH URL'


class PtthUpgradeFailed(PtthError):
    def __str__(self):
        return 'Failed to upgrade PTTH'
