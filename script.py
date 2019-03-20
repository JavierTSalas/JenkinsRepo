import jenkins
import sys
from lxml import etree
import os


def login():
     user = server.get_whoami()
     version = server.get_version()
     print('Hello %s from Jenkins %s' % (user['fullName'], version))


def installPlugins(plugins):
    '''
    Installs the plugins given in the list
    Returns bool if restart is required
    '''
    plugins_list=[key[0] for key in (server.get_plugins()).keys()]
    restart = True
    for plugin in plugins:
        if plugin not in plugins_list:
            restart = restart and server.install_plugin(plugin)
            print("Installing plugin:"+plugin)
    return restart


def createNewConfig(file_path,output_path):
    '''
    Makes a copy of the example PythonProject's build script and repalces the Git URL to the current working directory 
    '''
    doc = etree.parse(file_path)
    root=doc.getroot()
    
    # The path for the node that contains the location of our git folder
    code = root.xpath('//scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url')
    
    if code:
        # Replaces <url> text
        code[0].text = os.getcwd()
        # Save back to the XML file
        etree.ElementTree(root).write(output_path, pretty_print=True)

def createNewProject(project_name,output_path):

    data=''
    with open(output_path) as myfile:
        data="".join(line.rstrip() for line in myfile)
    server.create_job(project_name,data)


if __name__=="__main__":
    server = jenkins.Jenkins('http://localhost:8080', username='admin', password='9a93930a0ea54c829d696001d7815572')
    login()
    print("Starting JenkinsQuickStart")
    # Installs Jenkins Plugins
    plugins=['violations','git','cobertura']
    if installPlugins(plugins):
        print("Please restart Jenkins and relaunch the script")
        sys.exit(-1)
    
    # Replaces the elements using xml parser
    output_path='config_new.xml'
    python_config='PythonProject.xml'
   
    createNewConfig(python_config,output_path) 
    # Create a new project 
    project_name='NewPythonProject'
    createNewProject(project_name,output_path)
   
    # Fetch the build console 
    server.build_job(project_name)     

    print(server.debug_job_info(project_name))
