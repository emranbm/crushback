# Business metrics (Temporary)
Here the database business metrics exporter is built, due to a bug in the kubernetes service provider!  
This directory will be removed as soon as the bug is addressed.  

## K8S service provider bug
The kubernetes service provider of Crushback has an issue that prevents applying manifests containing 'select ...' anywhere in their values!  
Hence, we've managed to embed the value inside a built docker image.  

