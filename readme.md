# What is Iter_3?
Iter_3 is at it's core is a series of APIs designed to quickly create and implement small python apps with large functionality. Iter_3 supports a wide variety of use cases and is undergoing heavy development currently. Some examples of apps currently designed as a plugin in Iter_3 are:
* Credential manager
* Note manager
* Calculator
Please keep in mind each of these is a feature rich application designed to work with the Iter_3 APIs.

## What can the Iter_3 API system do?
* User Management
* Server/Client interfacing made easy
* Implicit data transport and synchronized data execution
* Secure User session validation
* Easily customizeable UI

## What are some upcoming features?
* Server based settings storage
* Default global and local encryption for data


--------------------------
Pain points:
 - CRUD functions feel repetitive
 - Creating UI & hooking it up is time consuming
   - This is a direct result of the UI/Network not having a clean connection
   - Results are also a pain to pass back and forth (Something similar to callback hell)
 - Plugin system is a bit quirky


Both of the above can be simply solved with better integration through the
sqlAlchemy models. Eg a View models the data somehow, and has methods to interact with
the server to manipulate the data
