# Sales Report App
***
Web based data report app with
  * django concepts (models, views, templates, signals and more!)
  * pandas dataframes , matplotlib and seaborn integration
  * pdf integration
  * javascript ajax integration
  * dropzone js for csv files
***

To start using webapp
1.  create virtual environment with:

    > virtualenv Django_DS

    > cd Django_DS

    then activate the environment using:

    > source bin/activate

    🔑 for Windows users:
    > source Scripts/activate

2.  Installing requirements:
    * Either by using command:
    > pip install r- requirements.txt
    
    * or by simply (in case above command show some error):
    > pip install django==3.2.6
    
    > pip install pillow django-crispy-forms matplotlib seaborn pandas xhtml2pdf python-decouple
    
3.  Now change current directory to `src`:
    > cd src
    
    then run the webapp using command:
    > python manage.py runserver
    
4.  Explore the app features.🤩
