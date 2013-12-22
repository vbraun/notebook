Welcome to the Sage Notebook Documentation
==========================================

.. todo::

   Describe how to *use* the notebook.



Reference Manual
----------------

The notebook is a separate project from Sage, since GUI code works
different from computational code and has different documentation and
testing requirements. It is not independent, but instead relies on a
well-defined :doc:`sage_interface`. The compute server interface is
via bidirectional RPC. In particular there are no return values, if
you want a reply then you have to make a call that prompts the compute
server to make a call back to you. This is the only way you can have
responsive interfaces

The notebook follows the basic model/view/presenter pattern. The model
is the notebook data, the interface to the Sage compute server,
configuration data, etc. The view is the code that displays stuff to
the user. There are multiple interchangeable views to support
different technologies, for example there is a HTML/websocket and a
Gtk3 implementation. 

The presenter ties view to the model. In particular, the model is not
allowed to talk directly to the view and vice versa. Instead, the
presenter is to be informed of an action (for example, load a
worksheet) and then update the model and view accordingly.


.. toctree::
   :maxdepth: 2

   hacking
   sage_interface


Source Reference
----------------

.. toctree::
   :maxdepth: 2

   apidoc/sage_notebook/sage_notebook

   

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

