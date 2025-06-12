import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import Type

# Ensure the backend directory is in the Python path
# This might be needed if running scripts from the root directory
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir.parent)) # Add root dir

# Now import BaseNode safely
from backend.engine.base_node import BaseNode

# Define the path to the nodes directory relative to this file
NODES_DIR = Path(__file__).parent.parent / "nodes"

class NodeLoaderError(Exception):
    pass

_node_classes = None

def _find_node_classes():
    global _node_classes
    if _node_classes is not None:
        return _node_classes

    _node_classes = {}
    # Ensure the nodes directory is importable
    if str(NODES_DIR.parent) not in sys.path:
        sys.path.insert(0, str(NODES_DIR.parent))

    # Import all modules in the nodes directory
    for _, name, is_pkg in pkgutil.iter_modules([str(NODES_DIR)]):
        if not is_pkg:
            try:
                module = importlib.import_module(f"backend.nodes.{name}")
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and \
                       issubclass(obj, BaseNode) and \
                       obj is not BaseNode and \
                       not inspect.isabstract(obj):
                        if obj.__name__ in _node_classes:
                           raise NodeLoaderError(
                               f"Duplicate node type found: {obj.__name__} in {module.__file__} "
                               f"and {_node_classes[obj.__name__].__module__}")
                        _node_classes[obj.__name__] = obj
            except ImportError as e:
                print(f"Warning: Could not import module {name}: {e}")
            except Exception as e:
                 print(f"Warning: Error loading node classes from module {name}: {e}")

    if not _node_classes:
        print(f"Warning: No node classes found in {NODES_DIR}")

    return _node_classes

def get_node_class(node_type: str) -> Type[BaseNode]:
    classes = _find_node_classes()
    node_class = classes.get(node_type)
    if node_class is None:
        raise NodeLoaderError(f"Node type '{node_type}' not found. Available types: {list(classes.keys())}")
    return node_class

def reload_node_classes():
    """Forces reloading of node classes. Useful for development with --reload."""
    global _node_classes
    _node_classes = None
    # Clear previously imported node modules from sys.modules
    modules_to_remove = []
    prefix = "backend.nodes."
    for mod_name in sys.modules:
        if mod_name.startswith(prefix):
            modules_to_remove.append(mod_name)
    for mod_name in modules_to_remove:
        del sys.modules[mod_name]
    _find_node_classes() 