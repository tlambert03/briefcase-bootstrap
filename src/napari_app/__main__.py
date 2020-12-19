try:
    import sys
    import os

    # probably mac specific for now
    bin = os.path.join(os.path.dirname(sys.exec_prefix), "app_packages", "bin")
    os.environ["PATH"] = bin + os.pathsep + os.environ["PATH"]

    from napari.__main__ import main

    sys.exit(main())
except ImportError as e:
    from .bootstrap import BootStrap

    BootStrap().run()

except Exception as e:
    from .error import ErrorDialog

    ErrorDialog(e).run()