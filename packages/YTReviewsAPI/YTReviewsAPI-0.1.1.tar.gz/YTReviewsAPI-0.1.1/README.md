# OneReview Data Gathering Engine/ Database API 

The goal of this application was threefold. First, the application provides an API wrapper around the database. Second, the application actively scrapes/calls webpages/APIs to provide a coninuous stream of data. Finally, I wished to provide some kind of GUI to monitor the status of the database and collection process. 

## Justification

A full stack web application to collect/store/access data seems like overkill. This may be true. However, I believe in the seperation of concerns. I should not think about gathering/cleaning/accessing data while I build models; all of the data-side opperations should be done seperately.  

In addition to seperating functionality, this application can be configured to process data for other projects as well. It provides a good framework to work with down the line. 

As for the GUI, that was just for fun:). 

## Maintenance 

I have many more feature ideas for this project. Please check out our [issues](https://github.com/porterehunley/OneReview_Data_Collection/issues) page for an idea of things you want to see or upcoming releases. 

## Deployment

The project is deployed with Gunicorn and Nginx via an Ansible playbook.

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Ansible](https://docs.ansible.com/ansible/latest/index.html) - CI/CD
* [Gunicorn](http://docs.gunicorn.org/en/stable/index.html) - Used for production and deployment


## Authors

* **Porter Hunley** - *Sole contributer*

## License

This project is not licensed 

## Acknowledgments

* A huge thanks to Miguel Grinberg and his excellent [tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) on Flask. 