import os

__all__ = [a.replace('.py', '') for a in os.listdir('bots') if a.endswith('py')]
