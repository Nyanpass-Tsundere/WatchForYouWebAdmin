from io import BytesIO
import subprocess 
import json
def tail(logFile,line,field=[0,1]):
    lFile = open(logFile,'a')
    lFile.close()
    
    ## for python 3.5
    #process = subprocess.run(['tail',logFile,'-n '+str(int(line))],stdout=subprocess.PIPE)
    #buf = BytesIO(process.stdout)

    ## for python 3.2
    buf = BytesIO( subprocess.check_output(['tail',logFile,'-n '+str(int(line))]) )
    data = []
    for line in buf.readlines():
        loadline = json.loads(line.decode())
        returnLine = []
        for i in field:
            returnLine.append(loadline[i])

        data.append( returnLine )

    return data
