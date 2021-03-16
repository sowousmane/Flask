# Flask

Flask is a web micro-framework written in Python. It allows you to design a solid web application in a professional way.

What is a web micro-framework?

It is a set of modules that allow you to develop faster by providing common functionalities. When you design a web application, you always need to manage HTTP requests, a web server, display dynamic web pages, manage cookies... Why code these features every time? A web framework provides you with these features to start a project on a solid foundation.


**Using Flask to create a python application  



To test if this project is working well you have install Flask in your local computer by following the instructions bellow:  
- You have **clone the project** in your computer  
- change the branch because after clonning the project **you'll be in the main branch so you have to do: git checkout master**  so you'll be in the master branch  
- **ls** to verify if really you have the project in your computer.  

**Now let's insttaling flask**   
=> virtualenv env -p python3  
=> . env/bin/activate **don't forget the dot(.)**  
=> pip install flask  
now you can run your flask application by typping this command **in my case**  
**python3 run.py**  

*After you'll see something like this in your terminal that means your app is running sussefuly.  
 Serving Flask app "fbapp.views" (lazy loading)*  
 *Environment: production*  
   *WARNING: This is a development server. Do not use it in a production deployment.*  
   *Use a production WSGI server instead.*  
 *Debug mode: on*  
 *Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)*  
 *Restarting with stat*  
 *Debugger is active!*  
 *Debugger PIN: 134-874-021*  
*127.0.0.1 - - [03/Mar/2021 22:45:59] "GET / HTTP/1.1" 200 -*  
