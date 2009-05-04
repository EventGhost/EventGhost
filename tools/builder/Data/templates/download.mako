<%inherit file="layout.mako"/>\
<%def name="title()">Download EventGhost</%def>
<%def name="content_rst()" buffered="True"> 

Latest Version:
~~~~~~~~~~~~~~~

* `${files[0].name} <${files[0].target}>`_, ${files[0].size}, ${files[0].time}

Previous Versions:
~~~~~~~~~~~~~~~~~~

% for fileData in files[1:11]:
* `${fileData.name} <${fileData.target}>`_, ${fileData.size}, ${fileData.time}
% endfor


Other Downloads:
~~~~~~~~~~~~~~~~

* `X10 remote driver (for 32bit Windows) <x10drivers_x86.exe>`_
* `X10 remote driver (for 64bit Windows) <x10drivers_x64.exe>`_
* `Example files for the Webserver plugin <Webserver_Demo.zip>`_

</%def>
${rst2html(self.content_rst())}