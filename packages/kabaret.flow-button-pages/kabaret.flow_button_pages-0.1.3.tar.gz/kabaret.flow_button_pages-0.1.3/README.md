# kabaret.flow_button_pages

A collection of custom_page widgets to use in your flow, as well as 
an extended Home page showing thumbnail/icon and color for your Projects.

Button Home
===========

The Button Home extends the default Home page will a few options.

Right click on an empty space on the Home page to access the **Admin**
area. You will find the default Home with additional **Home Settings**: 
- **Show Status**: Will show the Project status below its name. 
- **Show Archived**: Will hide archived Project unless checked.
- **Button Height**: Height of each Project button.
- **Default Thumbnail**: Defines the thumbnail to use when
 no thumbnail is set on a Project.

As well as the **Project Settings**. You can edit them here, or with a
right click on a Project button -> **Configure**
- **Color**: use an hex color here, it will change the button text color.
- **Thumbnail**: Define the thumbnail to show on the button. You can 
use:
    - A file path (! avoid backslashes !)
    - A data uri. This will embed the image in the database. You can 
    use Chrome Developers Tools to get it from an image.
    - A classic **kabaret** resource identifier like `('icons.gui', 'start')`



In order to create a new Project or edit a Project status, you still need
to use the classic controls (The actions are in the **Admin** area's 
`Projects` Map). 

     
Usage
-----
In your Session class, override the `_create_actor()` method to create
a Flow actor using `ButtonHomeRoot` as custom home root:

          from kabaret.app.ui import gui
          from kabaret.app.actors.flow import Flow
          from kabaret.flow_button_pages import ButtonHomeRoot

          class MySession(gui.KabaretStandaloneGUISession):
          
              def _create_actors(self):
                  Flow(self, CustomHomeRootType=ButtonHomeRoot)

That's it ! \o/
    

    