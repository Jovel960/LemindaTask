def init(app):
    from .auth import init
    init(app)
    from .userOperations import init
    init(app)
    from .questions import init
    init(app)