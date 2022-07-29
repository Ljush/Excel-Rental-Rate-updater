# readme.md
- Setting up directories
    Keep your excel sheets in the sheets folder.


"""
Potential Error that could be raised but likely won't be a real issue:
UserWarning: Data Validation extension is not supported and will be removed
  >>> warn(msg)

SO Solution: Excel has a feature called Data Validation 
(in the Data Tools section of the Data tab in my version) 
where you can pick from a list of rules to limit the type of 
data that can be entered in a cell. 
This is sometimes used to create dropdown lists in Excel. 
This warning is telling you that this feature is not supported 
by openpyxl, and those rules will not be enforced. 
If you want the warning to go away, you can click on the Data 
Validation icon in Excel, then click the Clear All button to 
remove all data validation rules and save your workbook."""