## prasticus

[Package documentation: soon available](http://)

Catchall module extensible by plugins

This is a root module to allow its author to distribute
other modules as plugins. There are currently two subpackages:

* `prasticus.catchall` an extensible container for plugins.
* `prasticus.configure` a module configuration system.

## Post install

The `configure` subpackage needs a root directory to work. Create
a directory and initialize it with the command

    python -W ignore -m prasticus.configure set-root --create DIRECTORY
    
The `catchall` subpackage needs an initial configuration file to work.
Create one with the command

   python3 -m prasticus.configure init-config prasticus.catchall

### License

This software is licensed under the [MIT License](http://en.wikipedia.org/wiki/MIT_License)

© 2018 Eric Ringeisen
