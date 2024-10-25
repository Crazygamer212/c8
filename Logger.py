fileName = "log.txt"
path = False

def wipeLog(toUse = "log.txt"):
    global fileName
    fileName = toUse
    file = open(fileName,"w")
    file.write("")
    file.close()

def output(val,toUse = None):
    global fileName
    if toUse != None:
        TempName = toUse
    else:
        TempName = fileName
    import inspect
    stack = inspect.stack()
    caller_frame = stack[2]
    caller_file = caller_frame.filename.split("\\")[-1]
    file = open(TempName,"a", encoding="utf-8")
    if path:
        file.write(f"{caller_file} - {val}\n")
    else:
        file.write(f"{val}\n")
    file.close()



