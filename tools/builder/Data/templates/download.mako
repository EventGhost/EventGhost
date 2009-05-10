<%inherit file="layout.mako"/>\
<%def name="title()">Download EventGhost</%def>
<%def name="head()">\
    <meta http-equiv="expires" content="Sat, 15 Dec 2001 12:00:00 GMT">
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="pragma" content="no-cache">
${parent.head()}\
</%def>\
<%def name="content_rst()" buffered="True"> 

Latest release:
~~~~~~~~~~~~~~~

* `${files[0].name} <${files[0].target}>`_, ${files[0].size}, ${files[0].time}

Previous releases:
~~~~~~~~~~~~~~~~~~

% for fileData in files[1:11]:
* `${fileData.name} <${fileData.target}>`_, ${fileData.size}, ${fileData.time}
% endfor


Other downloads:
~~~~~~~~~~~~~~~~

* `X10 remote driver (for 32bit Windows) <x10drivers_x86.exe>`_
* `X10 remote driver (for 64bit Windows) <x10drivers_x64.exe>`_
* `Example files for the Webserver plugin <Webserver_Demo.zip>`_

</%def>
${rst2html(self.content_rst())}