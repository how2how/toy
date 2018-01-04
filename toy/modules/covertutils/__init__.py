"""
The ``covertutils`` module provides ready plug-n-play tools for `Remote Code Execution Agent` programming.
Features like `chunking`, `encryption`, `data identification` are all handled transparently by its classes.
The :class:`SimpleOrchestrator` handles all data manipulation, and the :class:`Handlers.BaseHandler` derivative classes handle the agent's and handler's actions and responses.

The module does not provide networking functionalities. All networking has to be wrapped by two functions (a sender and a receiver functions) and Handlers will use those for raw_data.
"""
