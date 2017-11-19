## Why Promises?

The intention of this rather simple python module is to allow a simpler way for the application to separate our network layer from our UI. Our UI is already fairly removed from the application code (Yay), but before promises the network code was laced all throughout the code based. With Promises, there is now a guaranteed way to execute network code with a single line. On top of this, it also makes developing the code for both the client and server easier. You can view both actions in a single file. 
