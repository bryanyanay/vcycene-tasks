# vcycene-tasks
Bryan's attempt at the two tasks from Vcycene.

### How I would Debug Task 1
I start by downloading a null modem emulator (I used com0com) so that I can create a pair of 
serial ports that are connected. I can use these ports to test my receiver script.

I then create a sender script, which is basically a device emulator, with a function to emulate the actual device
sending data over to the receiver. This is necessary for testing the receiver throughout it's development.

I develop the receiver incrementally, testing after each feature I add before adding more. (You can see that in the history of git commits.)

For actual testing, all I did was have the sender send some test data, and see if the reciever does as I expect.
 - I have the sender and receiver print out what they're sending/receiving to verify if they match
 - I look at the contents of the dataRecord.txt file to see if the right data is being written
 - I use MySQL Workbench to check if the right data was written to the database
 - etc

I suppose for completeness I should make the sender send data that tests all edge cases (e.g., values at the edge of the ranges?), and write scripts that check if the data written to the file and database matches the test cases. 
I didn't do this though, I thought just checking a few cases by eye was enough.

Of course, during testing if I do discover problems I could debug with a debugger (stepping through, etc), or with
print statements, and the like. Fortunately, since I was developing it incrementally it was pretty obvious where the issues were when I did find bugs (I only added so much code each time after all) so I didn't have any hard to find bugs. (There were still some tricky ones though.)

### How I would debug Task 2

I used mosquitto as my mqtt broker, and it came with mosquitto_pub and mosquitto_sub, cmd-line mqtt client tools.

I used these tools to help test my app. E.g., to test whether the app was sending "Hello" to the "States" topic, I used `mosquitto_sub -t "States"`.

For testing if the GUI was correctly subscribing and displaying messages from the "Control" topic, I created a pubTest.py script. I could have used mosquitto_pub, but I just wanted to make a script.

Just like task 1, I tested incrementally after every feature added before moving on, making debugging much easier. 

Again, if I found any issues during testing I could use a debugger, use print statements, etc. I didn't actually find many issues though, which was good!