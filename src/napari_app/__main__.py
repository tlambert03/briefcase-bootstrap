try:
    import sys
    import os
    import site

    # patch. see https://github.com/napari/napari/pull/2030
    nap = os.path.join(site.getsitepackages()[0], "napari")
    build_res = os.path.join(nap, "resources", "build_icons.py")
    with open(build_res, "r") as f:
        text = f.read()
    text = text.replace("check_call([name,", "check_call([sys.executable, name,")
    with open(build_res, "w") as f:
        f.write(text)

    # probably mac specific for now
    bin = os.path.join(os.path.dirname(sys.exec_prefix), "app_packages", "bin")
    os.environ["PATH"] = bin + os.pathsep + os.environ["PATH"]

    from napari.__main__ import main

    sys.exit(main())
except ImportError:
    from .bootstrap import BootStrap

    BootStrap().run()

except Exception:
    from .error import ErrorDialog

    ErrorDialog().run()
