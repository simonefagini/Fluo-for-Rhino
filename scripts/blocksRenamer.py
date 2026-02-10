import rhinoscriptsyntax as rs

def getPrefix():
    prefix = rs.GetString("Insert Prefix")
    
    if prefix is None:
       return
    
    return prefix

def batchRenamer():
    prefix = getPrefix()
    oldBlockNames = rs.BlockNames(True)
        
    if oldBlockNames:
        for name in oldBlockNames:
            newBlockName= (prefix + name)
            rs.RenameBlock (name,newBlockName)
    return

batchRenamer()