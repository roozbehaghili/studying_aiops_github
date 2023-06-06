import os
import subprocess
import pandas as pd
import time
import glob
from pathlib import Path

def clone_git_repository(repo, target_path):
    url_git = 'https://github.com/' + repo
    os.chdir(target_path)
    repo2 = repo.replace('/', '-')
    git_clone_command = "git clone " + url_git + " " + repo2
    print("git clone {} ...".format(url_git))
    p = subprocess.Popen(git_clone_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    for line in p.stdout.readlines():
        output = output + str(line) + '\n'
    retval = p.wait()
    if retval == 0:
        # print(" Repository cloned successfully!")
        pass
    else:
        print(" Error in cloning!")
        print(output)
    return retval

def java_files(path, projectKey):
    input_path = path
    project_name = projectKey

    # print("JAVA: Now we are in project " + project_name)
    class_paths = ""
    flag = 0
    # print("injaa" + input_path+project_name)
    for root, dirs, files in os.walk(input_path+project_name):
        for file in files:
            if file.endswith("pom.xml"):
                # print(project_name, "is MAVEN")
                os.chdir(root)
                code = "mvn compile"
                p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = []
                for line in p.stdout.readlines():
                    output.append(str(line))
                retval = p.wait()
                # print(output)
                flag = 1
                break

            elif file.endswith("gradlew"):
                # print(project_name, "is GRADLE")
                os.chdir(root)
                code = "./gradlew classes"
                p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = []
                for line in p.stdout.readlines():
                    output.append(str(line))
                retval = p.wait()
                # print(output)
                flag = 1
                break
            elif file.endswith("build.xml"):
                # print(project_name, "is ANT")
                os.chdir(root)
                code = "ant -f build.xml"
                p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = []
                for line in p.stdout.readlines():
                    output.append(str(line))
                retval = p.wait()
                # print(output)
                flag = 1
                break
    if flag == 0:
        for root, dirs, files in os.walk(input_path+project_name):
            for file in files:
                if file.endswith(".java"):
                    # print(project_name, "is pure java (probably!)")
                    os.chdir(root)
                    code = "javac " + root + "/" + file
                    p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output = []
                    for line in p.stdout.readlines():
                        output.append(str(line))
                    retval = p.wait()
                    # print(output)
                    break

    for root, dirs, files in os.walk(input_path+project_name):
        for file in files: 
            if file.endswith(".class"):
                class_paths += root + "/,"
                break
    
    return class_paths

def read_source_script(filepath):
    if filepath.endswith(".ipynb"):
        with open(filepath, "r") as f:
            from nbconvert import PythonExporter
            import nbformat

            notebook = nbformat.reads(f.read(), nbformat.NO_CONVERT)
            exporter = PythonExporter()
            source, _ = exporter.from_notebook_node(notebook)
    else:
        with open(filepath, "r") as f:
            source = f.read()
    return source 

def create_py_file(path, source):
    with open(path, 'w') as f:
        f.write(source)
        f.flush()

def jupyter_files(path, projectKey):
    input_path = path+projectKey

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".ipynb"):
                # print("flagg" + root + file)
                inputtt = os.path.join(root, file)
                source = read_source_script(inputtt)
                create_py_file(inputtt, source)
                p = Path(inputtt)
                p.rename(p.with_suffix('.py'))    


def run_sonar_scanner(path, projectKey, language):
    # print("now we are in project " + projectKey)
    os.chdir(path + projectKey)
    # print("this is path" + path+projectKey)
    # path_repos_properties = path + "sonar-project.properties"
    # trainingStream = open(path_repos_properties, 'w')
    
    for root, dirs, files in os.walk(path+projectKey):
        for file in files: 
            if file.endswith(".java"):
                language = 'java'
                break
            elif file.endswith(".ipynb"):
                try:
                    jupyter_files(path, projectKey)
                    break 
                except:
                    print(projectKey + " failed. (python)")

    if language == 'java':
        try:
            class_paths = java_files(path, projectKey)
        except:
            print(projectKey + " failed. (java)")

        code = "sonar-scanner" + " -Dsonar.projectName=" + projectKey + " -Dsonar.projectKey=" + projectKey + " -Dsonar.sources=." + " -Dsonar.host.url=http://localhost:9000" + " -Dsonar.login=5edeaf624db320ccfc7ec1dd868383cc9a458ac5" + " -Dsonar.java.binaries=." 
    else:
        code = "sonar-scanner" + " -Dsonar.projectName=" + projectKey + " -Dsonar.projectKey=" + projectKey + " -Dsonar.sources=." + " -Dsonar.host.url=http://localhost:9000" + " -Dsonar.login=5edeaf624db320ccfc7ec1dd868383cc9a458ac5"

    print(code)

    # print("Executing sonar scanner on: {}".format(projectKey))

    os.chdir(path + projectKey)
    p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = []
    output_str = ''
    for line in p.stdout.readlines():
        output.append(str(line))
        
        output_str += str(line)+'\n'
    retval = p.wait()
    # print(output_str)
    # if retval == 0:
    #     print("  -- Execution successfull!")

    # if language == '':
    #     trainingStream.write('sonar.projectKey=' + projectKey + '\n' \
    #                         'sonar.projectName=' + projectKey + '\n' \
    #                         'sonar.projectVersion=1.0\n' \
    #                         'sonar.login=admin\n' \
    #                         'sonar.password=Admin123@\n' \
    #                         'sonar.host.url=http://localhost:9000\n' \
    #                         'sonar.sources=' + projectKey + '\n' \
    #                         'sonar.sourceEncoding=UTF-8')
    # elif 'C' in language:
    #     trainingStream.write('sonar.projectKey=' + projectKey + '\n' \
    #                         'sonar.projectName=' + projectKey + '\n' \
    #                         'sonar.projectVersion=1.1\n' \
    #                         'sonar.login=admin\n' \
    #                         'sonar.password=Admin123@\n' \
    #                         'sonar.host.url=http://localhost:9000\n' \
    #                         'sonar.cxx.gcc.reportPath=*.log\n' \
    #                         'sonar.cxx.gcc.charset=UTF-8\n' \
    #                         'sonar.language=C++\n' \
    #                         'sonar.cpp.file.suffixes=.cc,.cpp,.cxx,.c++,.hh,.hpp,.hxx,.h++,.ipp,.c,.h\n'\
    #                         'sonar.sources=' + projectKey + '\n' \
    #                         'sonar.sourceEncoding=UTF-8')
    # else:
    #     trainingStream.write('sonar.projectKey=' + projectKey + '\n' \
    #                         'sonar.projectName=' + projectKey + '\n' \
    #                         'sonar.login=admin\n' \
    #                         'sonar.password=Admin123@\n' \
    #                         'sonar.projectVersion=1.0\n' \
    #                         'sonar.host.url=http://localhost:9000\n' \
    #                         'sonar.sources=' + projectKey + '\n' \
    #                         'sonar.language=' + language + '\n' \
    #                         'sonar.sourceEncoding=UTF-8')

    # trainingStream.close()
    # git_log_command = "sonar-scanner"
    # command = "sonar-scanner " + path_repos_properties
    # os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")
    

def main_report():

    report_path = '/home/roozbeh/Desktop/SonarQube/sonar_results_ml3/'
    input_path = '/home/roozbeh/Desktop/SonarQube/'
    file = 'ml_final.csv'

    df = pd.read_csv(input_path + file, usecols = ['Repos'])
    Repos_Name = sum(df.values.tolist(), [])

    os.chdir(report_path)

    for index in range(len(Repos_Name)):
        project = str(Repos_Name[index]).replace('/', '-')
        print(project)
        try:
            command = "java -jar /home/roozbeh/Desktop/SonarQube/Sonar_files/sonar-cnes-report-4.1.1.jar -t 5edeaf624db320ccfc7ec1dd868383cc9a458ac5  -s http://localhost:9000/ -p "+project+" -r ./template.csv"
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(3)
        except:
            print(project + " failed. (getting the report)")

def main_scanner():
    report_path = '/home/roozbeh/Desktop/SonarQube/repos_ml/'
    input_path = '/home/roozbeh/Desktop/SonarQube/'
    file = 'ml_final.csv'
    
    df = pd.read_csv(input_path + file, usecols = ['Repos'])
    Repos_Name = sum(df.values.tolist(), [])
    for index in range(len(Repos_Name)):
        clone_git_repository(Repos_Name[index], report_path)
        # project2 = str(Repos_Name[index]).split('/')[1]
        project = str(Repos_Name[index]).replace('/', '-')
        run_sonar_scanner(report_path, project, '')
        time.sleep(5)

# main_scanner()
main_report()