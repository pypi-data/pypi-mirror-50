add
---

Add a file or directory.

========  =======  ===========================================
Name      Default  Description                                
========  =======  ===========================================
path      *None*   Path to local file to add                  
dest      *None*   Destination path of file                   
mode      *None*   The unix file mode to use for the tar file.
template  no       Treat added file as a template             
========  =======  ===========================================

env
---

Set container environment.

The environment variables are specified as the key/values.



export-deb
----------

Export files to a debian package.

=============  =======  ====================================================================================================================================================================================================================================================================================================================
Name           Default  Description                                                                                                                                                                                                                                                                                                         
=============  =======  ====================================================================================================================================================================================================================================================================================================================
dest           *None*   Local destination filename for package                                                                                                                                                                                                                                                                              
paths          *None*   List of paths to include in package                                                                                                                                                                                                                                                                                 
compress-type  xz       Compression to use for package                                                                                                                                                                                                                                                                                      
control        *None*   Control values for package, which is essentially the package metadata. The control contents can be specified as the literal file contents, or as a mapping. Consult the `Control Fields section of the Debian Policy Manual <https://www.debian.org/doc/debian-policy/ch-controlfields.html>`_ for more information.
=============  =======  ====================================================================================================================================================================================================================================================================================================================

export-rpm
----------

Export files to a rpm package.

=============  =======  =================================================================================================================================================
Name           Default  Description                                                                                                                                      
=============  =======  =================================================================================================================================================
name           *None*   RPM package name                                                                                                                                 
epoch          *None*   Epoch version, which is more significant than version or release                                                                                 
version        0.0      RPM version which is more sigificant than release, which intended to track upstream version.                                                     
release        0        RPM release number                                                                                                                               
arch           noarch   Architecture for package (example: noarch, x86_64)                                                                                               
rpm-os         Linux    Target operating system                                                                                                                          
url            *None*   Full url for more information about the package                                                                                                  
summary        *None*   A brief summary about the package                                                                                                                
description    *None*   A longer description about the package                                                                                                           
provides       *None*   A list of capabilities the package provides                                                                                                      
requires       *None*   A list of runtime dependencies for the package                                                                                                   
conflicts      *None*   A list of packages this package will conflict with                                                                                               
obsoletes      *None*   A list of packages this package obsoletes                                                                                                        
header         *None*   Additional rpm fields to provide manually                                                                                                        
compress-type  bzip2    The compression to use for the package contents                                                                                                  
dest           *None*   The destination file name to use for the package.  If not provided it will be automatically be determined from the `dest_dir` and version values.
dest-dir       .        The destination directory to put the package if dest is not explicitly provided                                                                  
paths          *None*   List of paths to include in package                                                                                                              
=============  =======  =================================================================================================================================================

export-tar
----------

Export files to a tar archive file.

=================  =======  =====================================================================================================================================
Name               Default  Description                                                                                                                          
=================  =======  =====================================================================================================================================
dest               *None*   The destination filename for the tar file                                                                                            
preamble           *None*   If provided, the tar file will contain this before the actual tar contents.  This can be used to make a self extracting runnable.    
preamble-encoding  utf-8    The encoding to write the preamble out as. Used if preamble is not provided as YAML !!binary type.                                   
compress-type      *None*   The compression type to use for the tar file. If not specified, the compression type will be inferred from the destination file name.
mode               *None*   The unix file mode to use for the tar file.                                                                                          
paths              *None*   List of paths to include in tar file                                                                                                 
=================  =======  =====================================================================================================================================

fail
----

Force the build to fail.



fetch
-----

Fetch a value from a url and save as a file in the image or variable.

========  =======  ==========================================================================
Name      Default  Description                                                               
========  =======  ==========================================================================
url       *None*   Url to fetch data from.                                                   
params    *None*   Key/values to pass as query string parameters                             
method    GET      HTTP method to use                                                        
dest-var  *None*   Destination variable to put output in                                     
json      no       If set, destination variable will be set with response converted from json
dest      *None*   Destination file to put output in                                         
========  =======  ==========================================================================

git
---

Add a git checkout to container image.

Before being added to the image, the git repo contents will be locally cached.

====  =======  ====================================
Name  Default  Description                         
====  =======  ====================================
repo  *None*   Git repository URL                  
dest  *None*   Destination in container image      
ref   master   Branch, tag or commit to checkout at
====  =======  ====================================

import-tar
----------

Import files from a tar archive file into the image.

====  =======  ================================================
Name  Default  Description                                     
====  =======  ================================================
dest  *None*   Destination path in image to unpack tar file to.
src   *None*   Local source path of tar file                   
====  =======  ================================================

include-vars
------------

Read variables from another yaml file.



local-run
---------

Run a command locally.

=======  =======  ==============
Name     Default  Description   
=======  =======  ==============
command  *None*   Command to run
=======  =======  ==============

patch
-----

No documentation available.

=========  =======  ===============================================
Name       Default  Description                                    
=========  =======  ===============================================
src        *None*   Patch file to apply                            
chdir      /        Directory to apply patch from                  
strip-dir  0        Strip directory prefixes from patched filenames
=========  =======  ===============================================

read-file
---------

Read contents of a file in the image into a variable.

====  =======  ===================================================
Name  Default  Description                                        
====  =======  ===================================================
path  *None*   Container file path to read data from              
var   *None*   Destination variable name to write file contents to
====  =======  ===================================================

run
---

Run a command in the container image.

=======  =======  ==============
Name     Default  Description   
=======  =======  ==============
command  *None*   Command to run
=======  =======  ==============

script
------

Run a script on the container image.

========  =======  ============================================
Name      Default  Description                                 
========  =======  ============================================
script    *None*   Script to push to container and run         
contents  *None*   Script contents to push to container and run
template  no       Treat script file via `script` as a template
========  =======  ============================================

set-image-attr
--------------

Set image attributes.

========  =======  ======================================================================================
Name      Default  Description                                                                           
========  =======  ======================================================================================
env       *None*   Environment variables to set on container image, specified as a mapping of key/values.
work-dir  *None*   Default working directory for commands                                                
========  =======  ======================================================================================

set-var
-------

Set a variable, specified as a mapping of key/value pairs.



