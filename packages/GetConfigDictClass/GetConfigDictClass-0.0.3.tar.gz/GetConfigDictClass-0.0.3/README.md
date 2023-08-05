 cf = GetConfigDictClass.GetConfigDictClass(filename, filepath)
 
 print (cf.sections())
 
 res = cf.get('Section1', 'foo')
 
 print (res)